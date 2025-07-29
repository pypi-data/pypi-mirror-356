"""Remote Console viewers implementation."""
from typing import Dict, Any, Optional, List, Callable
import os
import sys
import time
import subprocess
import tempfile
import platform
import threading
import queue
import webbrowser

from greenfish.utils.logger import Logger
from greenfish.core.remoteconsole.types import ConsoleType, ConsoleState

class ConsoleViewer:
    """Base class for console viewers."""

    def __init__(self, url: str = None):
        """Initialize console viewer.

        Args:
            url: Console URL
        """
        self.url = url
        self.process = None
        self.running = False
        self.send_callback = None

    def launch(self) -> bool:
        """Launch console viewer.

        Returns:
            bool: True if successful
        """
        raise NotImplementedError("Subclasses must implement launch()")

    def close(self) -> bool:
        """Close console viewer.

        Returns:
            bool: True if successful
        """
        self.running = False

        if self.process:
            try:
                self.process.terminate()
                try:
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.process.kill()
            except Exception as e:
                Logger.error(f"Error closing console viewer: {str(e)}")
                return False

        return True

    def send_keystrokes(self, keystrokes: str) -> bool:
        """Send keystrokes to console.

        Args:
            keystrokes: Keystrokes to send

        Returns:
            bool: True if successful
        """
        if self.send_callback:
            try:
                self.send_callback(keystrokes)
                return True
            except Exception as e:
                Logger.error(f"Error sending keystrokes: {str(e)}")

        return False

    def send_special_key(self, key: str) -> bool:
        """Send special key to console.

        Args:
            key: Special key

        Returns:
            bool: True if successful
        """
        return False

    def set_send_callback(self, callback: Callable) -> None:
        """Set send data callback.

        Args:
            callback: Callback function
        """
        self.send_callback = callback

    def receive_data(self, data: bytes) -> None:
        """Receive data from console.

        Args:
            data: Data received
        """
        pass


