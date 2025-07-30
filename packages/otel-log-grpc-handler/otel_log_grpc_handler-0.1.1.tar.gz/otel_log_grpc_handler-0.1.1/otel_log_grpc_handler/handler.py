import logging
import grpc
import time
import sys
import threading
import collections
import atexit
# Attempt conditional import for the mapper
try:
    from otel_log_proto_mapper.converter import convert_log_record
    _HAS_DEFAULT_MAPPER = True
except ImportError:
    _HAS_DEFAULT_MAPPER = False

# --- OTLP Protobuf Imports (still needed by the handler for protobuf messages) ---
from opentelemetry.proto.collector.logs.v1 import logs_service_pb2_grpc
from opentelemetry.proto.collector.logs.v1 import logs_service_pb2
from opentelemetry.proto.common.v1 import common_pb2
from opentelemetry.proto.resource.v1 import resource_pb2
from opentelemetry.proto.logs.v1 import logs_pb2 as otel_logs_pb2


class OTLPGrpcLogHandler(logging.Handler):
    """
    A custom logging handler that sends LogRecords to an OTLP collector via gRPC.
    Implements client-side batching for efficiency and robustness.
    Automatically registers its close method with atexit for graceful shutdown.
    """


    def __init__(self, endpoint: str,
                 resource_attributes: list[common_pb2.KeyValue] | None = None,
                 max_batch_size: int = 100, flush_interval: float = 1.0,
                 max_queue_size: int = 2048,
                 log_record_converter=None):
        super().__init__()
        self.endpoint = endpoint
        self.max_batch_size = max_batch_size
        self.flush_interval = flush_interval
        self.max_queue_size = max_queue_size

        self.resource_attributes = (
            resource_attributes if resource_attributes is not None
            else OTLPGrpcLogHandler.build_resource_attributes('unknown')
        )

        # Determine the log record conversion function
        if log_record_converter:
            self._log_record_converter_func = log_record_converter
        elif _HAS_DEFAULT_MAPPER:
            self._log_record_converter_func = convert_log_record
        else:
            raise ImportError(
                "The 'otel-log-proto-mapper' package is not installed. "
                "Please install it (e.g., `pip install otel-log-grpc-handler[mapper]`) "
                "or provide a custom `log_record_converter` function to the handler's constructor."
            )

        self.channel = None
        self.stub = None
        self.buffer = collections.deque()
        self.buffer_lock = threading.Lock()
        self.flush_event = threading.Event()
        self.shutdown_event = threading.Event()

        self._internal_logger = logging.getLogger(f"{self.__class__.__name__}.internal")
        self._internal_logger.setLevel(logging.INFO)
        if not self._internal_logger.handlers:
            console_handler = logging.StreamHandler(sys.stderr)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(formatter)
            self._internal_logger.addHandler(console_handler)
            self._internal_logger.propagate = False

        self.flush_thread = threading.Thread(target=self._flush_loop, daemon=True)
        self.flush_thread.start()

        self._connect()
        atexit.register(self.close)
        self._internal_logger.info("OTLPGrpcLogHandler's close method automatically registered with atexit.")

    @staticmethod
    def build_resource_attributes(
        service_name: str,
        deployment_environment: str | None = None,
        host_ip: str | None = None,
        host_name: str | None = None,
        service_namespace: str | None = None,
    ) -> list[common_pb2.KeyValue]:
        return [
            common_pb2.KeyValue(key=key, value=common_pb2.AnyValue(string_value=value))
            for key, value in [
                ("service.name", service_name),
                ("deployment.environment", deployment_environment),
                ("host.ip", host_ip),
                ("host.name", host_name),
                ("service.namespace", service_namespace),
            ]
            if value is not None
        ]

    def _connect(self):
        """Establishes gRPC channel and stub."""
        try:
            if self.channel is None or (hasattr(self.channel, '_channel_closed') and self.channel._channel_closed):
                self.channel = grpc.insecure_channel(self.endpoint)
                self.stub = logs_service_pb2_grpc.LogsServiceStub(self.channel)
                self._internal_logger.info(f"Connected to OTLP collector at {self.endpoint}")
            elif self.stub is None:
                self.stub = logs_service_pb2_grpc.LogsServiceStub(self.channel)
        except Exception as e:
            self._internal_logger.error(f"Failed to connect/reconnect to OTLP collector at {self.endpoint}: {e}", exc_info=True)
            self.channel = None
            self.stub = None

    def emit(self, record: logging.LogRecord):
        # Prevent self-recursion
        if record.name.startswith(self._internal_logger.name):
            print(f"preventing recursion for {record}")
            return

        with self.buffer_lock:
            if len(self.buffer) >= self.max_queue_size:
                self._internal_logger.warning(f"Log buffer full ({self.max_queue_size} messages), dropping log: {record.getMessage()}")
                return
            self.buffer.append(record)

        if len(self.buffer) >= self.max_batch_size:
            self.flush_event.set()

    def _flush_loop(self):
        """Background thread loop for flushing logs."""
        while not self.shutdown_event.is_set():
            flushed = self.flush_event.wait(timeout=self.flush_interval)
            self.flush_event.clear()

            with self.buffer_lock:
                # Only attempt to pop if there are logs to flush
                if len(self.buffer) > 0 and (flushed or (time.time() - self.buffer[0].created > self.flush_interval)):
                    records_to_flush = []
                    # Pop up to max_batch_size, or all if less than max_batch_size
                    for _ in range(min(len(self.buffer), self.max_batch_size)):
                        records_to_flush.append(self.buffer.popleft())
                else:
                    records_to_flush = []

            if records_to_flush:
                self._send_batch(records_to_flush)

        # Final flush on shutdown
        self._internal_logger.info("Flushing remaining logs on shutdown...")
        # Get all remaining records from the buffer for the final flush
        with self.buffer_lock:
            remaining_records = list(self.buffer)
            self.buffer.clear()
        self._send_batch(remaining_records)
        self._internal_logger.info("Remaining logs flushed.")


    def _send_batch(self, records: list):
        """Sends a batch of LogRecords to the OTLP collector."""
        if not records:
            return

        if not self.stub:
            self._connect()
            if not self.stub:
                self._internal_logger.error(f"Cannot send batch of {len(records)} logs: collector not connected.")
                return

        try:
            otel_log_records = [self._convert_log_record(r) for r in records]

            resource = resource_pb2.Resource(attributes=self.resource_attributes)

            scope_logs = otel_logs_pb2.ScopeLogs(
                scope=common_pb2.InstrumentationScope(name="python.logging", version="1.0"),
                log_records=otel_log_records,
            )

            resource_logs = otel_logs_pb2.ResourceLogs(scope_logs=[scope_logs], resource=resource)

            request = logs_service_pb2.ExportLogsServiceRequest(
                resource_logs=[resource_logs]
            )

            self.stub.Export(request, timeout=5)
            self._internal_logger.debug(f"Successfully sent batch of {len(records)} logs.")
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                self._internal_logger.error(f"OTLP collector unavailable for batch: {e.details}. Disconnecting to retry.", exc_info=True)
                # No channel.close() here as it might be closed by another handler in _flush_loop's final flush
                # Self-healing will attempt _connect() on next send
                if self.channel: # Ensure channel object exists before attempting close
                    self.channel.close()
                self.channel = None
                self.stub = None
            else:
                self._internal_logger.error(f"Error sending batch of {len(records)} logs to OTLP collector: {e.details}", exc_info=True)
        except Exception as e:
            self._internal_logger.error(f"Unexpected error in OTLP batch sender: {e}", exc_info=True)

    def _convert_log_record(self, record: logging.LogRecord) -> otel_logs_pb2.LogRecord:
        """Uses the selected log record converter function."""
        # Pass self.format for traceback formatting
        return self._log_record_converter_func(record, formatter_func=self.format)

    def flush(self):
        """Forces a flush of the buffer."""
        self._internal_logger.debug("Manual flush requested.")
        self.flush_event.set()
        # Give the flush thread a moment to pick up the signal
        # For a truly synchronous flush, you'd acquire the lock and call _send_batch directly.
        # But this is often fine for a 'best effort' manual flush.
        self.flush_thread.join(timeout=self.flush_interval * 2)

    def close(self):
        """Signals the flush thread to shut down and flushes remaining logs."""
        # Only close if it hasn't been closed already (atexit might call multiple times or after manual close)
        if not self.shutdown_event.is_set():
            self._internal_logger.info("Closing OTLPGrpcLogHandler...")
            self.shutdown_event.set()
            self.flush_event.set() # Wake up the thread if it's waiting
            self.flush_thread.join(timeout=10) # Wait for the flush thread to finish

            if self.flush_thread.is_alive():
                self._internal_logger.warning("Flush thread did not shut down cleanly. Some logs might be lost.")

            if self.channel:
                self.channel.close()
                self._internal_logger.info(f"Closed OTLP collector connection to {self.endpoint}")
            # Do not call super().close() if using atexit, as atexit registers direct callables
            # and logging.Handler's close() might be called multiple times if handled by atexit and root_logger.removeHandler
            # For simplicity, if we rely on atexit, we manage resources directly here.
        super().close() # Call parent close to mark handler as closed


# --- Global Logger Setup ---
def setup_logging_with_custom_otel_handler(
    service_name: str,
    otel_collector_endpoint: str | None = None,
    enable_otel_logs: bool = False,
    max_batch_size: int = 100,
    flush_interval: float = 1.0,
    max_queue_size: int = 2048
):
    """
    Sets up standard Python logging with a custom OTLP handler.
    The handler itself handles atexit registration.
    """
    logging.getLogger().handlers = []

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    if enable_otel_logs and otel_collector_endpoint:
        otlp_handler = OTLPGrpcLogHandler(
            endpoint=otel_collector_endpoint,
            resource_attributes=OTLPGrpcLogHandler.build_resource_attributes(service_name),
            max_batch_size=max_batch_size,
            flush_interval=flush_interval,
            max_queue_size=max_queue_size
        )
        otlp_handler.setLevel(logging.INFO)
        root_logger.addHandler(otlp_handler)
        logging.info(f"Custom OTLP logging handler with batching and auto-atexit added for {otel_collector_endpoint}.")
    else:
        logging.info("Custom OTLP logging handler not enabled.")
