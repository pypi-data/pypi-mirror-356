import logging
import pytest
import time
import sys

# The handler will import this conditionally, but for the test, we'll ensure it's available
try:
    from otel_log_proto_mapper.converter import convert_log_record
    _HAS_MAPPER = True
except ImportError:
    _HAS_MAPPER = False
    pytest.skip("otel-log-proto-mapper not installed, skipping integration tests", allow_module_level=True)


from otel_log_grpc_handler.handler import OTLPGrpcLogHandler # Assuming your handler is in otel_log_grpc_handler/handler.py


@pytest.fixture
def clean_logger():
    """Fixture to ensure the logging system is clean before each test."""
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
        handler.close()
    root_logger.setLevel(logging.WARNING)
    yield
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
        handler.close()


def test_integration_with_default_mapper(otlp_grpc_mock_server, clean_logger):
    endpoint, servicer = otlp_grpc_mock_server
    servicer.clear_requests()

    root_logger = logging.getLogger()
    # No custom converter passed; handler should use the default mapper if available
    handler = OTLPGrpcLogHandler(
        endpoint=endpoint,
        resource_attributes=OTLPGrpcLogHandler.build_resource_attributes("test-integration"),
        max_batch_size=1, # Smaller batch size for immediate flushing
        flush_interval=0.1
    )
    root_logger.setLevel(logging.INFO)
    handler.setLevel(logging.INFO)
    root_logger.addHandler(handler)

    test_message = "This is an integration test message."
    extra_data = {"request_id": "test-req-123"}
    logging.info(test_message, extra=extra_data)

    # Wait for the message to be received
    assert servicer.wait_for_requests(num_log_records=1)

    # Verify the received message content
    received_request = servicer.received_requests[0]
    assert len(received_request.resource_logs) == 1
    resource_log = received_request.resource_logs[0]
    assert len(resource_log.scope_logs) == 1
    scope_log = resource_log.scope_logs[0]
    assert len(scope_log.log_records) == 1

    received_log_record = scope_log.log_records[0]

    assert received_log_record.body.string_value == test_message
    assert received_log_record.severity_text == "INFO"

    # Verify attributes from the mapper
    attrs = get_all_attributes(received_log_record.attributes)
    assert attrs.get("logger.name") == "root" # Default logger name
    assert attrs.get("request_id") == "test-req-123"

    handler.close() # Clean up

def get_attribute_value(attributes, key):
    for attr in attributes:
        if attr.key == key:
            if attr.value.HasField("string_value"): return attr.value.string_value
            if attr.value.HasField("int_value"): return attr.value.int_value
            if attr.value.HasField("double_value"): return attr.value.double_value
            if attr.value.HasField("bool_value"): return attr.value.bool_value
    return None

def get_all_attributes(attributes):
    return {attr.key: get_attribute_value([attr], attr.key) for attr in attributes}
