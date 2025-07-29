from .base import FormatterBase
from .color import Color
from .style import Style

class TerminalFormatter(FormatterBase):
    """
    Formats text with ANSI color and style codes.
    """

    def __init__(self, color: str = "white", style: str = "normal"):
        self.color = color
        self.style = style

    def format(self, text: str) -> str:
        color_code = Color.get_code(self.color)
        style_code = Style.get_code(self.style)
        return f"\033[{style_code};{color_code}m{text}\033[0m"
