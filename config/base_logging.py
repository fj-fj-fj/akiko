BASE_LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "format": "{module}: {message}",
            "datefmt": "%d/%b/%Y %H:%M:%S",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
    },
    "loggers": {
        "": {"handlers": ["console"], "level": "DEBUG",},
        "api": {"handlers": ["console"], "level": "DEBUG", "propagate": False,},
    },
}