class KVMViewer(ConsoleViewer):
    """KVM console viewer."""

    def __init__(self, url: str = None):
        """Initialize KVM viewer.

        Args:
            url: Console URL
        """
        super().__init__(url)
        self.window_title = "KVM Console"
        self.plugin_type = None
        self.plugin_path = None

    def launch(self) -> bool:
        """Launch KVM viewer.

        Returns:
            bool: True if successful
        """
        try:
            if not self.url:
                Logger.error("No URL provided for KVM viewer")
                return False

            # Check if URL requires Java plugin
            if "jnlp" in self.url.lower() or "javaws" in self.url.lower():
                # Java Web Start URL
                self.plugin_type = "Java"
                return self._launch_java_viewer()
            elif "html5" in self.url.lower() or "webkvm" in self.url.lower():
                # HTML5 viewer
                self.plugin_type = "HTML5"
                return self._launch_browser_viewer()
            else:
                # Default to browser
                return self._launch_browser_viewer()

        except Exception as e:
            Logger.error(f"Error launching KVM viewer: {str(e)}")
            return False

    def _launch_browser_viewer(self) -> bool:
        """Launch browser-based viewer.

        Returns:
            bool: True if successful
        """
        try:
            # Open URL in browser
            webbrowser.open(self.url)
            self.running = True
            return True

        except Exception as e:
            Logger.error(f"Error launching browser viewer: {str(e)}")
            return False

    def _launch_java_viewer(self) -> bool:
        """Launch Java-based viewer.

        Returns:
            bool: True if successful
        """
        try:
            # Check if Java is installed
            try:
                java_process = subprocess.run(
                    ["java", "-version"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                if java_process.returncode != 0:
                    Logger.error("Java is not installed or not in PATH")
                    return False
            except Exception:
                Logger.error("Java is not installed or not in PATH")
                return False

            # Check if javaws is available
            javaws_cmd = "javaws"
            if platform.system() == "Windows":
                # Try to find javaws in common locations
                java_home = os.environ.get("JAVA_HOME")
                if java_home:
                    javaws_path = os.path.join(java_home, "bin", "javaws.exe")
                    if os.path.exists(javaws_path):
                        javaws_cmd = javaws_path

            # If URL is direct JNLP, launch it
            if self.url.lower().endswith(".jnlp"):
                self.process = subprocess.Popen([javaws_cmd, self.url])
                self.running = True
                return True

            # If URL is a web page, download JNLP file
            import requests
            response = requests.get(self.url)

            # Check if response is JNLP content
            content_type = response.headers.get("Content-Type", "")
            if "application/x-java-jnlp-file" in content_type:
                # Save JNLP content to temporary file
                with tempfile.NamedTemporaryFile(suffix=".jnlp", delete=False) as temp:
                    temp_path = temp.name
                    temp.write(response.content)

                try:
                    # Launch JNLP file
                    self.process = subprocess.Popen([javaws_cmd, temp_path])
                    self.running = True
                    return True
                finally:
                    # Clean up temporary file
                    try:
                        os.unlink(temp_path)
                    except:
                        pass
            else:
                # Not a JNLP file, try browser instead
                return self._launch_browser_viewer()

        except Exception as e:
            Logger.error(f"Error launching Java viewer: {str(e)}")
            return False


class SerialViewer(ConsoleViewer):
    """Serial console viewer."""

    def __init__(self, url: str = None):
        """Initialize Serial viewer.

        Args:
            url: Console URL
        """
        super().__init__(url)
        self.window_title = "Serial Console"
        self.data_queue = queue.Queue()
        self.reader_thread = None
        self.writer_thread = None
        self.terminal_process = None

    def launch(self) -> bool:
        """Launch Serial viewer.

        Returns:
            bool: True if successful
        """
        try:
            if self.url:
                # Web-based serial console
                return self._launch_browser_viewer()
            else:
                # Terminal-based serial console
                return self._launch_terminal_viewer()

        except Exception as e:
            Logger.error(f"Error launching Serial viewer: {str(e)}")
            return False

    def _launch_browser_viewer(self) -> bool:
        """Launch browser-based viewer.

        Returns:
            bool: True if successful
        """
        try:
            # Open URL in browser
            webbrowser.open(self.url)
            self.running = True
            return True

        except Exception as e:
            Logger.error(f"Error launching browser viewer: {str(e)}")
            return False

    def _launch_terminal_viewer(self) -> bool:
        """Launch terminal-based viewer.

        Returns:
            bool: True if successful
        """
        try:
            # Determine terminal application based on platform
            if platform.system() == "Windows":
                # Use PowerShell or Command Prompt
                terminal_cmd = ["powershell.exe"]
            elif platform.system() == "Darwin":
                # macOS Terminal
                terminal_cmd = ["open", "-a", "Terminal"]
            else:
                # Linux - try common terminals
                for term in ["gnome-terminal", "xterm", "konsole", "terminator"]:
                    try:
                        subprocess.run(["which", term], stdout=subprocess.PIPE, check=True)
                        terminal_cmd = [term]
                        break
                    except subprocess.CalledProcessError:
                        continue
                else:
                    terminal_cmd = ["xterm"]  # Default to xterm

            # For now, we'll use a simple approach - just launch the terminal
            # In a real implementation, you'd need to handle I/O between the SOL session and terminal
            self.process = subprocess.Popen(terminal_cmd)
            self.running = True

            # Start reader and writer threads
            self._start_reader_thread()
            self._start_writer_thread()

            return True

        except Exception as e:
            Logger.error(f"Error launching terminal viewer: {str(e)}")
            return False

    def _start_reader_thread(self) -> None:
        """Start reader thread for handling incoming data."""
        def reader_loop():
            try:
                while self.running:
                    try:
                        # Get data from queue with timeout
                        data = self.data_queue.get(timeout=0.1)

                        # Process and display data
                        self._display_data(data)

                        # Mark task as done
                        self.data_queue.task_done()
                    except queue.Empty:
                        # No data available, continue
                        continue
            except Exception as e:
                Logger.error(f"Error in serial reader thread: {str(e)}")

        self.reader_thread = threading.Thread(target=reader_loop)
        self.reader_thread.daemon = True
        self.reader_thread.start()

    def _start_writer_thread(self) -> None:
        """Start writer thread for handling user input."""
        # In a real implementation, this would read from the terminal
        # and send data using the send_callback
        pass

    def _display_data(self, data: bytes) -> None:
        """Display data in terminal.

        Args:
            data: Data to display
        """
        # In a real implementation, this would write to the terminal
        # For now, we'll just print to stdout for demonstration
        try:
            if isinstance(data, bytes):
                sys.stdout.buffer.write(data)
                sys.stdout.buffer.flush()
            else:
                sys.stdout.write(data)
                sys.stdout.flush()
        except Exception as e:
            Logger.error(f"Error displaying data: {str(e)}")

    def receive_data(self, data: bytes) -> None:
        """Receive data from console.

        Args:
            data: Data received
        """
        try:
            # Add data to queue for processing by reader thread
            self.data_queue.put(data)
        except Exception as e:
            Logger.error(f"Error receiving data: {str(e)}")

    def close(self) -> bool:
        """Close console viewer.

        Returns:
            bool: True if successful
        """
        self.running = False

        # Wait for threads to terminate
        if self.reader_thread and self.reader_thread.is_alive():
            self.reader_thread.join(timeout=2)

        if self.writer_thread and self.writer_thread.is_alive():
            self.writer_thread.join(timeout=2)

        # Close process
        return super().close()

    def send_keystrokes(self, keystrokes: str) -> bool:
        """Send keystrokes to console.

        Args:
            keystrokes: Keystrokes to send

        Returns:
            bool: True if successful
        """
        if self.send_callback:
            try:
                self.send_callback(keystrokes)
                return True
            except Exception as e:
                Logger.error(f"Error sending keystrokes: {str(e)}")

        return False

    def send_special_key(self, key: str) -> bool:
        """Send special key to console.

        Args:
            key: Special key

        Returns:
            bool: True if successful
        """
        # Map special keys to escape sequences
        key_map = {
            "CTRL+C": "\x03",
            "CTRL+D": "\x04",
            "CTRL+Z": "\x1A",
            "ESC": "\x1B",
            "ENTER": "\r",
            "BACKSPACE": "\x08"
        }

        if key in key_map and self.send_callback:
            try:
                self.send_callback(key_map[key])
                return True
            except Exception as e:
                Logger.error(f"Error sending special key: {str(e)}")

        return False
