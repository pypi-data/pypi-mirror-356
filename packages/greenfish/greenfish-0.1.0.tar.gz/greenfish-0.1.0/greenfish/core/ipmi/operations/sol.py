"""IPMI Serial Over LAN (SOL) operations module."""
from typing import Dict, Any, List, Optional, Callable
import threading
import time
import queue

from greenfish.utils.logger import Logger

# IPMI constants
IPMI_NETFN_APP = 0x06
IPMI_NETFN_TRANSPORT = 0x0C

# SOL commands
IPMI_CMD_SOL_ACTIVATING = 0x20
IPMI_CMD_SET_SOL_CONFIG = 0x21
IPMI_CMD_GET_SOL_CONFIG = 0x22

# SOL payload commands
SOL_PAYLOAD_TYPE = 0x01
SOL_PAYLOAD_ACTIVATE = 0x01
SOL_PAYLOAD_DEACTIVATE = 0x00

# SOL configuration parameters
SOL_PARAM_SET_IN_PROGRESS = 0x00
SOL_PARAM_SOL_ENABLE = 0x01
SOL_PARAM_SOL_AUTH = 0x02
SOL_PARAM_SOL_THRESHOLD = 0x03
SOL_PARAM_SOL_RETRY = 0x04
SOL_PARAM_SOL_BITRATE = 0x05
SOL_PARAM_SOL_VOLATILE_BITRATE = 0x06
SOL_PARAM_SOL_NON_VOLATILE_BITRATE = 0x07

# SOL packet types
SOL_PACKET_SEQUENCE_NUMBER = 0x08
SOL_PACKET_ACK = 0x40
SOL_PACKET_ACCEPTED = 0x00
SOL_PACKET_NACK = 0x40
SOL_PACKET_STATUS_NACK = 0x80
SOL_PACKET_BREAK = 0x10
SOL_PACKET_DTR = 0x02
SOL_PACKET_RTS = 0x01
SOL_PACKET_FLUSH_OUTBOUND = 0x20
SOL_PACKET_FLUSH_INBOUND = 0x40

