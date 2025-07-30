import logging
import time
import traceback  # For handling exc_info without a formatter_func

from opentelemetry.proto.common.v1 import common_pb2
from opentelemetry.proto.logs.v1 import logs_pb2 as otel_logs_pb2

OTEL_SEVERITY_MAP = {
    logging.DEBUG: otel_logs_pb2.SeverityNumber.SEVERITY_NUMBER_DEBUG,
    logging.INFO: otel_logs_pb2.SeverityNumber.SEVERITY_NUMBER_INFO,
    logging.WARNING: otel_logs_pb2.SeverityNumber.SEVERITY_NUMBER_WARN,
    logging.ERROR: otel_logs_pb2.SeverityNumber.SEVERITY_NUMBER_ERROR,
    logging.CRITICAL: otel_logs_pb2.SeverityNumber.SEVERITY_NUMBER_FATAL,
}

_RESERVED_ATTRIBUTES = frozenset({
    "name",
    "msg",
    "args",
    "levelname",
    "levelno",
    "pathname",
    "filename",
    "lineno",
    "funcName",
    "created",
    "asctime",
    "msecs",
    "relativeCreated",
    "thread",
    "threadName",
    "processName",
    "process",
    "exc_info",
    "exc_text",
    "stack_info",
    "_asctime",
    "message",
    "stack_info",
})

