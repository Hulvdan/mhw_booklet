import structlog

from .config import LOG_LEVEL

structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.TimeStamper(fmt='%Y-%m-%d %H:%M:%S'),
        structlog.dev.set_exc_info,
        structlog.processors.format_exc_info,
        structlog.dev.ConsoleRenderer(),
    ],
    context_class=dict,
    wrapper_class=structlog.make_filtering_bound_logger(LOG_LEVEL),
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=True
)
