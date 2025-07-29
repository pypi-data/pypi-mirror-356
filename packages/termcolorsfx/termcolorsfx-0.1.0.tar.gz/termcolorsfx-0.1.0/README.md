# termcolors

Advanced terminal formatting library with class-based structure and logger integration.

## Example

```python
from termcolors import TerminalFormatter, ColorLogger

fmt = TerminalFormatter(color="green", style="bold")
print(fmt.format("Success"))

logger = ColorLogger()
logger.info("Info message")
logger.warning("Warning!")
logger.error("Something went wrong")
