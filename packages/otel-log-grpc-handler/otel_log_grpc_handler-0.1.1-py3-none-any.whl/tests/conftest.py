import pytest
import grpc
import time
import threading
import collections
from concurrent import futures

from opentelemetry.proto.collector.logs.v1 import logs_service_pb2
from opentelemetry.proto.collector.logs.v1 import logs_service_pb2_grpc

class MockLogsServiceServicer(logs_service_pb2_grpc.LogsServiceServicer):
    """A mock gRPC server servicer to capture OTLP ExportLogsServiceRequest."""
    def __init__(self):
        self.received_requests = collections.deque()
        self.received_log_records = 0
        self.request_event = threading.Event() # To signal when a request is received

    def Export(self, request: logs_service_pb2.ExportLogsServiceRequest, context):
        """Implements the Export RPC for LogsService."""
        self.received_requests.append(request)

        self.received_log_records += sum(
            len(sl.log_records)
            for rl in request.resource_logs
            for sl in rl.scope_logs
        )

        self.request_event.set() # Signal that a request has been received
        return logs_service_pb2.ExportLogsServiceResponse()

    def clear_requests(self):
        """Clears the list of received requests."""
        self.received_requests.clear()
        self.received_log_records = 0
        self.request_event.clear()

    def wait_for_requests(self, num_log_records: int, timeout: float = 5.0):
        """Waits until a certain number of requests are received."""
        start_time = time.time()
        while self.received_log_records < num_log_records and (time.time() - start_time < timeout):
            self.request_event.wait(timeout=max(0, timeout - (time.time() - start_time)))
            self.request_event.clear() # Clear after waiting
        return self.received_log_records >= num_log_records


@pytest.fixture(scope="module")
def otlp_grpc_mock_server():
    """Pytest fixture to start and stop a mock OTLP gRPC server."""
    servicer = MockLogsServiceServicer()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    logs_service_pb2_grpc.add_LogsServiceServicer_to_server(servicer, server)

    # Start the server on a random available port
    port = server.add_insecure_port('localhost:0')
    server.start()
    print(f"\nMock gRPC server started on localhost:{port}")

    # Yield the server address and the servicer instance for tests to use
    yield f"localhost:{port}", servicer

    # Teardown: Stop the server after all tests in the module are done
    server.stop(grace=5).wait() # Wait up to 5 seconds for graceful shutdown
    print(f"\nMock gRPC server on localhost:{port} stopped.")
