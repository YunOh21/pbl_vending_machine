import logging


class LoggerManager:
    PROJECT_NAME = "vending_machine"
    _loggers = {}

    @classmethod
    def get_logger(cls):
        logger_name = f"{cls.PROJECT_NAME}"

        if logger_name not in cls._loggers:
            logger = logging.getLogger(logger_name)

            logger.setLevel(logging.DEBUG)
            logger.propagate = False

            if not logger.handlers:
                handler = logging.StreamHandler()
                formatter = logging.Formatter(
                    "%(asctime)s [%(levelname)-5s] [%(name)s] %(module)-16s - %(message)s"
                )
                handler.setFormatter(formatter)
                logger.addHandler(handler)

            cls._loggers[logger_name] = logger

        return cls._loggers[logger_name]
