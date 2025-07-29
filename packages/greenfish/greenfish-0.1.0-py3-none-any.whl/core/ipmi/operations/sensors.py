"""IPMI sensor operations module."""
from typing import Dict, Any, List, Optional

from greenfish.utils.logger import Logger

# IPMI constants
IPMI_NETFN_SENSOR_EVENT = 0x04
IPMI_CMD_GET_DEVICE_SDR_INFO = 0x20
IPMI_CMD_GET_DEVICE_SDR = 0x21
IPMI_CMD_RESERVE_DEVICE_SDR_REPOSITORY = 0x22
IPMI_CMD_GET_SENSOR_READING = 0x2D
IPMI_CMD_GET_SENSOR_TYPE = 0x2F

# Sensor types
SENSOR_TYPE_TEMPERATURE = 0x01
SENSOR_TYPE_VOLTAGE = 0x02
SENSOR_TYPE_CURRENT = 0x03
SENSOR_TYPE_FAN = 0x04
SENSOR_TYPE_PHYSICAL_SECURITY = 0x05
SENSOR_TYPE_PLATFORM_SECURITY = 0x06
SENSOR_TYPE_PROCESSOR = 0x07
SENSOR_TYPE_POWER_SUPPLY = 0x08
SENSOR_TYPE_POWER_UNIT = 0x09
SENSOR_TYPE_COOLING_DEVICE = 0x0A
SENSOR_TYPE_OTHER_UNITS_BASED_SENSOR = 0x0B
SENSOR_TYPE_MEMORY = 0x0C
SENSOR_TYPE_DRIVE_SLOT = 0x0D
SENSOR_TYPE_POST_MEMORY_RESIZE = 0x0E
SENSOR_TYPE_SYSTEM_FIRMWARE_PROGRESS = 0x0F
SENSOR_TYPE_EVENT_LOGGING_DISABLED = 0x10
SENSOR_TYPE_WATCHDOG_1 = 0x11
SENSOR_TYPE_SYSTEM_EVENT = 0x12
SENSOR_TYPE_CRITICAL_INTERRUPT = 0x13
SENSOR_TYPE_BUTTON = 0x14
SENSOR_TYPE_MODULE_BOARD = 0x15
SENSOR_TYPE_MICROCONTROLLER = 0x16
SENSOR_TYPE_ADD_IN_CARD = 0x17
SENSOR_TYPE_CHASSIS = 0x18
SENSOR_TYPE_CHIP_SET = 0x19
SENSOR_TYPE_OTHER_FRU = 0x1A
SENSOR_TYPE_CABLE_INTERCONNECT = 0x1B
SENSOR_TYPE_TERMINATOR = 0x1C
SENSOR_TYPE_SYSTEM_BOOT_INITIATED = 0x1D
SENSOR_TYPE_BOOT_ERROR = 0x1E
SENSOR_TYPE_OS_BOOT = 0x1F
SENSOR_TYPE_OS_CRITICAL_STOP = 0x20
SENSOR_TYPE_SLOT_CONNECTOR = 0x21
SENSOR_TYPE_SYSTEM_ACPI_POWER_STATE = 0x22
SENSOR_TYPE_WATCHDOG_2 = 0x23
SENSOR_TYPE_PLATFORM_ALERT = 0x24
SENSOR_TYPE_ENTITY_PRESENCE = 0x25
SENSOR_TYPE_MONITOR_ASIC = 0x26
SENSOR_TYPE_LAN = 0x27
SENSOR_TYPE_MANAGEMENT_SUBSYSTEM_HEALTH = 0x28
SENSOR_TYPE_BATTERY = 0x29
SENSOR_TYPE_SESSION_AUDIT = 0x2A
SENSOR_TYPE_VERSION_CHANGE = 0x2B
SENSOR_TYPE_FRU_STATE = 0x2C

