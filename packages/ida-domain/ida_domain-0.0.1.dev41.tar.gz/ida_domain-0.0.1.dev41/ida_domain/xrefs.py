from __future__ import annotations

import logging
from enum import Enum
from typing import TYPE_CHECKING

import ida_xref

from .decorators import check_db_open, decorate_all_methods

if TYPE_CHECKING:
    from .database import Database


logger = logging.getLogger(__name__)


_ref_types = {
    ida_xref.fl_U: 'Data_Unknown',
    ida_xref.dr_O: 'Data_Offset',
    ida_xref.dr_W: 'Data_Write',
    ida_xref.dr_R: 'Data_Read',
    ida_xref.dr_T: 'Data_Text',
    ida_xref.dr_I: 'Data_Informational',
    ida_xref.fl_CF: 'Code_Far_Call',
    ida_xref.fl_CN: 'Code_Near_Call',
    ida_xref.fl_JF: 'Code_Far_Jump',
    ida_xref.fl_JN: 'Code_Near_Jump',
    20: 'Code_User',
    ida_xref.fl_F: 'Ordinary_Flow',
}


class XrefsKind(Enum):
    """
    Enumeration for IDA Xrefs types.
    """

    CODE = 'code'
    DATA = 'data'
    ALL = 'all'


@decorate_all_methods(check_db_open)
class Xrefs:
    """
    Provides access to cross-reference (xref) analysis in the IDA database.
    """

    def __init__(self, database: 'Database'):
        """
        Constructs a xrefs handler for the given database.

        Args:
            database: Reference to the active IDA database.
        """
        self.m_database = database

    def get_to(self, ea: int, kind: XrefsKind = XrefsKind.ALL, flow: bool = True):
        """
        Creates an iterator over all xrefs pointing to a given address.

        Args:
            ea: Target effective address.
            kind: Xrefs kind (defaults to XrefsKind.ALL).
            flow: Follow normal code flow or not (defaults to True).

        Returns:
            An iterator over references to input target addresses.
        """
        xref = ida_xref.xrefblk_t()
        if kind == XrefsKind.CODE:
            if flow:
                yield from xref.crefs_to(ea)
            else:
                yield from xref.fcrefs_to(ea)

        elif kind == XrefsKind.DATA:
            yield from xref.drefs_to(ea)

        elif kind == XrefsKind.ALL:
            success = xref.first_to(ea, ida_xref.XREF_ALL)

            while success:
                yield xref
                success = xref.next_to()

    def get_from(self, ea: int, kind: XrefsKind = XrefsKind.ALL, flow: bool = False):
        """
        Creates an iterator over all xrefs originating from a given address.

        Args:
            ea: Source effective address.
            kind: Xrefs kind (defaults to XrefsKind.ALL).
            flow: Follow normal code flow or not (defaults to True).

        Returns:
            An iterator over outgoing xrefs.
        """
        xref = ida_xref.xrefblk_t()
        if kind == XrefsKind.CODE:
            if flow:
                yield from xref.crefs_from(ea)
            else:
                yield from xref.fcrefs_from(ea)

        elif kind == XrefsKind.DATA:
            yield from xref.drefs_from(ea)

        elif kind == XrefsKind.ALL:
            success = xref.first_from(ea, ida_xref.XREF_ALL)

            while success:
                yield xref
                success = xref.next_from()

    def get_name(self, ref: ida_xref.xrefblk_t()):
        """
        Get human-readable xref type name.

        Args:
            ref: A xref block.

        Returns:
            A human-readable xref type name.
        """
        return _ref_types.get(ref.type, 'Unknown')
