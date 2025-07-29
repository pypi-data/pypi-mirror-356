"""IPMI System Event Log (SEL) operations module."""
from typing import Dict, Any, List, Optional
import time
from datetime import datetime

from greenfish.utils.logger import Logger

# IPMI constants
IPMI_NETFN_STORAGE = 0x0A
IPMI_CMD_GET_SEL_INFO = 0x40
IPMI_CMD_GET_SEL_ALLOCATION_INFO = 0x41
IPMI_CMD_RESERVE_SEL = 0x42
IPMI_CMD_GET_SEL_ENTRY = 0x43
IPMI_CMD_ADD_SEL_ENTRY = 0x44
IPMI_CMD_PARTIAL_ADD_SEL_ENTRY = 0x45
IPMI_CMD_DELETE_SEL_ENTRY = 0x46
IPMI_CMD_CLEAR_SEL = 0x47
IPMI_CMD_GET_SEL_TIME = 0x48
IPMI_CMD_SET_SEL_TIME = 0x49
IPMI_CMD_GET_AUXILIARY_LOG_STATUS = 0x5A
IPMI_CMD_SET_AUXILIARY_LOG_STATUS = 0x5B

# SEL record types
SEL_RECORD_TYPE_SYSTEM_EVENT = 0x02
SEL_RECORD_TYPE_OEM_TIMESTAMPED = 0xC0
SEL_RECORD_TYPE_OEM_NON_TIMESTAMPED = 0xE0

