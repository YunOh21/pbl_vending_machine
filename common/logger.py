import logging


class LoggerManager:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not LoggerManager._initialized:
            self.PROJECT_NAME = "vending_machine"
            self._setup_logger()
            LoggerManager._initialized = True

    def _setup_logger(self):
        logger_name = f"{self.PROJECT_NAME}"
        self.logger = logging.getLogger(logger_name)

        if not self.logger.handlers:
            self.logger.setLevel(logging.DEBUG)
            self.logger.propagate = False

            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s [%(levelname)-5s] [%(name)s] %(module)-16s - %(message)s"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def get_logger(self):
        return self.logger
