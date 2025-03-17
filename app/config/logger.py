import logging
import os
from logging.handlers import RotatingFileHandler

# Ensure logs directory exists
if not os.path.exists("logs"):
    os.makedirs("logs")

class LineCountRotatingHandler(logging.FileHandler):
    def __init__(self, filename, max_lines=500, mode='a', encoding=None, delay=False):
        super().__init__(filename, mode, encoding, delay)
        self.max_lines = max_lines
        self.line_count = 0
        self._check_existing_lines()

    def _check_existing_lines(self):
        """Count existing lines if appending to a file."""
        try:
            with open(self.baseFilename, 'r', encoding='utf-8') as f:
                self.line_count = sum(1 for _ in f)
        except FileNotFoundError:
            self.line_count = 0

    def emit(self, record):
        """Write log and rotate if max lines exceeded."""
        if self.line_count >= self.max_lines:
            self.rotate_log()
        super().emit(record)
        self.line_count += 1

    def rotate_log(self):
        """Refresh log file by overwriting."""
        self.close()
        with open(self.baseFilename, 'w', encoding='utf-8') as f:
            f.truncate(0)
        self.line_count = 0

# Configure logging
log_file = "logs/app.log"
handler = LineCountRotatingHandler(log_file, max_lines=500)

logging.basicConfig(
    handlers=[handler],
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Example Usage
for i in range(520):  # Simulating logs beyond 500 lines
    logger.info(f"Log entry {i+1}")

print("Logging complete.")
