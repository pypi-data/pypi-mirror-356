"""IPMI FRU (Field Replaceable Unit) operations module."""
from typing import Dict, Any, List, Optional
import struct

from greenfish.utils.logger import Logger

# IPMI constants
IPMI_NETFN_STORAGE = 0x0A
IPMI_CMD_GET_FRU_INVENTORY_AREA_INFO = 0x10
IPMI_CMD_READ_FRU_DATA = 0x11
IPMI_CMD_WRITE_FRU_DATA = 0x12

# FRU area types
FRU_AREA_INTERNAL = 0
FRU_AREA_CHASSIS = 1
FRU_AREA_BOARD = 2
FRU_AREA_PRODUCT = 3
FRU_AREA_MULTIRECORD = 4

# FRU language codes
FRU_LANG_ENGLISH = 0
FRU_LANG_AFAR = 1
FRU_LANG_ABKHAZIAN = 2
FRU_LANG_AFRIKAANS = 3
FRU_LANG_AMHARIC = 4

class FRUOperations:
    """IPMI FRU operations handler."""

    def __init__(self, protocol):
        """Initialize FRU operations handler.

        Args:
            protocol: IPMI protocol handler
        """
        self.protocol = protocol
        self._fru_cache = {}

    def get_fru_inventory_area_info(self, device_id: int = 0) -> Dict[str, Any]:
        """Get FRU inventory area information.

        Args:
            device_id: FRU device ID

        Returns:
            Dict containing FRU inventory area information
        """
        request_data = bytes([device_id])

        response = self.protocol.send_command(IPMI_NETFN_STORAGE, IPMI_CMD_GET_FRU_INVENTORY_AREA_INFO, request_data)

        if response['completion_code'] != 0:
            Logger.error(f"Failed to get FRU inventory area info: {response['completion_code']:#x}")
            return {}

        data = response['data']
        if len(data) < 3:
            Logger.error("Invalid FRU inventory area info response")
            return {}

        return {
            'area_size': (data[1] << 8) | data[0],
            'access': "word" if data[2] & 0x01 else "byte"
        }

    def read_fru_data(self, device_id: int = 0, offset: int = 0, count: int = 16) -> bytes:
        """Read FRU data.

        Args:
            device_id: FRU device ID
            offset: Offset to read from
            count: Number of bytes to read

        Returns:
            FRU data bytes
        """
        request_data = bytes([
            device_id,
            offset & 0xFF,
            (offset >> 8) & 0xFF,
            count
        ])

        response = self.protocol.send_command(IPMI_NETFN_STORAGE, IPMI_CMD_READ_FRU_DATA, request_data)

        if response['completion_code'] != 0:
            Logger.error(f"Failed to read FRU data: {response['completion_code']:#x}")
            return b''

        data = response['data']
        if len(data) < 1:
            Logger.error("Invalid read FRU data response")
            return b''

        count_read = data[0]
        if count_read == 0:
            return b''

        return data[1:1 + count_read]

    def read_fru_area(self, device_id: int = 0) -> bytes:
        """Read entire FRU area.

        Args:
            device_id: FRU device ID

        Returns:
            FRU area bytes
        """
        # Check if FRU data is in cache
        if device_id in self._fru_cache:
            return self._fru_cache[device_id]

        # Get FRU inventory area info
        area_info = self.get_fru_inventory_area_info(device_id)
        if not area_info:
            return b''

        area_size = area_info.get('area_size', 0)
        if area_size == 0:
            return b''

        # Read FRU data in chunks
        fru_data = bytearray()
        offset = 0

        while offset < area_size:
            count = min(16, area_size - offset)
            chunk = self.read_fru_data(device_id, offset, count)

            if not chunk:
                break

            fru_data.extend(chunk)
            offset += len(chunk)

        # Cache FRU data
        self._fru_cache[device_id] = bytes(fru_data)

        return bytes(fru_data)

    def get_fru_inventory(self, device_id: int = 0) -> Dict[str, Any]:
        """Get FRU inventory information.

        Args:
            device_id: FRU device ID

        Returns:
            Dict containing FRU inventory information
        """
        # Read FRU area
        fru_data = self.read_fru_area(device_id)
        if not fru_data or len(fru_data) < 8:
            return {}

        # Parse common header
        common_header = self._parse_common_header(fru_data)
        if not common_header:
            return {}

        result = {
            'common_header': common_header,
            'device_id': device_id
        }

        # Parse chassis info area
        if common_header.get('chassis_offset', 0) > 0:
            chassis_offset = common_header['chassis_offset'] * 8
            chassis_info = self._parse_chassis_info(fru_data, chassis_offset)
            result['chassis_info'] = chassis_info

        # Parse board info area
        if common_header.get('board_offset', 0) > 0:
            board_offset = common_header['board_offset'] * 8
            board_info = self._parse_board_info(fru_data, board_offset)
            result['board_info'] = board_info

        # Parse product info area
        if common_header.get('product_offset', 0) > 0:
            product_offset = common_header['product_offset'] * 8
            product_info = self._parse_product_info(fru_data, product_offset)
            result['product_info'] = product_info

        # Parse multi-record area
        if common_header.get('multirecord_offset', 0) > 0:
            multirecord_offset = common_header['multirecord_offset'] * 8
            multirecord_info = self._parse_multirecord_info(fru_data, multirecord_offset)
            result['multirecord_info'] = multirecord_info

        return result

    def _parse_common_header(self, data: bytes) -> Dict[str, Any]:
        """Parse FRU common header.

        Args:
            data: FRU data bytes

        Returns:
            Dict containing common header information
        """
        if len(data) < 8:
            Logger.error("Invalid FRU common header")
            return {}

        # Check format version
        if data[0] != 0x01:
            Logger.error(f"Unsupported FRU format version: {data[0]:#x}")
            return {}

        # Calculate header checksum
        checksum = sum(data[0:7]) & 0xFF
        if (checksum + data[7]) & 0xFF != 0:
            Logger.error(f"Invalid FRU common header checksum: {data[7]:#x}, calculated: {(0x100 - checksum) & 0xFF:#x}")
            return {}

        return {
            'format_version': data[0],
            'internal_offset': data[1],
            'chassis_offset': data[2],
            'board_offset': data[3],
            'product_offset': data[4],
            'multirecord_offset': data[5],
            'pad': data[6],
            'checksum': data[7]
        }

    def _parse_chassis_info(self, data: bytes, offset: int) -> Dict[str, Any]:
        """Parse FRU chassis info area.

        Args:
            data: FRU data bytes
            offset: Offset to chassis info area

        Returns:
            Dict containing chassis info
        """
        if offset >= len(data) or offset + 3 >= len(data):
            return {}

        # Check format version
        if data[offset] != 0x01:
            Logger.error(f"Unsupported chassis info format version: {data[offset]:#x}")
            return {}

        area_length = data[offset + 1] * 8
        if offset + area_length > len(data):
            area_length = len(data) - offset

        # Calculate checksum
        checksum = sum(data[offset:offset + area_length - 1]) & 0xFF
        if (checksum + data[offset + area_length - 1]) & 0xFF != 0:
            Logger.error("Invalid chassis info checksum")

        chassis_type = data[offset + 2]

        # Map chassis type to string
        chassis_types = {
            0x01: "Other",
            0x02: "Unknown",
            0x03: "Desktop",
            0x04: "Low Profile Desktop",
            0x05: "Pizza Box",
            0x06: "Mini Tower",
            0x07: "Tower",
            0x08: "Portable",
            0x09: "Laptop",
            0x0A: "Notebook",
            0x0B: "Hand Held",
            0x0C: "Docking Station",
            0x0D: "All in One",
            0x0E: "Sub Notebook",
            0x0F: "Space-saving",
            0x10: "Lunch Box",
            0x11: "Main Server Chassis",
            0x12: "Expansion Chassis",
            0x13: "SubChassis",
            0x14: "Bus Expansion Chassis",
            0x15: "Peripheral Chassis",
            0x16: "RAID Chassis",
            0x17: "Rack Mount Chassis",
            0x18: "Sealed-case PC",
            0x19: "Multi-system chassis",
            0x1A: "Compact PCI",
            0x1B: "Advanced TCA",
            0x1C: "Blade",
            0x1D: "Blade Enclosure"
        }

        chassis_type_str = chassis_types.get(chassis_type, f"Unknown ({chassis_type:#x})")

        # Parse part number and serial number
        part_number, serial_number, custom_fields = self._parse_type_length_fields(data, offset + 3, offset + area_length - 1)

        return {
            'format_version': data[offset],
            'area_length': area_length,
            'chassis_type': chassis_type,
            'chassis_type_str': chassis_type_str,
            'part_number': part_number,
            'serial_number': serial_number,
            'custom_fields': custom_fields
        }

    def _parse_board_info(self, data: bytes, offset: int) -> Dict[str, Any]:
        """Parse FRU board info area.

        Args:
            data: FRU data bytes
            offset: Offset to board info area

        Returns:
            Dict containing board info
        """
        if offset >= len(data) or offset + 6 >= len(data):
            return {}

        # Check format version
        if data[offset] != 0x01:
            Logger.error(f"Unsupported board info format version: {data[offset]:#x}")
            return {}

        area_length = data[offset + 1] * 8
        if offset + area_length > len(data):
            area_length = len(data) - offset

        # Calculate checksum
        checksum = sum(data[offset:offset + area_length - 1]) & 0xFF
        if (checksum + data[offset + area_length - 1]) & 0xFF != 0:
            Logger.error("Invalid board info checksum")

        language_code = data[offset + 2]

        # Parse manufacturing date/time
        mfg_time = int.from_bytes(data[offset + 3:offset + 6], byteorder='little')

        # Convert minutes since 1996-01-01 00:00:00 to a more readable format
        # Note: This is a simplified conversion
        minutes_since_1996 = mfg_time
        hours_since_1996 = minutes_since_1996 // 60
        days_since_1996 = hours_since_1996 // 24
        years_since_1996 = days_since_1996 // 365

        mfg_year = 1996 + years_since_1996
        remaining_days = days_since_1996 % 365
        mfg_month = (remaining_days // 30) + 1  # Approximate
        mfg_day = (remaining_days % 30) + 1     # Approximate

        mfg_date = f"{mfg_year:04d}-{mfg_month:02d}-{mfg_day:02d}"

        # Parse manufacturer, product name, serial number, part number, FRU file ID
        manufacturer, product_name, serial_number, part_number, fru_file_id, custom_fields = self._parse_type_length_fields(
            data, offset + 6, offset + area_length - 1, max_fields=5
        )

        return {
            'format_version': data[offset],
            'area_length': area_length,
            'language_code': language_code,
            'mfg_date': mfg_date,
            'manufacturer': manufacturer,
            'product_name': product_name,
            'serial_number': serial_number,
            'part_number': part_number,
            'fru_file_id': fru_file_id,
            'custom_fields': custom_fields
        }

    def _parse_product_info(self, data: bytes, offset: int) -> Dict[str, Any]:
        """Parse FRU product info area.

        Args:
            data: FRU data bytes
            offset: Offset to product info area

        Returns:
            Dict containing product info
        """
        if offset >= len(data) or offset + 3 >= len(data):
            return {}

        # Check format version
        if data[offset] != 0x01:
            Logger.error(f"Unsupported product info format version: {data[offset]:#x}")
            return {}

        area_length = data[offset + 1] * 8
        if offset + area_length > len(data):
            area_length = len(data) - offset

        # Calculate checksum
        checksum = sum(data[offset:offset + area_length - 1]) & 0xFF
        if (checksum + data[offset + area_length - 1]) & 0xFF != 0:
            Logger.error("Invalid product info checksum")

        language_code = data[offset + 2]

        # Parse manufacturer, product name, part number, version, serial number, asset tag, FRU file ID
        manufacturer, product_name, part_number, version, serial_number, asset_tag, fru_file_id, custom_fields = self._parse_type_length_fields(
            data, offset + 3, offset + area_length - 1, max_fields=7
        )

        return {
            'format_version': data[offset],
            'area_length': area_length,
            'language_code': language_code,
            'manufacturer': manufacturer,
            'product_name': product_name,
            'part_number': part_number,
            'version': version,
            'serial_number': serial_number,
            'asset_tag': asset_tag,
            'fru_file_id': fru_file_id,
            'custom_fields': custom_fields
        }

    def _parse_multirecord_info(self, data: bytes, offset: int) -> List[Dict[str, Any]]:
        """Parse FRU multi-record area.

        Args:
            data: FRU data bytes
            offset: Offset to multi-record area

        Returns:
            List of multi-record info dictionaries
        """
        records = []

        if offset >= len(data) or offset + 5 > len(data):
            return records

        current_offset = offset

        while current_offset + 5 <= len(data):
            record_type = data[current_offset]
            format_version = data[current_offset + 1]
            record_length = data[current_offset + 2]
            record_checksum = data[current_offset + 3]
            header_checksum = data[current_offset + 4]

            # Verify header checksum
            header_sum = sum(data[current_offset:current_offset + 4]) & 0xFF
            if (header_sum + header_checksum) & 0xFF != 0:
                Logger.error("Invalid multi-record header checksum")
                break

            # Verify record checksum
            if current_offset + 5 + record_length <= len(data):
                record_sum = sum(data[current_offset + 5:current_offset + 5 + record_length]) & 0xFF
                if (record_sum + record_checksum) & 0xFF != 0:
                    Logger.error("Invalid multi-record data checksum")

                record_data = data[current_offset + 5:current_offset + 5 + record_length]

                records.append({
                    'type': record_type,
                    'format_version': format_version,
                    'length': record_length,
                    'data': record_data
                })

                # Check if this is the last record
                if not (format_version & 0x80):
                    break

                current_offset += 5 + record_length
            else:
                break

        return records

    def _parse_type_length_fields(self, data: bytes, start_offset: int, end_offset: int, max_fields: int = None) -> tuple:
        """Parse type/length fields.

        Args:
            data: FRU data bytes
            start_offset: Start offset of fields
            end_offset: End offset of fields (exclusive)
            max_fields: Maximum number of fields to parse

        Returns:
            Tuple of parsed fields and custom fields
        """
        fields = []
        custom_fields = []

        offset = start_offset
        field_count = 0

        while offset < end_offset:
            if max_fields is not None and field_count >= max_fields:
                # Parse remaining as custom fields
                while offset < end_offset:
                    type_length = data[offset]
                    if type_length == 0xC1:
                        # End of fields
                        offset += 1
                        break

                    field_type = type_length >> 6
                    field_length = type_length & 0x3F

                    if offset + 1 + field_length > end_offset:
                        break

                    if field_length > 0:
                        field_data = data[offset + 1:offset + 1 + field_length]

                        if field_type == 0:  # Binary
                            custom_fields.append({
                                'type': 'binary',
                                'data': field_data.hex()
                            })
                        elif field_type == 1:  # BCD plus
                            custom_fields.append({
                                'type': 'bcd_plus',
                                'data': ''.join([f"{b:02x}" for b in field_data])
                            })
                        elif field_type == 2:  # 6-bit ASCII
                            # 6-bit ASCII decoding is complex, simplify for now
                            custom_fields.append({
                                'type': '6bit_ascii',
                                'data': field_data.hex()
                            })
                        elif field_type == 3:  # 8-bit ASCII
                            try:
                                text = field_data.decode('ascii', errors='replace')
                                custom_fields.append({
                                    'type': 'ascii',
                                    'data': text
                                })
                            except UnicodeDecodeError:
                                custom_fields.append({
                                    'type': 'ascii',
                                    'data': field_data.hex()
                                })

                    offset += 1 + field_length

                break

            type_length = data[offset]
            if type_length == 0xC1:
                # End of fields
                offset += 1
                break

            field_type = type_length >> 6
            field_length = type_length & 0x3F

            if offset + 1 + field_length > end_offset:
                break

            field_value = ""
            if field_length > 0:
                field_data = data[offset + 1:offset + 1 + field_length]

                if field_type == 0:  # Binary
                    field_value = field_data.hex()
                elif field_type == 1:  # BCD plus
                    field_value = ''.join([f"{b:02x}" for b in field_data])
                elif field_type == 2:  # 6-bit ASCII
                    # 6-bit ASCII decoding is complex, simplify for now
                    field_value = field_data.hex()
                elif field_type == 3:  # 8-bit ASCII
                    try:
                        field_value = field_data.decode('ascii', errors='replace')
                    except UnicodeDecodeError:
                        field_value = field_data.hex()

            fields.append(field_value)
            field_count += 1
            offset += 1 + field_length

        # Pad fields with empty strings if needed
        if max_fields is not None:
            fields.extend([""] * (max_fields - len(fields)))

        return tuple(fields) + (custom_fields,)
