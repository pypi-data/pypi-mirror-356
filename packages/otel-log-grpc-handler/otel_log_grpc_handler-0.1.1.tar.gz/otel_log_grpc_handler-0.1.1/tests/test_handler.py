import logging
import pytest
import time
import sys
import uuid # For unique log IDs in tests

from otel_log_grpc_handler.handler import OTLPGrpcLogHandler
from opentelemetry.proto.common.v1 import common_pb2
from opentelemetry.proto.logs.v1 import logs_pb2 as otel_logs_pb2

# A semi-random mapper for testing the handler's transport logic
def semi_random_log_record_converter(record: logging.LogRecord, formatter_func=None) -> otel_logs_pb2.LogRecord:
    """A mock converter that produces a predictable but unique OTLP LogRecord."""
    log_id = str(uuid.uuid4())
    return otel_logs_pb2.LogRecord(
        time_unix_nano=int(record.created * 1e9),
        severity_number=otel_logs_pb2.SeverityNumber.SEVERITY_NUMBER_INFO,
        severity_text="INFO",
        body=common_pb2.AnyValue(string_value=f"Test log: {record.getMessage()} - ID: {log_id}"),
        attributes=[
            common_pb2.KeyValue(key="test.log.id", value=common_pb2.AnyValue(string_value=log_id)),
            common_pb2.KeyValue(key="original.level", value=common_pb2.AnyValue(string_value=record.levelname)),
            common_pb2.KeyValue(key="test.source", value=common_pb2.AnyValue(string_value="mock_converter")),
        ]
    )

@pytest.fixture
def clean_logger():
    """Fixture to ensure the logging system is clean before each test."""
    root_logger = logging.getLogger()
    # Remove all handlers that might have been added by previous tests or fixtures
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
        handler.close() # Ensure resources are released
    root_logger.setLevel(logging.WARNING) # Set a default level to avoid excessive console output
    yield
    # Clean up again after test
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
        handler.close()


def test_handler_sends_mapped_messages(otlp_grpc_mock_server, clean_logger):
    endpoint, servicer = otlp_grpc_mock_server
    servicer.clear_requests() # Clear any requests from previous tests

    root_logger = logging.getLogger()
    handler = OTLPGrpcLogHandler(
        endpoint=endpoint,
        resource_attributes=OTLPGrpcLogHandler.build_resource_attributes("test-handler-module"),
        max_batch_size=2, # Small batch size for quick flushing
        flush_interval=0.1,
        log_record_converter=semi_random_log_record_converter # Provide our custom mapper
    )
    handler.setLevel(logging.INFO)
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)

    # Emit logs
    test_message_1 = "Log Message One"
    logging.info(test_message_1)
    test_message_2 = "Log Message Two"
    logging.info(test_message_2)
    test_message_3 = "Log Message Three"
    logging.info(test_message_3) # This will cause a flush as batch_size is 2

    # Wait for requests to be received by the mock server
    assert servicer.wait_for_requests(num_log_records=2) # Expect first batch

    # Verify received messages
    received_batch_1 = servicer.received_requests[0]
    assert len(received_batch_1.resource_logs[0].scope_logs[0].log_records) == 2
    log_record_1 = received_batch_1.resource_logs[0].scope_logs[0].log_records[0]
    log_record_2 = received_batch_1.resource_logs[0].scope_logs[0].log_records[1]

    assert test_message_1 in log_record_1.body.string_value
    assert test_message_2 in log_record_2.body.string_value
    assert get_attribute_value(log_record_1.attributes, "test.source") == "mock_converter"

    # Ensure the remaining message is flushed on handler close (atexit)
    handler.close() # Manually trigger close for test
    assert servicer.wait_for_requests(num_log_records=3) # Expect the remaining one to be flushed

    received_batch_2 = servicer.received_requests[1] # This might be the 3rd log if flushed separately or in a different batch
    # More robust check is to look at all received logs.
    all_received_bodies = [
        lr.body.string_value
        for req in servicer.received_requests
        for rl in req.resource_logs
        for sl in rl.scope_logs
        for lr in sl.log_records
    ]

    assert any(test_message_1 in body for body in all_received_bodies)
    assert any(test_message_2 in body for body in all_received_bodies)
    assert any(test_message_3 in body for body in all_received_bodies)

def get_attribute_value(attributes, key):
    for attr in attributes:
        if attr.key == key:
            if attr.value.HasField("string_value"): return attr.value.string_value
            if attr.value.HasField("int_value"): return attr.value.int_value
            if attr.value.HasField("double_value"): return attr.value.double_value
            if attr.value.HasField("bool_value"): return attr.value.bool_value
    return None