class SOLOperations:
    """IPMI SOL operations handler."""

    def __init__(self, protocol):
        """Initialize SOL operations handler.

        Args:
            protocol: IPMI protocol handler
        """
        self.protocol = protocol
        self.sol_active = False
        self.sol_sequence_number = 0
        self.sol_thread = None
        self.sol_running = False
        self.sol_data_queue = queue.Queue()
        self.sol_callback = None
        self.sol_session_info = {}

    def get_sol_config(self, channel: int = 1, parameter: int = SOL_PARAM_SOL_ENABLE) -> Dict[str, Any]:
        """Get SOL configuration.

        Args:
            channel: Channel number
            parameter: Configuration parameter

        Returns:
            Dict containing SOL configuration
        """
        request_data = bytes([
            channel,
            parameter,
            0x00,  # Set selector
            0x00   # Block selector
        ])

        response = self.protocol.send_command(IPMI_NETFN_TRANSPORT, IPMI_CMD_GET_SOL_CONFIG, request_data)

        if response['completion_code'] != 0:
            Logger.error(f"Failed to get SOL configuration: {response['completion_code']:#x}")
            return {}

        data = response['data']
        if len(data) < 2:
            Logger.error("Invalid SOL configuration response")
            return {}

        result = {
            'parameter_revision': data[0],
            'parameter': parameter,
            'data': data[1:]
        }

        # Parse specific parameters
        if parameter == SOL_PARAM_SET_IN_PROGRESS:
            result['set_in_progress'] = data[1] & 0x03
        elif parameter == SOL_PARAM_SOL_ENABLE:
            result['sol_enabled'] = bool(data[1] & 0x01)
        elif parameter == SOL_PARAM_SOL_AUTH:
            result['auth_support'] = {
                'callback': bool(data[1] & 0x01),
                'user': bool(data[1] & 0x02),
                'operator': bool(data[1] & 0x04),
                'admin': bool(data[1] & 0x08),
                'oem': bool(data[1] & 0x10)
            }
            result['force_auth'] = bool(data[1] & 0x20)
            result['force_encryption'] = bool(data[1] & 0x40)
        elif parameter == SOL_PARAM_SOL_THRESHOLD:
            result['character_threshold'] = data[1]
            result['character_send_threshold'] = data[2]
        elif parameter == SOL_PARAM_SOL_RETRY:
            result['retry_count'] = data[1]
            result['retry_interval'] = data[2]
        elif parameter == SOL_PARAM_SOL_BITRATE:
            bitrates = {
                0x00: 9600,
                0x01: 19200,
                0x02: 38400,
                0x03: 57600,
                0x04: 115200
            }
            result['bitrate'] = bitrates.get(data[1] & 0x0F, "unknown")

        return result

    def set_sol_config(self, channel: int = 1, parameter: int = SOL_PARAM_SOL_ENABLE, data: bytes = b'\x01') -> bool:
        """Set SOL configuration.

        Args:
            channel: Channel number
            parameter: Configuration parameter
            data: Parameter data

        Returns:
            bool: True if successful
        """
        request_data = bytes([
            channel,
            parameter,
            0x00,  # Set selector
            0x00   # Block selector
        ]) + data

        response = self.protocol.send_command(IPMI_NETFN_TRANSPORT, IPMI_CMD_SET_SOL_CONFIG, request_data)

        if response['completion_code'] != 0:
            Logger.error(f"Failed to set SOL configuration: {response['completion_code']:#x}")
            return False

        return True

    def enable_sol(self, channel: int = 1) -> bool:
        """Enable SOL.

        Args:
            channel: Channel number

        Returns:
            bool: True if successful
        """
        return self.set_sol_config(channel, SOL_PARAM_SOL_ENABLE, b'\x01')

    def disable_sol(self, channel: int = 1) -> bool:
        """Disable SOL.

        Args:
            channel: Channel number

        Returns:
            bool: True if successful
        """
        return self.set_sol_config(channel, SOL_PARAM_SOL_ENABLE, b'\x00')

    def set_sol_bitrate(self, channel: int = 1, bitrate: int = 4) -> bool:
        """Set SOL bit rate.

        Args:
            channel: Channel number
            bitrate: Bit rate code (0=9600, 1=19200, 2=38400, 3=57600, 4=115200)

        Returns:
            bool: True if successful
        """
        if bitrate < 0 or bitrate > 4:
            Logger.error(f"Invalid SOL bit rate: {bitrate}")
            return False

        return self.set_sol_config(channel, SOL_PARAM_SOL_BITRATE, bytes([bitrate]))

    def activate_sol(self, payload_instance: int = 1) -> bool:
        """Activate SOL session.

        Args:
            payload_instance: Payload instance

        Returns:
            bool: True if successful
        """
        if self.sol_active:
            Logger.warning("SOL session already active")
            return True

        # Activate SOL payload
        request_data = bytes([
            payload_instance,  # Payload instance
            SOL_PAYLOAD_TYPE,  # Payload type (SOL)
            SOL_PAYLOAD_ACTIVATE,  # Activate
            0x00,  # Authentication (use session info)
            0x00,  # Encryption (use session info)
            0x00,  # Reserved
        ])

        response = self.protocol.send_command(IPMI_NETFN_APP, IPMI_CMD_SOL_ACTIVATING, request_data)

        if response['completion_code'] != 0:
            Logger.error(f"Failed to activate SOL: {response['completion_code']:#x}")
            return False

        data = response['data']
        if len(data) < 4:
            Logger.error("Invalid SOL activation response")
            return False

        # Store SOL session info
        self.sol_session_info = {
            'inbound_seq_num': 0,
            'outbound_seq_num': 0,
            'max_packet_size': (data[1] << 8) | data[0],
            'payload_instance': payload_instance
        }

        self.sol_active = True
        Logger.info("SOL session activated")

        return True

    def deactivate_sol(self, payload_instance: int = 1) -> bool:
        """Deactivate SOL session.

        Args:
            payload_instance: Payload instance

        Returns:
            bool: True if successful
        """
        if not self.sol_active:
            Logger.warning("No active SOL session")
            return True

        # Deactivate SOL payload
        request_data = bytes([
            payload_instance,  # Payload instance
            SOL_PAYLOAD_TYPE,  # Payload type (SOL)
            SOL_PAYLOAD_DEACTIVATE,  # Deactivate
            0x00,  # Authentication (use session info)
            0x00,  # Encryption (use session info)
            0x00,  # Reserved
        ])

        response = self.protocol.send_command(IPMI_NETFN_APP, IPMI_CMD_SOL_ACTIVATING, request_data)

        if response['completion_code'] != 0:
            Logger.error(f"Failed to deactivate SOL: {response['completion_code']:#x}")
            return False

        self.sol_active = False
        Logger.info("SOL session deactivated")

        return True

    def start_sol_session(self, callback: Callable[[bytes], None]) -> bool:
        """Start SOL session with callback for received data.

        Args:
            callback: Function to call with received data

        Returns:
            bool: True if session started successfully
        """
        if self.sol_thread and self.sol_thread.is_alive():
            Logger.warning("SOL session already running")
            return False

        # Activate SOL
        if not self.activate_sol():
            return False

        # Set callback
        self.sol_callback = callback

        # Start SOL thread
        self.sol_running = True
        self.sol_thread = threading.Thread(target=self._sol_thread_func)
        self.sol_thread.daemon = True
        self.sol_thread.start()

        return True

    def stop_sol_session(self) -> bool:
        """Stop SOL session.

        Returns:
            bool: True if successful
        """
        if not self.sol_thread or not self.sol_thread.is_alive():
            Logger.warning("No active SOL session")
            return True

        # Stop SOL thread
        self.sol_running = False
        self.sol_thread.join(2.0)

        # Deactivate SOL
        return self.deactivate_sol()

    def send_sol_data(self, data: bytes) -> bool:
        """Send data over SOL.

        Args:
            data: Data to send

        Returns:
            bool: True if data was queued successfully
        """
        if not self.sol_active:
            Logger.error("No active SOL session")
            return False

        # Queue data for sending
        try:
            self.sol_data_queue.put(data)
            return True
        except Exception as e:
            Logger.error(f"Failed to queue SOL data: {str(e)}")
            return False

    def send_sol_break(self) -> bool:
        """Send break over SOL.

        Returns:
            bool: True if successful
        """
        if not self.sol_active:
            Logger.error("No active SOL session")
            return False

        # Send break packet
        packet = bytes([
            self.sol_sequence_number,
            SOL_PACKET_BREAK,
            0x00, 0x00  # No data
        ])

        self._increment_sequence_number()

        try:
            # Send SOL break packet
            # In a real implementation, this would use a custom RMCP+ packet
            # For now, we just log it
            Logger.info("Sending SOL break")
            return True
        except Exception as e:
            Logger.error(f"Failed to send SOL break: {str(e)}")
            return False

    def _sol_thread_func(self) -> None:
        """SOL thread function."""
        Logger.info("SOL thread started")

        while self.sol_running:
            try:
                # Check for outgoing data
                try:
                    data = self.sol_data_queue.get(block=False)
                    self._send_sol_packet(data)
                except queue.Empty:
                    pass

                # Check for incoming data
                # In a real implementation, this would receive RMCP+ packets
                # For now, we just simulate it
                time.sleep(0.1)

            except Exception as e:
                Logger.error(f"SOL thread error: {str(e)}")
                time.sleep(1.0)

        Logger.info("SOL thread stopped")

    def _send_sol_packet(self, data: bytes) -> bool:
        """Send SOL packet.

        Args:
            data: Data to send

        Returns:
            bool: True if successful
        """
        # In a real implementation, this would construct and send an RMCP+ packet
        # For now, we just log it
        Logger.info(f"Sending SOL data: {data!r}")

        self._increment_sequence_number()
        return True

    def _increment_sequence_number(self) -> None:
        """Increment SOL sequence number."""
        self.sol_sequence_number = (self.sol_sequence_number + 1) & 0x0F
