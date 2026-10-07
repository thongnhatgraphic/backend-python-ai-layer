                                    Logging
                                    ↓
                                    structured logging
                                    ↓
                                    observability

Logging cho phép bạn có:
    timestamp
    level
    logger name
    message
    exception
    metadata

Ví dụ:
2026-09-17 11:02:15 ERROR tool_executor
Tool validation failed
tool=calculate_sum

1. Các log level cơ bản:
- DEBUG:
        - Thông tin phục vụ developer debug.
        - logger.debug("Tool arguments received")
- INFO
        - logger.info("Tool execution started")
- WARNING
        - logger.warning("Tool retrying")
- ERROR
        - logger.error("Tool execution failed")


