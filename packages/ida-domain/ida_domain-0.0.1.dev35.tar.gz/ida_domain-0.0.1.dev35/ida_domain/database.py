from __future__ import annotations

import inspect
import logging
from datetime import datetime
from typing import TYPE_CHECKING, Dict, Optional

import ida_ida
import ida_idaapi
import ida_kernwin
import ida_loader
import ida_nalt
from idadex import ea_t

from .basic_blocks import BasicBlocks
from .bytes import Bytes
from .comments import Comments
from .decorators import check_db_open
from .flirt import Flirt
from .functions import Functions
from .heads import Heads
from .ida_command_builder import IdaCommandBuilder
from .instructions import Instructions
from .names import Names
from .segments import Segments
from .strings import Strings
from .types import Types
from .xrefs import Xrefs
from .entries import Entries

if TYPE_CHECKING:
    from .basic_blocks import BasicBlocks
    from .instructions import Instructions


logger = logging.getLogger(__name__)


class Database:
    """
    Provides access and control over the loaded IDA database.
    """

    # List of property names that should be included in metadata
    _metadata_properties = [
        'path',
        'module',
        'base_address',
        'filesize',
        'md5',
        'sha256',
        'crc32',
        'architecture',
        'bitness',
        'format',
        'load_time',
    ]

    def __init__(self):
        """
        Constructs a new interface to the IDA database.

        Note:
            When running inside IDA, this refers to the currently open database.
            Use open() to load a new database when using IDA as a library.
        """

    def open(self, db_path: str, db_args: Optional[IdaCommandBuilder] = None) -> bool:
        """
        Opens a database from the specified file path.

        Args:
            db_path: Path to the input file.
            db_args: Command builder responsible for passing arguments to IDA kernel.

        Returns:
            True if the database was successfully opened, false otherwise.

        Note:
            This function is available only when running IDA as a library.
            When running inside the IDA GUI, simply construct a Database() instance
            to refer to the currently open database. Use is_open() to check if a
            database is loaded.
        """
        if ida_kernwin.is_ida_library(None, 0, None):
            run_auto_analysis = True if db_args is None else db_args.auto_analysis_enabled
            # We can open a new database only in the context of idalib
            import idapro

            res = idapro.open_database(
                db_path, run_auto_analysis, '' if db_args is None else db_args.build_args()
            )
            if res != 0:
                logger.error(
                    f'{inspect.currentframe().f_code.co_name}: Failed to open database {db_path}'
                )
                return False
            return True
        else:
            # No database available
            logger.error(
                f'{inspect.currentframe().f_code.co_name}: '
                f'Open is available only when running as a library.'
            )
            return False

    def is_open(self) -> bool:
        """
        Checks if the database is loaded.

        Returns:
            True if a database is open, false otherwise.
        """
        idb_path = ida_loader.get_path(ida_loader.PATH_TYPE_IDB)

        return idb_path is not None and len(idb_path) > 0

    @check_db_open
    def close(self, save: bool) -> None:
        """
        Closes the currently open database.

        Args:
            save: If true, saves changes before closing; otherwise, discards them.

        Note:
            This function is available only when running IDA as a library.
            When running inside the IDA GUI, we have no control on the database lifecycle.
        """
        if ida_kernwin.is_ida_library(None, 0, None):
            import idapro

            idapro.close_database(save)
        else:
            logger.error(
                f'{inspect.currentframe().f_code.co_name}: '
                f'Close is available only when running as a library.'
            )

    # Properties for Python-friendly access
    @property
    @check_db_open
    def entry_point(self) -> ea_t:
        """
        The entry point address of the binary.
        """
        return self.entries.get_at_index(0).address

    @property
    @check_db_open
    def current_ea(self) -> ea_t:
        """
        The current effective address (equivalent to the "screen EA" in IDA GUI).
        """
        return ida_kernwin.get_screen_ea()

    @current_ea.setter
    @check_db_open
    def current_ea(self, ea: int) -> None:
        """
        Sets the current effective address (equivalent to the "screen EA" in IDA GUI).
        """
        if ida_kernwin.is_ida_library(None, 0, None):
            import idapro

            idapro.set_screen_ea(ea)
        else:
            ida_kernwin.jumpto(ea)

    @property
    @check_db_open
    def minimum_ea(self) -> ea_t:
        """
        The minimum effective address from this database.
        """
        return ida_ida.inf_get_min_ea()

    @property
    @check_db_open
    def maximum_ea(self) -> ea_t:
        """
        The maximum effective address from this database.
        """
        return ida_ida.inf_get_max_ea()

    @property
    @check_db_open
    def base_address(self) -> Optional[ea_t]:
        """
        The image base address of this database.
        """
        base_addr = ida_nalt.get_imagebase()
        return base_addr if base_addr != ida_idaapi.BADADDR else None

    # Individual metadata properties
    @property
    @check_db_open
    def path(self) -> Optional[str]:
        """The input file path."""
        input_path = ida_nalt.get_input_file_path()
        return input_path if input_path else None

    @property
    @check_db_open
    def module(self) -> Optional[str]:
        """The module name."""
        module_name = ida_nalt.get_root_filename()
        return module_name if module_name else None

    @property
    @check_db_open
    def filesize(self) -> Optional[int]:
        """The input file size."""
        file_size = ida_nalt.retrieve_input_file_size()
        return file_size if file_size > 0 else None

    @property
    @check_db_open
    def md5(self) -> Optional[str]:
        """The MD5 hash of the input file."""
        md5_hash = ida_nalt.retrieve_input_file_md5()
        return md5_hash.hex() if md5_hash else None

    @property
    @check_db_open
    def sha256(self) -> Optional[str]:
        """The SHA256 hash of the input file."""
        sha256_hash = ida_nalt.retrieve_input_file_sha256()
        return sha256_hash.hex() if sha256_hash else None

    @property
    @check_db_open
    def crc32(self) -> Optional[int]:
        """The CRC32 checksum of the input file."""
        crc32 = ida_nalt.retrieve_input_file_crc32()
        return crc32 if crc32 != 0 else None

    @property
    @check_db_open
    def architecture(self) -> Optional[str]:
        """The processor architecture."""
        arch = ida_ida.inf_get_procname()
        return arch if arch else None

    @property
    @check_db_open
    def bitness(self) -> Optional[int]:
        """The application bitness (32/64)."""
        bitness = ida_ida.inf_get_app_bitness()
        return bitness if bitness > 0 else None

    @property
    @check_db_open
    def format(self) -> Optional[str]:
        """The file format type."""
        file_format = ida_loader.get_file_type_name()
        return file_format if file_format else None

    @property
    @check_db_open
    def load_time(self) -> Optional[str]:
        """The database load time."""
        ctime = ida_nalt.get_idb_ctime()
        return datetime.fromtimestamp(ctime).strftime('%Y-%m-%d %H:%M:%S') if ctime else None

    @property
    @check_db_open
    def metadata(self) -> Dict[str, str]:
        """
        Map of key-value metadata about the current database.
        Dynamically built from all metadata properties.
        """
        metadata = {}

        for prop_name in self._metadata_properties:
            try:
                value = getattr(self, prop_name)
                if value is not None:
                    if isinstance(value, int):
                        metadata[prop_name] = f'0x{value:x}'
                    else:
                        metadata[prop_name] = str(value)
            except Exception:
                # Skip properties that might fail to access
                continue

        return metadata

    @property
    def segments(self) -> Segments:
        """Handler that provides access to memory segment-related operations."""
        return Segments(self)

    @property
    def functions(self) -> Functions:
        """Handler that provides access to function-related operations."""
        return Functions(self)

    @property
    def basic_blocks(self) -> BasicBlocks:
        """Handler that provides access to basic block-related operations."""
        return BasicBlocks(self)

    @property
    def instructions(self) -> Instructions:
        """Handler that provides access to instruction-related operations."""
        return Instructions(self)

    @property
    def comments(self) -> Comments:
        """Handler that provides access to user comment-related operations."""
        return Comments(self)

    @property
    def entries(self) -> Entries:
        """Handler that provides access to entries operations."""
        return Entries(self)

    @property
    def heads(self) -> Heads:
        """Handler that provides access to user heads operations."""
        return Heads(self)

    @property
    def strings(self) -> Strings:
        """Handler that provides access to string-related operations."""
        return Strings(self)

    @property
    def names(self) -> Names:
        """Handler that provides access to name-related operations."""
        return Names(self)

    @property
    def types(self) -> Types:
        """Handler that provides access to type-related operations."""
        return Types(self)

    @property
    def bytes(self) -> Bytes:
        """Handler that provides access to byte-level memory operations."""
        return Bytes(self)

    @property
    def flirt(self) -> Flirt:
        """Handler that provides access to signature file operations."""
        return Flirt(self)

    @property
    def xrefs(self) -> Xrefs:
        """Handler that provides access to cross-reference (xref) operations."""
        return Xrefs(self)
