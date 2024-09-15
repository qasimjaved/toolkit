import logging
import logging.config

# Global logsuffix which can be dynamically modified if needed
logsuffix = []

LOGGING_DEFAULT = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'class': 'logging.Formatter',
            'format': '[%(asctime)s > %(module)s:%(lineno)d %(levelname)s]:%(message)s',
            'datefmt': '%m/%d/%Y %I:%M:%S %p',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'standard',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}


class SuffixAdder(logging.LoggerAdapter):
    """
    Logger adapter to add suffix information to log messages.
    """

    def __init__(self, logger, extra_suffix=None):
        """
        Initialize the SuffixAdder adapter.

        :param logger: The logger instance to be wrapped.
        :param extra_suffix: Optional list of suffixes to append to each log message.
        """
        super(SuffixAdder, self).__init__(logger, {})
        self.extra_suffix = extra_suffix if extra_suffix else []

    def process(self, msg, kwargs):
        """
        Process the log message and add suffixes if provided.

        :param msg: Original log message.
        :param kwargs: Additional arguments for logging.
        :return: Modified message with suffixes appended.
        """
        # Add global logsuffix and any local suffix from kwargs
        combined_suffix = self.extra_suffix + logsuffix + kwargs.pop("suffix", [])

        # Append suffixes to the log message
        if combined_suffix:
            msg = f"{msg} | {' | '.join(map(str, combined_suffix))}"

        return msg, kwargs


def get_logger(extra_suffix=None) -> SuffixAdder:
    """
    Get a logger instance wrapped with the SuffixAdder to handle suffixes.

    :param extra_suffix: Optional list of additional suffixes to be included with each log.
    :return: Logger instance wrapped in SuffixAdder.
    """
    logging.config.dictConfig(LOGGING_DEFAULT)
    logger = logging.getLogger()
    return SuffixAdder(logger, extra_suffix)


# Example usage of the logger
logger = get_logger()