# Sensor units
SENSOR_UNIT_UNSPECIFIED = 0x00
SENSOR_UNIT_DEGREES_C = 0x01
SENSOR_UNIT_DEGREES_F = 0x02
SENSOR_UNIT_DEGREES_K = 0x03
SENSOR_UNIT_VOLTS = 0x04
SENSOR_UNIT_AMPS = 0x05
SENSOR_UNIT_WATTS = 0x06
SENSOR_UNIT_JOULES = 0x07
SENSOR_UNIT_COULOMBS = 0x08
SENSOR_UNIT_VA = 0x09
SENSOR_UNIT_NITS = 0x0A
SENSOR_UNIT_LUMEN = 0x0B
SENSOR_UNIT_LUX = 0x0C
SENSOR_UNIT_CANDELA = 0x0D
SENSOR_UNIT_KPA = 0x0E
SENSOR_UNIT_PSI = 0x0F
SENSOR_UNIT_NEWTON = 0x10
SENSOR_UNIT_CFM = 0x11
SENSOR_UNIT_RPM = 0x12
SENSOR_UNIT_HZ = 0x13
SENSOR_UNIT_MICROSECOND = 0x14
SENSOR_UNIT_MILLISECOND = 0x15
SENSOR_UNIT_SECOND = 0x16
SENSOR_UNIT_MINUTE = 0x17
SENSOR_UNIT_HOUR = 0x18
SENSOR_UNIT_DAY = 0x19
SENSOR_UNIT_WEEK = 0x1A
SENSOR_UNIT_MIL = 0x1B
SENSOR_UNIT_INCHES = 0x1C
SENSOR_UNIT_FEET = 0x1D
SENSOR_UNIT_CU_IN = 0x1E
SENSOR_UNIT_CU_FEET = 0x1F
SENSOR_UNIT_MM = 0x20
SENSOR_UNIT_CM = 0x21
SENSOR_UNIT_M = 0x22
SENSOR_UNIT_CU_CM = 0x23
SENSOR_UNIT_CU_M = 0x24
SENSOR_UNIT_LITERS = 0x25
SENSOR_UNIT_FLUID_OUNCE = 0x26
SENSOR_UNIT_RADIANS = 0x27
SENSOR_UNIT_STERADIANS = 0x28
SENSOR_UNIT_REVOLUTIONS = 0x29
SENSOR_UNIT_CYCLES = 0x2A
SENSOR_UNIT_GRAVITIES = 0x2B
SENSOR_UNIT_OUNCE = 0x2C
SENSOR_UNIT_POUND = 0x2D
SENSOR_UNIT_FT_LB = 0x2E
SENSOR_UNIT_OZ_IN = 0x2F
SENSOR_UNIT_GAUSS = 0x30
SENSOR_UNIT_GILBERTS = 0x31
SENSOR_UNIT_HENRY = 0x32
SENSOR_UNIT_MILLIHENRY = 0x33
SENSOR_UNIT_FARAD = 0x34
SENSOR_UNIT_MICROFARAD = 0x35
SENSOR_UNIT_OHMS = 0x36
SENSOR_UNIT_SIEMENS = 0x37
SENSOR_UNIT_MOLE = 0x38
SENSOR_UNIT_BECQUEREL = 0x39
SENSOR_UNIT_PPM = 0x3A
SENSOR_UNIT_RESERVED = 0x3B
SENSOR_UNIT_DECIBELS = 0x3C
SENSOR_UNIT_DBA = 0x3D
SENSOR_UNIT_DBC = 0x3E
SENSOR_UNIT_GRAY = 0x3F
SENSOR_UNIT_SIEVERT = 0x40
SENSOR_UNIT_COLOR_TEMP_DEG_K = 0x41
SENSOR_UNIT_BIT = 0x42
SENSOR_UNIT_KILOBIT = 0x43
SENSOR_UNIT_MEGABIT = 0x44
SENSOR_UNIT_GIGABIT = 0x45
SENSOR_UNIT_BYTE = 0x46
SENSOR_UNIT_KILOBYTE = 0x47
SENSOR_UNIT_MEGABYTE = 0x48
SENSOR_UNIT_GIGABYTE = 0x49
SENSOR_UNIT_WORD = 0x4A
SENSOR_UNIT_DWORD = 0x4B
SENSOR_UNIT_QWORD = 0x4C
SENSOR_UNIT_LINE = 0x4D
SENSOR_UNIT_HIT = 0x4E
SENSOR_UNIT_MISS = 0x4F
SENSOR_UNIT_RETRY = 0x50
SENSOR_UNIT_RESET = 0x51
SENSOR_UNIT_OVERFLOW = 0x52
SENSOR_UNIT_UNDERRUN = 0x53
SENSOR_UNIT_COLLISION = 0x54
SENSOR_UNIT_PACKETS = 0x55
SENSOR_UNIT_MESSAGES = 0x56
SENSOR_UNIT_CHARACTERS = 0x57
SENSOR_UNIT_ERROR = 0x58
SENSOR_UNIT_CORRECTABLE_ERROR = 0x59
SENSOR_UNIT_UNCORRECTABLE_ERROR = 0x5A
SENSOR_UNIT_FATAL_ERROR = 0x5B
SENSOR_UNIT_GRAMS = 0x5C