def convert_log_record(
    record: logging.LogRecord, formatter_func=None, reserved_attributes=_RESERVED_ATTRIBUTES
) -> otel_logs_pb2.LogRecord:
    """
    Converts a Python LogRecord to an OTLP LogRecord protobuf message.
    formatter_func (callable, optional): A function that takes a LogRecord
                                         and returns a formatted string, typically
                                         used for exception stacktraces. If not
                                         provided, `traceback.format_exc()` is used
                                         for `exc_info`.

    See also: LoggingHandler._translate in opentelemetry-sdk
    (https://github.com/open-telemetry/opentelemetry-python/blob/36ac612f263f224665865e2ecc692f3c32a66a23/opentelemetry-sdk/src/opentelemetry/sdk/_logs/_internal/__init__.py#L512)
    """
    log_attributes = []

    # Map standard LogRecord attributes to OTLP attributes
    # You might want to be more selective here based on what's truly useful in OTLP
    log_attributes.append(
        common_pb2.KeyValue(
            key="logger.name", value=common_pb2.AnyValue(string_value=record.name)
        )
    )
    log_attributes.append(
        common_pb2.KeyValue(
            key="code.filepath", value=common_pb2.AnyValue(string_value=record.pathname)
        )
    )
    log_attributes.append(
        common_pb2.KeyValue(
            key="code.filename", value=common_pb2.AnyValue(string_value=record.filename)
        )
    )
    log_attributes.append(
        common_pb2.KeyValue(
            key="code.lineno", value=common_pb2.AnyValue(int_value=record.lineno)
        )
    )
    log_attributes.append(
        common_pb2.KeyValue(
            key="code.function", value=common_pb2.AnyValue(string_value=record.funcName)
        )
    )
    log_attributes.append(
        common_pb2.KeyValue(
            key="process.pid", value=common_pb2.AnyValue(int_value=record.process)
        )
    )
    log_attributes.append(
        common_pb2.KeyValue(
            key="thread.id", value=common_pb2.AnyValue(int_value=record.thread)
        )
    )
    if record.threadName:  # threadName might be empty string
        log_attributes.append(
            common_pb2.KeyValue(
                key="thread.name",
                value=common_pb2.AnyValue(string_value=record.threadName),
            )
        )
    if record.processName:
        log_attributes.append(
            common_pb2.KeyValue(
                key="process.name",
                value=common_pb2.AnyValue(string_value=record.processName),
            )
        )

    # Add `extra` attributes from LogRecord.__dict__
    for key, value in record.__dict__.items():
        # Exclude standard LogRecord internal/known fields and those already mapped
        if key in reserved_attributes or key.startswith("_"):
            continue

        # Convert value to common_pb2.AnyValue based on type
        if isinstance(value, str):
            log_attributes.append(
                common_pb2.KeyValue(
                    key=key, value=common_pb2.AnyValue(string_value=value)
                )
            )
        elif isinstance(value, int):
            log_attributes.append(
                common_pb2.KeyValue(key=key, value=common_pb2.AnyValue(int_value=value))
            )
        elif isinstance(value, float):
            log_attributes.append(
                common_pb2.KeyValue(
                    key=key, value=common_pb2.AnyValue(double_value=value)
                )
            )
        elif isinstance(value, bool):
            log_attributes.append(
                common_pb2.KeyValue(
                    key=key, value=common_pb2.AnyValue(bool_value=value)
                )
            )
        elif isinstance(value, (list, tuple)):
            array_values = [
                common_pb2.AnyValue(string_value=str(item)) for item in value
            ]  # Simplify list to string for now
            log_attributes.append(
                common_pb2.KeyValue(
                    key=key,
                    value=common_pb2.AnyValue(
                        array_value=common_pb2.ArrayValue(values=array_values)
                    ),
                )
            )
        elif isinstance(value, dict):
            kvlist = [
                common_pb2.KeyValue(
                    key=k, value=common_pb2.AnyValue(string_value=str(v))
                )
                for k, v in value.items()
            ]  # Simplify dict to string for now
            log_attributes.append(
                common_pb2.KeyValue(
                    key=key,
                    value=common_pb2.AnyValue(
                        kvlist_value=common_pb2.KeyValueList(values=kvlist)
                    ),
                )
            )
        else:
            # Fallback for unhandled types, serialize to string
            log_attributes.append(
                common_pb2.KeyValue(
                    key=key, value=common_pb2.AnyValue(string_value=str(value))
                )
            )

    # Handle exception information
    if record.exc_info:
        exc_type = record.exc_info[0].__name__ if record.exc_info[0] else "UnknownError"
        exc_message = str(record.exc_info[1]) if record.exc_info[1] else ""
        stacktrace_str = ""
        if formatter_func:
            # Use the provided formatter (e.g., logging.Formatter.format for full stack)
            temp_record = logging.LogRecord(
                name=record.name,
                level=record.levelno,
                pathname=record.pathname,
                lineno=record.lineno,
                msg=record.msg,
                args=record.args,
                exc_info=record.exc_info,
            )
            stacktrace_str = formatter_func(temp_record)
        elif record.exc_text:  # Pre-formatted exception text if available
            stacktrace_str = record.exc_text
        else:  # Fallback to standard traceback formatting
            stacktrace_str = "".join(traceback.format_exception(*record.exc_info))

        log_attributes.append(
            common_pb2.KeyValue(
                key="exception.type", value=common_pb2.AnyValue(string_value=exc_type)
            )
        )
        log_attributes.append(
            common_pb2.KeyValue(
                key="exception.message",
                value=common_pb2.AnyValue(string_value=exc_message),
            )
        )
        log_attributes.append(
            common_pb2.KeyValue(
                key="exception.stacktrace",
                value=common_pb2.AnyValue(string_value=stacktrace_str),
            )
        )
    elif record.stack_info:  # Python 3.2+ for stack_info
        log_attributes.append(
            common_pb2.KeyValue(
                key="stacktrace",
                value=common_pb2.AnyValue(string_value=record.stack_info),
            )
        )

    return otel_logs_pb2.LogRecord(
        time_unix_nano=int(record.created * 1e9),  # Unix timestamp in nanoseconds
        observed_time_unix_nano=int(
            time.time() * 1e9
        ),  # Time when the log was observed by the system
        severity_number=OTEL_SEVERITY_MAP.get(
            record.levelno, otel_logs_pb2.SeverityNumber.SEVERITY_NUMBER_UNSPECIFIED
        ),
        severity_text=record.levelname,
        body=common_pb2.AnyValue(
            string_value=record.getMessage()
        ),  # Formatted log message
        attributes=log_attributes,
        dropped_attributes_count=0,
        flags=0,
    )
