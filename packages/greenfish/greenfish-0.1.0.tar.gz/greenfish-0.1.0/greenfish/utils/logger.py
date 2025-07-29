from colorama import init, Fore, Back, Style
import datetime

# Initialize colorama
init()

class Logger:
    """Utility class for colorful console logging."""

    @staticmethod
    def info(message: str) -> None:
        """Log an info message in blue."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{Fore.BLUE}[INFO]{Style.RESET_ALL} {timestamp} - {message}")

    @staticmethod
    def success(message: str) -> None:
        """Log a success message in green."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} {timestamp} - {message}")

    @staticmethod
    def warning(message: str) -> None:
        """Log a warning message in yellow."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} {timestamp} - {message}")

    @staticmethod
    def error(message: str) -> None:
        """Log an error message in red."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {timestamp} - {message}")

    @staticmethod
    def debug(message: str) -> None:
        """Log a debug message in cyan."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{Fore.CYAN}[DEBUG]{Style.RESET_ALL} {timestamp} - {message}")

# Create a global logger instance
logger = Logger()
