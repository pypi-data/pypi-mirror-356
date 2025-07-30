# otel-log-proto-mapper

A Python library designed to facilitate the conversion of standard `logging.LogRecord` objects into OpenTelemetry Protocol (OTLP) Log Protobuf messages. This library provides a decoupled mapping function, enabling flexible integration into custom logging solutions without requiring the full OpenTelemetry SDK.

## Features

- Converts `logging.LogRecord` attributes (message, level, `extra` data, exception info) into OTLP Log Protobuf fields.
- Supports mapping of common Python types to OTLP `AnyValue`.
- Provides an `OTEL_SEVERITY_MAP` for standard logging levels.

## Installation

```bash
pip install otel-log-proto-mapper
```

## Usage

```python
import logging
from otel_log_proto_mapper import convert_log_record, OTEL_SEVERITY_MAP
# Assuming you also have opentelemetry-proto installed for type hints and protobuf classes
from opentelemetry.proto.logs.v1 import logs_pb2 as otel_logs_pb2

# Create a dummy LogRecord
logger = logging.getLogger("my_app")
logger.setLevel(logging.INFO)
record = logging.LogRecord(
    name=logger.name,
    level=logging.INFO,
    pathname="/app/main.py",
    lineno=42,
    func="do_work",
    msg="Processing data",
    args=(),
    exc_info=None,
    created=time.time(),
)
record.user_id = "user123" # Example of an 'extra' attribute

# Convert to OTLP LogRecord
otel_log_record = convert_log_record(record)

print(f"OTLP Severity: {otel_log_record.severity_text} ({otel_log_record.severity_number})")
print(f"OTLP Body: {otel_log_record.body.string_value}")
print("OTLP Attributes:")
for attr in otel_log_record.attributes:
    print(f"  {attr.key}: {attr.value}")

# Example with exception
try:
    raise ValueError("Something went wrong!")
except ValueError:
    exc_record = logging.LogRecord(
        name=logger.name,
        level=logging.ERROR,
        pathname="/app/main.py",
        lineno=50,
        func="handle_error",
        msg="An error occurred",
        args=(),
        exc_info=sys.exc_info(),
        created=time.time(),
    )
    # When using convert_log_record, you typically pass a formatter for full traceback
    # like handler.format in the OTLPGrpcLogHandler context.
    # For standalone test, you can rely on converter's internal traceback formatting.
    otel_exc_log_record = convert_log_record(exc_record)
    print("\nOTLP Exception Log:")
    for attr in otel_exc_log_record.attributes:
        if attr.key.startswith("exception."):
            print(f"  {attr.key}: {attr.value}")
```
