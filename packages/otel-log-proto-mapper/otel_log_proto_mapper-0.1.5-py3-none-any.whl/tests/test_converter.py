import logging
import time
import sys


from otel_log_proto_mapper.converter import convert_log_record, OTEL_SEVERITY_MAP


# Helper to create a dummy LogRecord
def create_log_record(level, message, exc_info=None, extra=None):
    record = logging.LogRecord(
        name="test_logger",
        level=level,
        pathname="/path/to/test.py",
        lineno=10,
        func="test_func",
        msg=message,
        args=(),
        exc_info=exc_info,
    )
    # Simulate creation time for accurate timestamps
    record.created = time.time()
    if extra:
        for key, value in extra.items():
            setattr(record, key, value)
    return record


def get_attribute_value(attributes, key):
    for attr in attributes:
        if attr.key == key:
            if attr.value.HasField("string_value"):
                return attr.value.string_value

            if attr.value.HasField("int_value"):
                return attr.value.int_value

            if attr.value.HasField("double_value"):
                return attr.value.double_value

            if attr.value.HasField("bool_value"):
                return attr.value.bool_value

            if attr.value.HasField("array_value"):
                return [v.string_value for v in attr.value.array_value.values]

            if attr.value.HasField("kvlist_value"):
                return {
                    kv.key: kv.value.string_value
                    for kv in attr.value.kvlist_value.values
                }

    return None


def get_all_attributes(attributes):
    return {attr.key: get_attribute_value([attr], attr.key) for attr in attributes}


def test_basic_info_log_conversion():
    record = create_log_record(logging.INFO, "Hello, OTLP!")
    otel_log = convert_log_record(record)

    assert otel_log.severity_number == OTEL_SEVERITY_MAP[logging.INFO]
    assert otel_log.severity_text == "INFO"
    assert otel_log.body.string_value == "Hello, OTLP!"
    assert otel_log.time_unix_nano > 0

    attrs = get_all_attributes(otel_log.attributes)
    assert attrs.get("logger.name") == "test_logger"
    assert attrs.get("code.lineno") == 10
    assert attrs.get("code.function") == "test_func"


def test_log_with_extra_attributes():
    extra_data = {
        "user_id": 123,
        "session_id": "abc-xyz",
        "is_admin": True,
        "latency_ms": 50.5,
    }
    record = create_log_record(logging.WARNING, "User action.", extra=extra_data)
    otel_log = convert_log_record(record)

    attrs = get_all_attributes(otel_log.attributes)
    assert attrs.get("user_id") == 123
    assert attrs.get("session_id") == "abc-xyz"
    assert attrs.get("is_admin") == 1
    assert attrs.get("latency_ms") == 50.5
    assert otel_log.severity_number == OTEL_SEVERITY_MAP[logging.WARNING]


def test_log_with_exception_info():
    try:
        1 / 0
    except ZeroDivisionError:
        record = create_log_record(
            logging.ERROR, "Division by zero!", exc_info=sys.exc_info()
        )

    otel_log = convert_log_record(
        record, formatter_func=lambda r: "FORMATTED_TRACEBACK_HERE"
    )

    attrs = get_all_attributes(otel_log.attributes)
    assert attrs.get("exception.type") == "ZeroDivisionError"
    assert "division by zero" in attrs.get("exception.message")
    assert attrs.get("exception.stacktrace") == "FORMATTED_TRACEBACK_HERE"
    assert otel_log.severity_number == OTEL_SEVERITY_MAP[logging.ERROR]


def test_log_with_unhandled_extra_type():
    extra_data = {"unique_ids": {1, 2, 3}}
    record = create_log_record(logging.INFO, "Complex object.", extra=extra_data)
    otel_log = convert_log_record(record)
    attrs = get_all_attributes(otel_log.attributes)
    # Verify unique_ids is converted to string if specific mapping not implemented
    assert attrs.get("unique_ids") == "{1, 2, 3}"


def test_log_with_list_extra():
    extra_data = {"ids": [1, 2, 3]}
    record = create_log_record(logging.INFO, "List data.", extra=extra_data)
    otel_log = convert_log_record(record)
    attrs = get_all_attributes(otel_log.attributes)
    assert attrs.get("ids") == ["1", "2", "3"]  # Simplified string conversion
