from termcolors.formatter import TerminalFormatter

def test_formatter_basic():
    fmt = TerminalFormatter("green", "bold")
    result = fmt.format("Hello")
    assert "\033[1;32mHello\033[0m" == result
