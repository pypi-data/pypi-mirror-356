from __future__ import annotations

import logging
import struct
from typing import TYPE_CHECKING

import ida_bytes
import ida_ida
import ida_lines

from .decorators import check_db_open, decorate_all_methods

if TYPE_CHECKING:
    from .database import Database


logger = logging.getLogger(__name__)


@decorate_all_methods(check_db_open)
class Bytes:
    """
    Handles operations related to raw data access from the IDA database.

    This class provides methods to read various data types (bytes, words, floats, etc.)
    from memory addresses in the disassembled binary.
    """

    def __init__(self, database: 'Database'):
        """
        Constructs a bytes handler for the given database.

        Args:
            database: Reference to the active IDA database.
        """
        self.m_database = database

    def _log_error(self, method_name: str, ea: int, message: str = 'Failed to read data') -> None:
        """
        Helper method to log errors consistently.

        Args:
            method_name: Name of the method where the error occurred.
            ea: The effective address where the error occurred.
            message: Custom error message.
        """
        logger.error(f'{method_name}: {message} from address 0x{ea:x}')

    def get_byte(self, ea: int) -> int | None:
        """
        Retrieves a single byte (8 bits) at the specified address.

        Args:
            ea: The effective address.

        Returns:
            The byte value (0-255), or None if an error occurs.
        """
        try:
            return ida_bytes.get_byte(ea)
        except Exception:
            self._log_error('get_byte', ea)
            return None

    def get_word(self, ea: int) -> int | None:
        """
        Retrieves a word (16 bits/2 bytes) at the specified address.

        Args:
            ea: The effective address.

        Returns:
            The word value, or None if an error occurs.
        """
        try:
            return ida_bytes.get_word(ea)
        except Exception:
            self._log_error('get_word', ea)
            return None

    def get_dword(self, ea: int) -> int | None:
        """
        Retrieves a double word (32 bits/4 bytes) at the specified address.

        Args:
            ea: The effective address.

        Returns:
            The dword value, or None if an error occurs.
        """
        try:
            return ida_bytes.get_dword(ea)
        except Exception:
            self._log_error('get_dword', ea)
            return None

    def get_qword(self, ea: int) -> int | None:
        """
        Retrieves a quad word (64 bits/8 bytes) at the specified address.

        Args:
            ea: The effective address.

        Returns:
            The qword value, or None if an error occurs.
        """
        try:
            return ida_bytes.get_qword(ea)
        except Exception:
            self._log_error('get_qword', ea)
            return None

    def _read_floating_point(self, ea: int, data_flags: int, method_name: str) -> float | None:
        """
        Helper method to read floating-point values from memory.

        Args:
            ea: The effective address.
            data_flags: Data flags - float flags or double flags.
            method_name: Name of the calling method for error reporting.

        Returns:
            The floating-point value, or None if an error occurs.
        """
        try:
            # Get data element size for the floating-point type
            size = ida_bytes.get_data_elsize(ea, data_flags)
        except Exception:
            self._log_error(method_name, ea, 'Failed to get data element size')
            return None

        if size <= 0 or size > 16:
            self._log_error(method_name, ea, f'Invalid size {size} for floating-point data')
            return None

        # Read bytes from address
        data = ida_bytes.get_bytes(ea, size)
        if data is None or len(data) != size:
            self._log_error(method_name, ea, 'Failed to read bytes')
            return None

        # Convert bytes to floating-point value
        try:
            # Get processor endianness
            is_little_endian = not ida_ida.inf_is_be()
            endian = '<' if is_little_endian else '>'

            if size == 4:
                # IEEE 754 single precision (32-bit float)
                return struct.unpack(f'{endian}f', data)[0]
            elif size == 8:
                # IEEE 754 double precision (64-bit double)
                return struct.unpack(f'{endian}d', data)[0]
            else:
                self._log_error(method_name, ea, f'Unsupported floating-point size: {size}')
                return None

        except (struct.error, ValueError, OverflowError) as e:
            self._log_error(method_name, ea, f'Failed to convert bytes to floating-point: {e}')
            return None

    def get_float(self, ea: int) -> float | None:
        """
        Retrieves a single-precision floating-point value at the specified address.

        Args:
            ea: The effective address.

        Returns:
            The float value, or None if an error occurs.
        """
        return self._read_floating_point(ea, ida_bytes.float_flag(), 'get_float')

    def get_double(self, ea: int) -> float | None:
        """
        Retrieves a double-precision floating-point value at the specified address.

        Args:
            ea: The effective address.

        Returns:
            The double value, or None if an error occurs.
        """
        return self._read_floating_point(ea, ida_bytes.double_flag(), 'get_double')

    def get_disassembly(self, ea: int) -> str | None:
        """
        Retrieves the disassembly text at the specified address.

        Args:
            ea: The effective address.

        Returns:
            The disassembly string, or None if an error occurs.
        """
        try:
            # Generate disassembly line with multi-line and remove tags flags
            line = ida_lines.generate_disasm_line(
                ea, ida_lines.GENDSM_MULTI_LINE | ida_lines.GENDSM_REMOVE_TAGS
            )
            if line:
                return line
            else:
                self._log_error('get_disassembly', ea, 'Failed to generate disassembly line')
                return None
        except Exception:
            self._log_error('get_disassembly', ea, 'Exception while generating disassembly line')
            return None
