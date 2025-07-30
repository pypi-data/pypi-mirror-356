# otel-log-grpc-handler

A Python `logging.Handler` that facilitates sending log messages to an OpenTelemetry Protocol (OTLP) collector via gRPC. This handler is designed for flexibility, allowing users to either leverage an automatic LogRecord-to-OTLP protobuf mapper (provided by the `otel-log-proto-mapper` package) or to supply their own custom mapping function.

## Features

-   **Seamless OTLP Export:** Buffers and asynchronously sends Python `LogRecord`s to an OTLP gRPC endpoint.
-   **Optional LogRecord Mapping:**
    -   Automatically uses `otel-log-proto-mapper` if installed, providing out-of-the-box conversion from `logging.LogRecord` to OTLP `LogRecord` protobufs.
    -   Allows users to provide a custom `log_record_converter` callable if `otel-log-proto-mapper` is not installed or if a different mapping is desired.
-   **Configurable Batching:** Control the batch size and flush interval for efficient log transmission.
-   **Thread-Safe:** Designed to handle logging from multiple threads.
-   **Robust Shutdown:** Integrates with `atexit` for graceful shutdown, ensuring buffered logs are sent before application exit.

## Installation

Install the core handler:

```bash
pip install otel-log-grpc-handler
## or
pip install otel-log-grpc-handler[mapper]
```

## Usage

### Basic Usage (with automatic mapper)

This assumes you have installed the handler with the `[mapper]` extra (e.g., `pip install otel-log-grpc-handler[mapper]`).

```python
import logging
import time
from otel_log_grpc_handler.handler import OTLPGrpcLogHandler

# Configure your logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create an OTLP gRPC handler
# Replace "localhost:4317" with your OTLP collector endpoint
# The handler will automatically look for 'otel-log-proto-mapper'
# to convert log records.
handler = OTLPGrpcLogHandler(
    endpoint="localhost:4317",
    service_name="my-python-app",
    max_batch_size=10,
    flush_interval=1.0 # Flush every 1 second or after 10 logs
)

# Add the handler to your logger
logger.addHandler(handler)

# Example logging
logger.info("Hello from my Python application!")
logger.warning("Something potentially problematic happened.")
try:
    1 / 0
except ZeroDivisionError:
    logger.error("An error occurred during division.", exc_info=True)
```

### Usage with a Custom LogRecord Converter

If you do not install `otel-log-proto-mapper` or prefer to implement your own conversion logic, you can pass a callable to the `log_record_converter` parameter.

Your custom converter function must accept a `logging.LogRecord` and an optional `formatter_func` (for formatting exceptions) and return an `opentelemetry.proto.logs.v1.logs_pb2.LogRecord` object.

```python
import logging
import time
from otel_log_grpc_handler.handler import OTLPGrpcLogHandler
from opentelemetry.proto.common.v1 import common_pb2
from opentelemetry.proto.logs.v1 import logs_pb2 as otel_logs_pb2

# --- Your Custom LogRecord Converter ---
def my_custom_converter(record: logging.LogRecord, formatter_func=None) -> otel_logs_pb2.LogRecord:
    # This is a very simplified example.
    # In a real scenario, you'd parse more attributes and handle types carefully.
    body_value = record.getMessage()

    attributes = [
        common_pb2.KeyValue(key="logger.name", value=common_pb2.AnyValue(string_value=record.name)),
        common_pb2.KeyValue(key="custom_tag", value=common_pb2.AnyValue(string_value="my_special_log")),
    ]

    if record.exc_info and formatter_func:
        # Use the formatter_func provided by the handler for detailed stack traces
        attributes.append(common_pb2.KeyValue(key="exception.stacktrace",
                                               value=common_pb2.AnyValue(string_value=formatter_func(record))))

    return otel_logs_pb2.LogRecord(
        time_unix_nano=int(record.created * 1e9),
        severity_number=otel_logs_pb2.SeverityNumber.SEVERITY_NUMBER_INFO, # Simplified for example
        severity_text=record.levelname,
        body=common_pb2.AnyValue(string_value=body_value),
        attributes=attributes,
    )
# --- End Custom Converter ---


logger = logging.getLogger("custom_app")
logger.setLevel(logging.DEBUG)

# Create the handler, explicitly passing your custom converter
handler = OTLPGrpcLogHandler(
    endpoint="localhost:4317",
    service_name="my-custom-converter-app",
    log_record_converter=my_custom_converter # Provide your custom function
)

logger.addHandler(handler)

logger.debug("Debug message with custom converter.")
logger.info("Info message with custom converter.")
```