class SELOperations:
    """IPMI SEL operations handler."""

    def __init__(self, protocol):
        """Initialize SEL operations handler.

        Args:
            protocol: IPMI protocol handler
        """
        self.protocol = protocol
        self._reservation_id = None

    def get_sel_info(self) -> Dict[str, Any]:
        """Get SEL information.

        Returns:
            Dict containing SEL information
        """
        response = self.protocol.send_command(IPMI_NETFN_STORAGE, IPMI_CMD_GET_SEL_INFO)

        if response['completion_code'] != 0:
            Logger.error(f"Failed to get SEL info: {response['completion_code']:#x}")
            return {}

        data = response['data']
        if len(data) < 14:
            Logger.error("Invalid SEL info response")
            return {}

        return {
            'version': data[0],
            'entries': (data[2] << 8) | data[1],
            'free_space': (data[4] << 8) | data[3],
            'most_recent_addition': int.from_bytes(data[5:9], byteorder='little'),
            'most_recent_erase': int.from_bytes(data[9:13], byteorder='little'),
            'operation_support': {
                'delete_sel': bool(data[13] & 0x08),
                'partial_add_sel': bool(data[13] & 0x04),
                'reserve_sel': bool(data[13] & 0x02),
                'get_sel_allocation': bool(data[13] & 0x01)
            }
        }

    def reserve_sel(self) -> int:
        """Reserve SEL.

        Returns:
            Reservation ID or 0 on failure
        """
        response = self.protocol.send_command(IPMI_NETFN_STORAGE, IPMI_CMD_RESERVE_SEL)

        if response['completion_code'] != 0:
            Logger.error(f"Failed to reserve SEL: {response['completion_code']:#x}")
            return 0

        data = response['data']
        if len(data) < 2:
            Logger.error("Invalid reserve SEL response")
            return 0

        reservation_id = (data[1] << 8) | data[0]
        self._reservation_id = reservation_id

        return reservation_id

    def get_sel_entry(self, record_id: int) -> Dict[str, Any]:
        """Get SEL entry.

        Args:
            record_id: Record ID

        Returns:
            Dict containing SEL entry information
        """
        # Reserve SEL if needed
        if self._reservation_id is None:
            self.reserve_sel()

        request_data = bytes([
            record_id & 0xFF,
            (record_id >> 8) & 0xFF,
            self._reservation_id & 0xFF,
            (self._reservation_id >> 8) & 0xFF,
            0x00,  # Offset
            0xFF   # Bytes to read (all)
        ])

        response = self.protocol.send_command(IPMI_NETFN_STORAGE, IPMI_CMD_GET_SEL_ENTRY, request_data)

        if response['completion_code'] != 0:
            Logger.error(f"Failed to get SEL entry: {response['completion_code']:#x}")
            return {}

        data = response['data']
        if len(data) < 16:
            Logger.error("Invalid SEL entry response")
            return {}

        next_record_id = (data[1] << 8) | data[0]
        record_type = data[4]

        # Parse record based on type
        record = {
            'record_id': record_id,
            'next_record_id': next_record_id,
            'record_type': record_type,
            'raw_data': data[2:]
        }

        if record_type == SEL_RECORD_TYPE_SYSTEM_EVENT:
            self._parse_system_event_record(record, data[2:])
        elif record_type >= SEL_RECORD_TYPE_OEM_TIMESTAMPED:
            self._parse_oem_record(record, data[2:])

        return record

    def get_all_sel_entries(self) -> List[Dict[str, Any]]:
        """Get all SEL entries.

        Returns:
            List of SEL entry dictionaries
        """
        entries = []

        # Get SEL info
        sel_info = self.get_sel_info()
        if not sel_info:
            return entries

        # Get all entries
        record_id = 0
        for _ in range(sel_info.get('entries', 0)):
            entry = self.get_sel_entry(record_id)
            if not entry:
                break

            entries.append(entry)

            # Move to next record
            record_id = entry.get('next_record_id')
            if record_id == 0xFFFF:
                break

        return entries

    def clear_sel(self) -> bool:
        """Clear SEL.

        Returns:
            bool: True if successful
        """
        # Reserve SEL if needed
        if self._reservation_id is None:
            self.reserve_sel()

        # First initiate clear with 'CLR' ASCII
        request_data = bytes([
            self._reservation_id & 0xFF,
            (self._reservation_id >> 8) & 0xFF,
            0x43,  # 'C'
            0x4C,  # 'L'
            0x52,  # 'R'
            0xAA   # Initiate erase
        ])

        response = self.protocol.send_command(IPMI_NETFN_STORAGE, IPMI_CMD_CLEAR_SEL, request_data)

        if response['completion_code'] != 0:
            Logger.error(f"Failed to initiate SEL clear: {response['completion_code']:#x}")
            return False

        data = response['data']
        if len(data) < 1:
            Logger.error("Invalid clear SEL response")
            return False

        # Check status
        status = data[0]
        if status == 0x00:
            # Erase completed
            return True
        elif status == 0x01:
            # Erase in progress, poll until complete
            max_retries = 10
            retry_delay = 1.0

            for _ in range(max_retries):
                time.sleep(retry_delay)

                # Check status
                request_data = bytes([
                    self._reservation_id & 0xFF,
                    (self._reservation_id >> 8) & 0xFF,
                    0x43,  # 'C'
                    0x4C,  # 'L'
                    0x52,  # 'R'
                    0x00   # Get erase status
                ])

                response = self.protocol.send_command(IPMI_NETFN_STORAGE, IPMI_CMD_CLEAR_SEL, request_data)

                if response['completion_code'] != 0:
                    Logger.error(f"Failed to get SEL clear status: {response['completion_code']:#x}")
                    return False

                data = response['data']
                if len(data) < 1:
                    Logger.error("Invalid clear SEL status response")
                    return False

                status = data[0]
                if status == 0x00:
                    # Erase completed
                    return True

            Logger.error("SEL clear timed out")
            return False
        else:
            Logger.error(f"Unknown SEL clear status: {status:#x}")
            return False

    def get_sel_time(self) -> int:
        """Get SEL time.

        Returns:
            SEL time as Unix timestamp
        """
        response = self.protocol.send_command(IPMI_NETFN_STORAGE, IPMI_CMD_GET_SEL_TIME)

        if response['completion_code'] != 0:
            Logger.error(f"Failed to get SEL time: {response['completion_code']:#x}")
            return 0

        data = response['data']
        if len(data) < 4:
            Logger.error("Invalid SEL time response")
            return 0

        return int.from_bytes(data, byteorder='little')

    def set_sel_time(self, timestamp: int) -> bool:
        """Set SEL time.

        Args:
            timestamp: Unix timestamp

        Returns:
            bool: True if successful
        """
        request_data = timestamp.to_bytes(4, byteorder='little')

        response = self.protocol.send_command(IPMI_NETFN_STORAGE, IPMI_CMD_SET_SEL_TIME, request_data)

        if response['completion_code'] != 0:
            Logger.error(f"Failed to set SEL time: {response['completion_code']:#x}")
            return False

        return True

    def _parse_system_event_record(self, record: Dict[str, Any], data: bytes) -> None:
        """Parse system event record data.

        Args:
            record: SEL record dictionary to update
            data: Raw record data
        """
        if len(data) < 14:
            Logger.error("Invalid system event record data")
            return

        # Extract timestamp
        timestamp = int.from_bytes(data[2:6], byteorder='little')

        # Convert timestamp to datetime
        try:
            dt = datetime.fromtimestamp(timestamp)
            record['timestamp'] = dt.isoformat()
        except (ValueError, OverflowError):
            record['timestamp'] = None

        record['generator_id'] = (data[7] << 8) | data[6]
        record['event_message_format_version'] = data[8] >> 4
        record['sensor_type'] = data[9]
        record['sensor_number'] = data[10]
        record['event_type'] = data[11] & 0x7F
        record['event_direction'] = 'assertion' if data[11] & 0x80 else 'deassertion'
        record['event_data'] = data[12:15]

        # Decode event data based on event type
        if record['event_type'] == 0x01:  # Threshold event
            record['event_description'] = self._decode_threshold_event(data[12], data[13], data[14])
        elif record['event_type'] == 0x02:  # Discrete event
            record['event_description'] = self._decode_discrete_event(data[12], data[13], data[14])
        elif record['event_type'] == 0x03:  # Digital discrete event
            record['event_description'] = self._decode_digital_event(data[12], data[13], data[14])
        else:
            record['event_description'] = f"Event type {record['event_type']:#x}"

    def _parse_oem_record(self, record: Dict[str, Any], data: bytes) -> None:
        """Parse OEM record data.

        Args:
            record: SEL record dictionary to update
            data: Raw record data
        """
        if len(data) < 14:
            Logger.error("Invalid OEM record data")
            return

        # For timestamped OEM records
        if record['record_type'] >= SEL_RECORD_TYPE_OEM_TIMESTAMPED and record['record_type'] <= 0xDF:
            # Extract timestamp
            timestamp = int.from_bytes(data[2:6], byteorder='little')

            # Convert timestamp to datetime
            try:
                dt = datetime.fromtimestamp(timestamp)
                record['timestamp'] = dt.isoformat()
            except (ValueError, OverflowError):
                record['timestamp'] = None

            record['manufacturer_id'] = int.from_bytes(data[6:9], byteorder='little')
            record['oem_data'] = data[9:]
        else:
            # Non-timestamped OEM records
            record['oem_data'] = data[2:]

    def _decode_threshold_event(self, data1: int, data2: int, data3: int) -> str:
        """Decode threshold event data.

        Args:
            data1: Event data 1
            data2: Event data 2
            data3: Event data 3

        Returns:
            Event description string
        """
        threshold_type = (data1 >> 1) & 0x07
        threshold_map = {
            0x00: "Lower Non-critical",
            0x01: "Lower Critical",
            0x02: "Lower Non-recoverable",
            0x03: "Upper Non-critical",
            0x04: "Upper Critical",
            0x05: "Upper Non-recoverable"
        }

        direction = "going high" if data1 & 0x01 else "going low"
        threshold = threshold_map.get(threshold_type, f"Unknown ({threshold_type:#x})")

        return f"Threshold {threshold} {direction}, value = {data2:#x}"

    def _decode_discrete_event(self, data1: int, data2: int, data3: int) -> str:
        """Decode discrete event data.

        Args:
            data1: Event data 1
            data2: Event data 2
            data3: Event data 3

        Returns:
            Event description string
        """
        offset = data1 & 0x0F
        return f"Discrete event, offset = {offset:#x}, data = {data2:#x} {data3:#x}"

    def _decode_digital_event(self, data1: int, data2: int, data3: int) -> str:
        """Decode digital discrete event data.

        Args:
            data1: Event data 1
            data2: Event data 2
            data3: Event data 3

        Returns:
            Event description string
        """
        state = "asserted" if data1 & 0x01 else "deasserted"
        return f"Digital state {state}, data = {data2:#x} {data3:#x}"
