import logging
from .formatter import TerminalFormatter

class ColorLogger:
    """
    Custom logger with color support.
    """

    def __init__(self, name: str = "ColorLogger"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(ch)

    def info(self, message: str):
        colored = TerminalFormatter(color="cyan", style="bold").format(message)
        self.logger.info(colored)

    def warning(self, message: str):
        colored = TerminalFormatter(color="yellow", style="bold").format(message)
        self.logger.warning(colored)

    def error(self, message: str):
        colored = TerminalFormatter(color="red", style="bold").format(message)
        self.logger.error(colored)
