class Color:
    COLORS = {
        "black": "30", "red": "31", "green": "32",
        "yellow": "33", "blue": "34", "magenta": "35",
        "cyan": "36", "white": "37"
    }

    @staticmethod
    def get_code(color: str) -> str:
        return Color.COLORS.get(color.lower(), "37")
