import logging


class Logger:
    def __init__(self, name: str):
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.DEBUG)

        # Create console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # Create formatter and add it to the handlers
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        ch.setFormatter(formatter)

        # Add the handlers to the logger
        self._logger.addHandler(ch)

    def get_logger(self):
        """
        Returns the logger instance.
        """
        return self._logger

    def log_debug(self, data: str, message: str = ""):
        """
        Log a debug message.

        :param data: The data to log.
        :param message: Optional message to log alongside the data.
        """
        if message:
            self._logger.debug(f"{message}: {data}")
        else:
            self._logger.debug(data)

    def log_info(self, data: str):
        """
        Log an info message.

        :param data: The message to log.
        """
        self._logger.info(data)

    def log_error(self, error: Exception):
        """
        Log an error message.
        :param error: The exception to log.
        """
        self._logger.error(f"An error occurred: {error}")
