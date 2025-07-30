import logging
from colorama import Fore, Style, init
from datetime import datetime

init(autoreset=True)

class Logita:
    """
    A logging class that outputs colored messages to the console and optionally logs them to a file.

    Attributes:
        print_to_console (bool): Determines if messages should be printed to the console.
        logger (logging.Logger): Internal logger instance for file logging.
    """

    def __init__(self, log_to_file=False, log_filename="app.log", print_to_console=True):
        """
        Initializes the Loggy instance.

        Args:
            log_to_file (bool): Enables logging to a file if True.
            log_filename (str): The filename for storing log messages.
            print_to_console (bool): Enables printing messages to the console if True.
        """
        self.print_to_console = print_to_console
        self.logger = logging.getLogger("Loggy")
        self.logger.setLevel(logging.DEBUG)

        if log_to_file:
            file_handler = logging.FileHandler(log_filename)
            file_handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def _log(self, level, message):
        """
        Private method to log a message with a given level.

        Args:
            level (str): The log level (info, success, error, warning, debug, critical, exception).
            message (str): The message to log.
        """
        current_time = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

        color_dict = {
            "info": Fore.BLUE,
            "success": Fore.GREEN,
            "error": Fore.RED,
            "warning": Fore.YELLOW,
            "debug": Fore.CYAN,
            "critical": Fore.MAGENTA,
            "exception": Fore.WHITE + Style.BRIGHT,
        }

        color = color_dict.get(level, Fore.WHITE)

        # Print colored message to console if enabled
        if self.print_to_console:
            print(f"{current_time} {color}{message}{Style.RESET_ALL}")

        # Log message to file if handlers are configured
        if self.logger.hasHandlers():
            log_func = {
                "info": self.logger.info,
                "success": self.logger.info,
                "error": self.logger.error,
                "warning": self.logger.warning,
                "debug": self.logger.debug,
                "critical": self.logger.critical,
                "exception": self.logger.exception,
            }.get(level, self.logger.info)
            log_func(message)

    def info(self, message):
        """Logs a message with level INFO."""
        self._log("info", message)

    def success(self, message):
        """Logs a message with level SUCCESS (alias for INFO)."""
        self._log("success", message)

    def error(self, message):
        """Logs a message with level ERROR."""
        self._log("error", message)

    def warning(self, message):
        """Logs a message with level WARNING."""
        self._log("warning", message)

    def debug(self, message):
        """Logs a message with level DEBUG."""
        self._log("debug", message)

    def critical(self, message):
        """Logs a message with level CRITICAL."""
        self._log("critical", message)

    def exception(self, message):
        """Logs a message with level EXCEPTION."""
        self._log("exception", message)

    def set_log_level(self, level):
        """
        Dynamically sets the logging level.

        Args:
            level (str): Desired log level ('debug', 'info', 'warning', 'error', 'critical').
        """
        level_dict = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warning": logging.WARNING,
            "error": logging.ERROR,
            "critical": logging.CRITICAL
        }
        self.logger.setLevel(level_dict.get(level, logging.DEBUG))