class SensorOperations:
    """IPMI sensor operations handler."""

    def __init__(self, protocol):
        """Initialize sensor operations handler.

        Args:
            protocol: IPMI protocol handler
        """
        self.protocol = protocol
        self._sdr_cache = {}
        self._reservation_id = None

    def get_sensor_reading(self, sensor_number: int) -> Dict[str, Any]:
        """Get sensor reading.

        Args:
            sensor_number: Sensor number

        Returns:
            Dict containing sensor reading information
        """
        data = bytes([sensor_number])
        response = self.protocol.send_command(IPMI_NETFN_SENSOR_EVENT, IPMI_CMD_GET_SENSOR_READING, data)

        if response['completion_code'] != 0:
            Logger.error(f"Failed to get sensor reading: {response['completion_code']:#x}")
            return {}

        data = response['data']
        if len(data) < 4:
            Logger.error("Invalid sensor reading response")
            return {}

        reading = data[0]
        reading_state = data[1]
        threshold_status = data[2]

        return {
            'sensor_number': sensor_number,
            'reading': reading,
            'reading_state': reading_state,
            'scanning_enabled': bool(reading_state & 0x40),
            'reading_unavailable': bool(reading_state & 0x20),
            'threshold_status': {
                'lower_non_critical': bool(threshold_status & 0x01),
                'lower_critical': bool(threshold_status & 0x02),
                'lower_non_recoverable': bool(threshold_status & 0x04),
                'upper_non_critical': bool(threshold_status & 0x08),
                'upper_critical': bool(threshold_status & 0x10),
                'upper_non_recoverable': bool(threshold_status & 0x20)
            }
        }

    def get_sdr_repository_info(self) -> Dict[str, Any]:
        """Get SDR repository information.

        Returns:
            Dict containing SDR repository information
        """
        response = self.protocol.send_command(IPMI_NETFN_SENSOR_EVENT, IPMI_CMD_GET_DEVICE_SDR_INFO)

        if response['completion_code'] != 0:
            Logger.error(f"Failed to get SDR repository info: {response['completion_code']:#x}")
            return {}

        data = response['data']
        if len(data) < 3:
            Logger.error("Invalid SDR repository info response")
            return {}

        return {
            'sdr_version': data[0],
            'record_count': (data[2] << 8) | data[1],
            'free_space': 0,  # Not available in device SDR
            'most_recent_addition': 0,  # Not available in device SDR
            'most_recent_erase': 0  # Not available in device SDR
        }

    def reserve_sdr_repository(self) -> int:
        """Reserve SDR repository.

        Returns:
            Reservation ID or 0 on failure
        """
        response = self.protocol.send_command(IPMI_NETFN_SENSOR_EVENT, IPMI_CMD_RESERVE_DEVICE_SDR_REPOSITORY)

        if response['completion_code'] != 0:
            Logger.error(f"Failed to reserve SDR repository: {response['completion_code']:#x}")
            return 0

        data = response['data']
        if len(data) < 2:
            Logger.error("Invalid reserve SDR repository response")
            return 0

        reservation_id = (data[1] << 8) | data[0]
        self._reservation_id = reservation_id

        return reservation_id

    def get_sdr(self, record_id: int) -> Dict[str, Any]:
        """Get SDR record.

        Args:
            record_id: Record ID

        Returns:
            Dict containing SDR record information
        """
        # Check if record is in cache
        if record_id in self._sdr_cache:
            return self._sdr_cache[record_id]

        # Reserve SDR repository if needed
        if self._reservation_id is None:
            self.reserve_sdr_repository()

        # Get SDR record header first to determine record length
        request_data = bytes([
            record_id & 0xFF,
            (record_id >> 8) & 0xFF,
            self._reservation_id & 0xFF,
            (self._reservation_id >> 8) & 0xFF,
            0x00,  # Offset
            0x05   # Bytes to read (header size)
        ])

        response = self.protocol.send_command(IPMI_NETFN_SENSOR_EVENT, IPMI_CMD_GET_DEVICE_SDR, request_data)

        if response['completion_code'] != 0:
            Logger.error(f"Failed to get SDR header: {response['completion_code']:#x}")
            return {}

        data = response['data']
        if len(data) < 7:
            Logger.error("Invalid SDR header response")
            return {}

        next_record_id = (data[1] << 8) | data[0]
        record_type = data[2]
        record_length = data[6]

        # Now get the full record
        record_data = bytearray()

        # Read in chunks of 16 bytes
        offset = 0
        while offset < record_length:
            bytes_to_read = min(16, record_length - offset)

            request_data = bytes([
                record_id & 0xFF,
                (record_id >> 8) & 0xFF,
                self._reservation_id & 0xFF,
                (self._reservation_id >> 8) & 0xFF,
                offset,
                bytes_to_read
            ])

            response = self.protocol.send_command(IPMI_NETFN_SENSOR_EVENT, IPMI_CMD_GET_DEVICE_SDR, request_data)

            if response['completion_code'] != 0:
                Logger.error(f"Failed to get SDR data: {response['completion_code']:#x}")
                return {}

            chunk_data = response['data'][2:]  # Skip next record ID
            record_data.extend(chunk_data)
            offset += len(chunk_data)

        # Parse SDR record based on type
        sdr_record = {
            'record_id': record_id,
            'next_record_id': next_record_id,
            'record_type': record_type,
            'record_length': record_length,
            'raw_data': bytes(record_data)
        }

        if record_type == 0x01:  # Full sensor record
            self._parse_full_sensor_record(sdr_record, record_data)
        elif record_type == 0x02:  # Compact sensor record
            self._parse_compact_sensor_record(sdr_record, record_data)

        # Cache the record
        self._sdr_cache[record_id] = sdr_record

        return sdr_record

    def get_all_sensors(self) -> List[Dict[str, Any]]:
        """Get all sensors with readings.

        Returns:
            List of sensor data dictionaries
        """
        sensors = []

        # Get SDR repository info
        sdr_info = self.get_sdr_repository_info()
        if not sdr_info:
            return sensors

        # Get all SDR records
        record_id = 0
        for _ in range(sdr_info.get('record_count', 0)):
            sdr_record = self.get_sdr(record_id)
            if not sdr_record:
                break

            # Only process sensor records
            if sdr_record.get('record_type') in [0x01, 0x02]:
                sensor_number = sdr_record.get('sensor_number')
                if sensor_number is not None:
                    # Get sensor reading
                    reading_data = self.get_sensor_reading(sensor_number)

                    # Combine SDR data with reading
                    sensor_data = {**sdr_record, **reading_data}
                    sensors.append(sensor_data)

            # Move to next record
            record_id = sdr_record.get('next_record_id')
            if record_id == 0xFFFF:
                break

        return sensors

    def get_sensors_by_type(self, sensor_type: int) -> List[Dict[str, Any]]:
        """Get sensors of a specific type.

        Args:
            sensor_type: Sensor type code

        Returns:
            List of sensor data dictionaries
        """
        all_sensors = self.get_all_sensors()
        return [s for s in all_sensors if s.get('sensor_type') == sensor_type]

    def _parse_full_sensor_record(self, record: Dict[str, Any], data: bytearray) -> None:
        """Parse full sensor record data.

        Args:
            record: SDR record dictionary to update
            data: Raw record data
        """
        if len(data) < 48:
            Logger.error("Invalid full sensor record data")
            return

        record['sensor_owner_id'] = data[0]
        record['sensor_owner_lun'] = data[1] & 0x03
        record['sensor_number'] = data[2]
        record['entity_id'] = data[3]
        record['entity_instance'] = data[4]
        record['sensor_initialization'] = data[5]
        record['sensor_capabilities'] = data[6]
        record['sensor_type'] = data[7]
        record['event_reading_type'] = data[8]

        # Sensor units
        record['sensor_units'] = {
            'percentage': bool(data[9] & 0x01),
            'modifier': (data[9] >> 1) & 0x03,
            'rate': (data[9] >> 3) & 0x07,
            'base_unit': data[10],
            'modifier_unit': data[11]
        }

        # Linearization and M, B, K factors for conversion
        record['linearization'] = data[12] & 0x7F
        record['m'] = data[13] | ((data[14] & 0xC0) << 2)
        record['m_tolerance'] = data[14] & 0x3F
        record['b'] = data[15] | ((data[16] & 0xC0) << 2)
        record['b_accuracy'] = data[16] & 0x3F
        record['accuracy'] = data[17] | ((data[18] & 0xF0) << 4)
        record['accuracy_exp'] = (data[18] >> 2) & 0x03
        record['r_exp'] = data[18] & 0x03
        record['b_exp'] = (data[19] >> 4) & 0x0F

        # Extract sensor name
        name_length = data[47] & 0x1F
        if len(data) >= 48 + name_length:
            name_data = data[48:48 + name_length]
            try:
                record['sensor_id'] = name_data.decode('ascii').strip()
            except UnicodeDecodeError:
                record['sensor_id'] = f"Sensor-{record['sensor_number']}"
        else:
            record['sensor_id'] = f"Sensor-{record['sensor_number']}"

    def _parse_compact_sensor_record(self, record: Dict[str, Any], data: bytearray) -> None:
        """Parse compact sensor record data.

        Args:
            record: SDR record dictionary to update
            data: Raw record data
        """
        if len(data) < 32:
            Logger.error("Invalid compact sensor record data")
            return

        record['sensor_owner_id'] = data[0]
        record['sensor_owner_lun'] = data[1] & 0x03
        record['sensor_number'] = data[2]
        record['entity_id'] = data[3]
        record['entity_instance'] = data[4]
        record['sensor_initialization'] = data[5]
        record['sensor_capabilities'] = data[6]
        record['sensor_type'] = data[7]
        record['event_reading_type'] = data[8]

        # Extract sensor name
        name_length = data[31] & 0x1F
        if len(data) >= 32 + name_length:
            name_data = data[32:32 + name_length]
            try:
                record['sensor_id'] = name_data.decode('ascii').strip()
            except UnicodeDecodeError:
                record['sensor_id'] = f"Sensor-{record['sensor_number']}"
        else:
            record['sensor_id'] = f"Sensor-{record['sensor_number']}"
