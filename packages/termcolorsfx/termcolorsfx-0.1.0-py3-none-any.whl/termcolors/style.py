class Style:
    STYLES = {
        "bold": "1",
        "underline": "4",
        "reverse": "7",
        "normal": "0"
    }

    @staticmethod
    def get_code(style: str) -> str:
        return Style.STYLES.get(style, "0")
