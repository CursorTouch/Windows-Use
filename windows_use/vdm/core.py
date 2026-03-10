"""Virtual Desktop Manager - Windows COM API wrapper.

Supports Windows 10 (17763+) and all Windows 11 versions (21H2 through 24H2+).
Uses undocumented internal COM interfaces whose GUIDs and vtable layouts
change between Windows builds.

Reference: https://github.com/FuPeiJiang/Windows-BuildNumber-VirtualDesktop
"""

import ctypes
import logging
import sys
import threading
from ctypes import HRESULT, POINTER, byref, c_void_p
from ctypes.wintypes import BOOL, HWND, UINT

import comtypes.client
from comtypes import COMMETHOD, GUID, IUnknown, STDMETHOD

logger = logging.getLogger(__name__)

_thread_local = threading.local()


def _get_manager():
    if not hasattr(_thread_local, "manager"):
        _thread_local.manager = VirtualDesktopManager()
    return _thread_local.manager


def is_window_on_current_desktop(hwnd: int) -> bool:
    return _get_manager().is_window_on_current_desktop(hwnd)


def get_window_desktop_id(hwnd: int) -> str:
    return _get_manager().get_window_desktop_id(hwnd)


def move_window_to_desktop(hwnd: int, desktop_id: str):
    _get_manager().move_window_to_desktop(hwnd, desktop_id)


# =============================================================================
# Standard COM CLSIDs (stable across all Windows versions)
# =============================================================================

CLSID_VirtualDesktopManager = GUID("{aa509086-5ca9-4c25-8f95-589d3c07b48a}")
CLSID_ImmersiveShell = GUID("{C2F03A33-21F5-47FA-B4BB-156362A2F239}")
CLSID_VirtualDesktopManagerInternal = GUID("{C5E0CDCA-7B6E-41B2-9FC4-D93975CC467B}")
IID_IServiceProvider = GUID("{6D5140C1-7436-11CE-8034-00AA006009FA}")

# =============================================================================
# Public IVirtualDesktopManager (documented, stable across all versions)
# =============================================================================


class IVirtualDesktopManager(IUnknown):
    _iid_ = GUID("{a5cd92ff-29be-454c-8d04-d82879fb3f1b}")
    _methods_ = [
        COMMETHOD(
            [],
            HRESULT,
            "IsWindowOnCurrentVirtualDesktop",
            (["in"], HWND, "topLevelWindow"),
            (["out", "retval"], POINTER(BOOL), "onCurrentDesktop"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetWindowDesktopId",
            (["in"], HWND, "topLevelWindow"),
            (["out", "retval"], POINTER(GUID), "desktopId"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "MoveWindowToDesktop",
            (["in"], HWND, "topLevelWindow"),
            (["in"], POINTER(GUID), "desktopId"),
        ),
    ]


class IServiceProvider(IUnknown):
    _iid_ = IID_IServiceProvider
    _methods_ = [
        COMMETHOD(
            [],
            HRESULT,
            "QueryService",
            (["in"], POINTER(GUID), "guidService"),
            (["in"], POINTER(GUID), "riid"),
            (["out"], POINTER(POINTER(IUnknown)), "ppvObject"),
        ),
    ]


class IObjectArray(IUnknown):
    _iid_ = GUID("{92CA9DCD-5622-4BBA-A805-5E9F541BD8CC}")
    _methods_ = [
        COMMETHOD(
            [],
            HRESULT,
            "GetCount",
            (["out"], POINTER(UINT), "pcObjects"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetAt",
            (["in"], UINT, "uiIndex"),
            (["in"], POINTER(GUID), "riid"),
            (["out"], POINTER(POINTER(IUnknown)), "ppv"),
        ),
    ]


# =============================================================================
# HSTRING utilities for WinRT string operations
# =============================================================================


class HSTRING(c_void_p):
    pass


try:
    _combase = ctypes.windll.combase
    _WindowsCreateString = _combase.WindowsCreateString
    _WindowsCreateString.argtypes = [ctypes.c_wchar_p, UINT, POINTER(HSTRING)]
    _WindowsCreateString.restype = HRESULT
    _WindowsDeleteString = _combase.WindowsDeleteString
    _WindowsDeleteString.argtypes = [HSTRING]
    _WindowsDeleteString.restype = HRESULT
except Exception:
    _WindowsCreateString = None
    _WindowsDeleteString = None


def create_hstring(text: str) -> HSTRING:
    """Create an HSTRING from a Python string."""
    if not _WindowsCreateString:
        return HSTRING(0)
    hs = HSTRING()
    hr = _WindowsCreateString(text, len(text), byref(hs))
    if hr != 0:
        raise OSError(f"WindowsCreateString failed: {hr}")
    return hs


def delete_hstring(hs: HSTRING):
    """Delete an HSTRING."""
    if _WindowsDeleteString and hs:
        _WindowsDeleteString(hs)


# =============================================================================
# Build detection
#
# The internal COM GUIDs change not just between major builds but also between
# revision numbers (UBR). We need both BUILD and UBR for precise matching.
# =============================================================================

BUILD = sys.getwindowsversion().build


def _get_ubr() -> int:
    """Get Update Build Revision from the Windows registry."""
    try:
        import winreg

        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows NT\CurrentVersion",
        )
        ubr, _ = winreg.QueryValueEx(key, "UBR")
        winreg.CloseKey(key)
        return ubr
    except Exception:
        return 0


UBR = _get_ubr()
_BUILD_TUPLE = (BUILD, UBR)

logger.debug(f"[VDM] Windows Build: {BUILD}.{UBR}")

# =============================================================================
# Version group determination
#
# The undocumented internal COM interface GUIDs and vtable layouts change
# between builds. We group builds by their interface characteristics.
#
# Reference: https://github.com/FuPeiJiang/Windows-BuildNumber-VirtualDesktop
#
# Groups:
#   WIN10        - Build < 22000 (Windows 10 / Server 2022)
#                  No HMONITOR params, no SetName, no MoveDesktop
#   WIN11_21H2   - 22000 <= Build < 22483
#                  HMONITOR params, has SetName
#   WIN11_22H2_E - 22483 <= Build(,UBR) < (22621,2215)
#                  HMONITOR params, has SetName, GetAllCurrentDesktops added
#   WIN11_22H2_L - (22621,2215) <= Build(,UBR) < (22631,3085)
#                  No HMONITOR params, has SetName (new GUIDs)
#   WIN11_23H2   - (22631,3085) <= Build < 26100
#                  No HMONITOR params, has SetName (new GUIDs again)
#   WIN11_24H2   - Build >= 26100
#                  No HMONITOR params, has SetName,
#                  SwitchDesktopAndMoveForegroundView added
# =============================================================================

if BUILD >= 26100:
    _VER = "WIN11_24H2"
elif _BUILD_TUPLE >= (22631, 3085):
    _VER = "WIN11_23H2"
elif _BUILD_TUPLE >= (22621, 2215):
    _VER = "WIN11_22H2_L"
elif BUILD >= 22483:
    _VER = "WIN11_22H2_E"
elif BUILD >= 22000:
    _VER = "WIN11_21H2"
else:
    _VER = "WIN10"

logger.debug(f"[VDM] Version group: {_VER}")

# Whether methods on the internal manager require an HMONITOR parameter
_USES_HMONITOR = _VER in ("WIN11_21H2", "WIN11_22H2_E")

# Whether SetName (rename desktop) is supported
_HAS_SET_NAME = _VER != "WIN10"

# =============================================================================
# Interface IIDs based on version group
# =============================================================================

_IID_MAP = {
    "WIN10": {
        "ManagerInternal": GUID("{F31574D6-B682-4CDC-BD56-1827860ABEC6}"),
        "Desktop": GUID("{FF72FFDD-BE7E-43FC-9C03-AD81681E88E4}"),
    },
    "WIN11_21H2": {
        "ManagerInternal": GUID("{B2F925B9-5A0F-4D2E-9F4D-2B1507593C10}"),
        "Desktop": GUID("{536D3495-B208-4CC9-AE26-DE8111275BF8}"),
    },
    "WIN11_22H2_E": {
        # Same GUIDs as 21H2 but different vtable layout
        "ManagerInternal": GUID("{B2F925B9-5A0F-4D2E-9F4D-2B1507593C10}"),
        "Desktop": GUID("{536D3495-B208-4CC9-AE26-DE8111275BF8}"),
    },
    "WIN11_22H2_L": {
        "ManagerInternal": GUID("{4970BA3D-FD4E-4647-BEA3-D89076EF4B9C}"),
        "Desktop": GUID("{A3175F2D-239C-4BD2-8AA0-EEBA8B0B138E}"),
    },
    "WIN11_23H2": {
        "ManagerInternal": GUID("{53F5CA0B-158F-4124-900C-057158060B27}"),
        "Desktop": GUID("{3F07F4BE-B107-441A-AF0F-39D82529072C}"),
    },
    "WIN11_24H2": {
        # Uses IVirtualDesktopManagerInternal2 IID on this build
        "ManagerInternal": GUID("{53F5CA0B-158F-4124-900C-057158060B27}"),
        "Desktop": GUID("{3F07F4BE-B107-441A-AF0F-39D82529072C}"),
    },
}

IID_IVirtualDesktopManagerInternal = _IID_MAP[_VER]["ManagerInternal"]
IID_IVirtualDesktop = _IID_MAP[_VER]["Desktop"]

# =============================================================================
# IVirtualDesktop interface
#
# Only GetID() is used by the VirtualDesktopManager wrapper.
# GetID is always at vtable index 4 (slot 1 after IUnknown) in ALL versions,
# so we use a minimal 2-method definition that works across all builds.
# =============================================================================


class IVirtualDesktop(IUnknown):
    _iid_ = IID_IVirtualDesktop
    _methods_ = [
        STDMETHOD(HRESULT, "IsViewVisible", (POINTER(IUnknown), POINTER(UINT))),
        COMMETHOD([], HRESULT, "GetID", (["out"], POINTER(GUID), "pGuid")),
    ]


# Placeholder for IApplicationView (used in method signatures but never called)
class IApplicationView(IUnknown):
    _iid_ = GUID("{372E1D3B-38D3-42E4-A15B-8AB2B178F513}")


# =============================================================================
# IVirtualDesktopManagerInternal interface
#
# The vtable layout changes significantly between Windows builds.
# Key differences:
#   - Win10: No HMONITOR params, no MoveDesktop, no SetName
#   - Win11 21H2: HMONITOR params on GetCount/GetCurrent/GetDesktops/Switch/Create
#   - Win11 22H2 early: Same as 21H2 + GetAllCurrentDesktops inserted at idx 7
#   - Win11 22H2 late / 23H2: HMONITOR params removed
#   - Win11 24H2: SwitchDesktopAndMoveForegroundView added at idx 10
# =============================================================================


class IVirtualDesktopManagerInternal(IUnknown):
    _iid_ = IID_IVirtualDesktopManagerInternal

    if _VER == "WIN10":
        _methods_ = [
            # 3: GetCount()
            COMMETHOD([], HRESULT, "GetCount", (["out"], POINTER(UINT), "pCount")),
            # 4: MoveViewToDesktop
            STDMETHOD(
                HRESULT,
                "MoveViewToDesktop",
                (POINTER(IApplicationView), POINTER(IVirtualDesktop)),
            ),
            # 5: CanViewMoveDesktops
            STDMETHOD(
                HRESULT,
                "CanViewMoveDesktops",
                (POINTER(IApplicationView), POINTER(UINT)),
            ),
            # 6: GetCurrentDesktop
            COMMETHOD(
                [],
                HRESULT,
                "GetCurrentDesktop",
                (["out"], POINTER(POINTER(IVirtualDesktop)), "pDesktop"),
            ),
            # 7: GetDesktops
            COMMETHOD(
                [],
                HRESULT,
                "GetDesktops",
                (["out"], POINTER(POINTER(IObjectArray)), "array"),
            ),
            # 8: GetAdjacentDesktop
            STDMETHOD(
                HRESULT,
                "GetAdjacentDesktop",
                (POINTER(IVirtualDesktop), UINT, POINTER(POINTER(IVirtualDesktop))),
            ),
            # 9: SwitchDesktop
            STDMETHOD(HRESULT, "SwitchDesktop", (POINTER(IVirtualDesktop),)),
            # 10: CreateDesktopW
            COMMETHOD(
                [],
                HRESULT,
                "CreateDesktopW",
                (["out"], POINTER(POINTER(IVirtualDesktop)), "pDesktop"),
            ),
            # 11: RemoveDesktop
            COMMETHOD(
                [],
                HRESULT,
                "RemoveDesktop",
                (["in"], POINTER(IVirtualDesktop), "destroyDesktop"),
                (["in"], POINTER(IVirtualDesktop), "fallbackDesktop"),
            ),
            # 12: FindDesktop
            COMMETHOD(
                [],
                HRESULT,
                "FindDesktop",
                (["in"], POINTER(GUID), "pGuid"),
                (["out"], POINTER(POINTER(IVirtualDesktop)), "pDesktop"),
            ),
            # No SetName on Windows 10
        ]

    elif _VER == "WIN11_21H2":
        _methods_ = [
            # 3: GetCount(hMon)
            COMMETHOD(
                [],
                HRESULT,
                "GetCount",
                (["in"], HWND, "hMon"),
                (["out"], POINTER(UINT), "pCount"),
            ),
            # 4: MoveViewToDesktop
            STDMETHOD(
                HRESULT,
                "MoveViewToDesktop",
                (POINTER(IApplicationView), POINTER(IVirtualDesktop)),
            ),
            # 5: CanViewMoveDesktops
            STDMETHOD(
                HRESULT,
                "CanViewMoveDesktops",
                (POINTER(IApplicationView), POINTER(UINT)),
            ),
            # 6: GetCurrentDesktop(hMon)
            COMMETHOD(
                [],
                HRESULT,
                "GetCurrentDesktop",
                (["in"], HWND, "hMon"),
                (["out"], POINTER(POINTER(IVirtualDesktop)), "pDesktop"),
            ),
            # 7: GetDesktops(hMon)
            COMMETHOD(
                [],
                HRESULT,
                "GetDesktops",
                (["in"], HWND, "hMon"),
                (["out"], POINTER(POINTER(IObjectArray)), "array"),
            ),
            # 8: GetAdjacentDesktop
            STDMETHOD(
                HRESULT,
                "GetAdjacentDesktop",
                (POINTER(IVirtualDesktop), UINT, POINTER(POINTER(IVirtualDesktop))),
            ),
            # 9: SwitchDesktop(hMon, desktop)
            STDMETHOD(HRESULT, "SwitchDesktop", (HWND, POINTER(IVirtualDesktop))),
            # 10: CreateDesktopW(hMon)
            COMMETHOD(
                [],
                HRESULT,
                "CreateDesktopW",
                (["in"], HWND, "hMon"),
                (["out"], POINTER(POINTER(IVirtualDesktop)), "pDesktop"),
            ),
            # 11: MoveDesktop(desktop, hMon, index)
            STDMETHOD(
                HRESULT, "MoveDesktop", (POINTER(IVirtualDesktop), HWND, UINT)
            ),
            # 12: RemoveDesktop
            COMMETHOD(
                [],
                HRESULT,
                "RemoveDesktop",
                (["in"], POINTER(IVirtualDesktop), "destroyDesktop"),
                (["in"], POINTER(IVirtualDesktop), "fallbackDesktop"),
            ),
            # 13: FindDesktop
            COMMETHOD(
                [],
                HRESULT,
                "FindDesktop",
                (["in"], POINTER(GUID), "pGuid"),
                (["out"], POINTER(POINTER(IVirtualDesktop)), "pDesktop"),
            ),
            # 14: GetDesktopSwitchIncludeExcludeViews
            STDMETHOD(
                HRESULT,
                "GetDesktopSwitchIncludeExcludeViews",
                (
                    POINTER(IVirtualDesktop),
                    POINTER(POINTER(IObjectArray)),
                    POINTER(POINTER(IObjectArray)),
                ),
            ),
            # 15: SetName
            COMMETHOD(
                [],
                HRESULT,
                "SetName",
                (["in"], POINTER(IVirtualDesktop), "pDesktop"),
                (["in"], HSTRING, "name"),
            ),
        ]

    elif _VER == "WIN11_22H2_E":
        # Same GUIDs as 21H2 but GetAllCurrentDesktops is inserted at index 7,
        # shifting GetDesktops and subsequent methods by one slot.
        _methods_ = [
            # 3: GetCount(hMon)
            COMMETHOD(
                [],
                HRESULT,
                "GetCount",
                (["in"], HWND, "hMon"),
                (["out"], POINTER(UINT), "pCount"),
            ),
            # 4: MoveViewToDesktop
            STDMETHOD(
                HRESULT,
                "MoveViewToDesktop",
                (POINTER(IApplicationView), POINTER(IVirtualDesktop)),
            ),
            # 5: CanViewMoveDesktops
            STDMETHOD(
                HRESULT,
                "CanViewMoveDesktops",
                (POINTER(IApplicationView), POINTER(UINT)),
            ),
            # 6: GetCurrentDesktop(hMon)
            COMMETHOD(
                [],
                HRESULT,
                "GetCurrentDesktop",
                (["in"], HWND, "hMon"),
                (["out"], POINTER(POINTER(IVirtualDesktop)), "pDesktop"),
            ),
            # 7: GetAllCurrentDesktops (NEW in 22483)
            COMMETHOD(
                [],
                HRESULT,
                "GetAllCurrentDesktops",
                (["out"], POINTER(POINTER(IObjectArray)), "array"),
            ),
            # 8: GetDesktops(hMon) - SHIFTED from idx 7
            COMMETHOD(
                [],
                HRESULT,
                "GetDesktops",
                (["in"], HWND, "hMon"),
                (["out"], POINTER(POINTER(IObjectArray)), "array"),
            ),
            # 9: GetAdjacentDesktop
            STDMETHOD(
                HRESULT,
                "GetAdjacentDesktop",
                (POINTER(IVirtualDesktop), UINT, POINTER(POINTER(IVirtualDesktop))),
            ),
            # 10: SwitchDesktop(hMon, desktop)
            STDMETHOD(HRESULT, "SwitchDesktop", (HWND, POINTER(IVirtualDesktop))),
            # 11: CreateDesktopW(hMon)
            COMMETHOD(
                [],
                HRESULT,
                "CreateDesktopW",
                (["in"], HWND, "hMon"),
                (["out"], POINTER(POINTER(IVirtualDesktop)), "pDesktop"),
            ),
            # 12: MoveDesktop(desktop, hMon, index)
            STDMETHOD(
                HRESULT, "MoveDesktop", (POINTER(IVirtualDesktop), HWND, UINT)
            ),
            # 13: RemoveDesktop
            COMMETHOD(
                [],
                HRESULT,
                "RemoveDesktop",
                (["in"], POINTER(IVirtualDesktop), "destroyDesktop"),
                (["in"], POINTER(IVirtualDesktop), "fallbackDesktop"),
            ),
            # 14: FindDesktop
            COMMETHOD(
                [],
                HRESULT,
                "FindDesktop",
                (["in"], POINTER(GUID), "pGuid"),
                (["out"], POINTER(POINTER(IVirtualDesktop)), "pDesktop"),
            ),
            # 15: GetDesktopSwitchIncludeExcludeViews
            STDMETHOD(
                HRESULT,
                "GetDesktopSwitchIncludeExcludeViews",
                (
                    POINTER(IVirtualDesktop),
                    POINTER(POINTER(IObjectArray)),
                    POINTER(POINTER(IObjectArray)),
                ),
            ),
            # 16: SetName
            COMMETHOD(
                [],
                HRESULT,
                "SetName",
                (["in"], POINTER(IVirtualDesktop), "pDesktop"),
                (["in"], HSTRING, "name"),
            ),
        ]

    elif _VER in ("WIN11_22H2_L", "WIN11_23H2"):
        # HMONITOR params removed, cleaner interface
        _methods_ = [
            # 3: GetCount
            COMMETHOD([], HRESULT, "GetCount", (["out"], POINTER(UINT), "pCount")),
            # 4: MoveViewToDesktop
            STDMETHOD(
                HRESULT,
                "MoveViewToDesktop",
                (POINTER(IApplicationView), POINTER(IVirtualDesktop)),
            ),
            # 5: CanViewMoveDesktops
            STDMETHOD(
                HRESULT,
                "CanViewMoveDesktops",
                (POINTER(IApplicationView), POINTER(UINT)),
            ),
            # 6: GetCurrentDesktop
            COMMETHOD(
                [],
                HRESULT,
                "GetCurrentDesktop",
                (["out"], POINTER(POINTER(IVirtualDesktop)), "pDesktop"),
            ),
            # 7: GetDesktops
            COMMETHOD(
                [],
                HRESULT,
                "GetDesktops",
                (["out"], POINTER(POINTER(IObjectArray)), "array"),
            ),
            # 8: GetAdjacentDesktop
            STDMETHOD(
                HRESULT,
                "GetAdjacentDesktop",
                (POINTER(IVirtualDesktop), UINT, POINTER(POINTER(IVirtualDesktop))),
            ),
            # 9: SwitchDesktop
            STDMETHOD(HRESULT, "SwitchDesktop", (POINTER(IVirtualDesktop),)),
            # 10: CreateDesktopW
            COMMETHOD(
                [],
                HRESULT,
                "CreateDesktopW",
                (["out"], POINTER(POINTER(IVirtualDesktop)), "pDesktop"),
            ),
            # 11: MoveDesktop
            STDMETHOD(HRESULT, "MoveDesktop", (POINTER(IVirtualDesktop), UINT)),
            # 12: RemoveDesktop
            COMMETHOD(
                [],
                HRESULT,
                "RemoveDesktop",
                (["in"], POINTER(IVirtualDesktop), "destroyDesktop"),
                (["in"], POINTER(IVirtualDesktop), "fallbackDesktop"),
            ),
            # 13: FindDesktop
            COMMETHOD(
                [],
                HRESULT,
                "FindDesktop",
                (["in"], POINTER(GUID), "pGuid"),
                (["out"], POINTER(POINTER(IVirtualDesktop)), "pDesktop"),
            ),
            # 14: GetDesktopSwitchIncludeExcludeViews
            STDMETHOD(
                HRESULT,
                "GetDesktopSwitchIncludeExcludeViews",
                (
                    POINTER(IVirtualDesktop),
                    POINTER(POINTER(IObjectArray)),
                    POINTER(POINTER(IObjectArray)),
                ),
            ),
            # 15: SetName
            COMMETHOD(
                [],
                HRESULT,
                "SetName",
                (["in"], POINTER(IVirtualDesktop), "pDesktop"),
                (["in"], HSTRING, "name"),
            ),
        ]

    elif _VER == "WIN11_24H2":
        # SwitchDesktopAndMoveForegroundView added at idx 10, shifting
        # CreateDesktopW and subsequent methods by one slot.
        _methods_ = [
            # 3: GetCount
            COMMETHOD([], HRESULT, "GetCount", (["out"], POINTER(UINT), "pCount")),
            # 4: MoveViewToDesktop
            STDMETHOD(
                HRESULT,
                "MoveViewToDesktop",
                (POINTER(IApplicationView), POINTER(IVirtualDesktop)),
            ),
            # 5: CanViewMoveDesktops
            STDMETHOD(
                HRESULT,
                "CanViewMoveDesktops",
                (POINTER(IApplicationView), POINTER(UINT)),
            ),
            # 6: GetCurrentDesktop
            COMMETHOD(
                [],
                HRESULT,
                "GetCurrentDesktop",
                (["out"], POINTER(POINTER(IVirtualDesktop)), "pDesktop"),
            ),
            # 7: GetDesktops
            COMMETHOD(
                [],
                HRESULT,
                "GetDesktops",
                (["out"], POINTER(POINTER(IObjectArray)), "array"),
            ),
            # 8: GetAdjacentDesktop
            STDMETHOD(
                HRESULT,
                "GetAdjacentDesktop",
                (POINTER(IVirtualDesktop), UINT, POINTER(POINTER(IVirtualDesktop))),
            ),
            # 9: SwitchDesktop
            STDMETHOD(HRESULT, "SwitchDesktop", (POINTER(IVirtualDesktop),)),
            # 10: SwitchDesktopAndMoveForegroundView (NEW in 24H2)
            STDMETHOD(
                HRESULT,
                "SwitchDesktopAndMoveForegroundView",
                (POINTER(IVirtualDesktop),),
            ),
            # 11: CreateDesktopW
            COMMETHOD(
                [],
                HRESULT,
                "CreateDesktopW",
                (["out"], POINTER(POINTER(IVirtualDesktop)), "pDesktop"),
            ),
            # 12: MoveDesktop
            STDMETHOD(HRESULT, "MoveDesktop", (POINTER(IVirtualDesktop), UINT)),
            # 13: RemoveDesktop
            COMMETHOD(
                [],
                HRESULT,
                "RemoveDesktop",
                (["in"], POINTER(IVirtualDesktop), "destroyDesktop"),
                (["in"], POINTER(IVirtualDesktop), "fallbackDesktop"),
            ),
            # 14: FindDesktop
            COMMETHOD(
                [],
                HRESULT,
                "FindDesktop",
                (["in"], POINTER(GUID), "pGuid"),
                (["out"], POINTER(POINTER(IVirtualDesktop)), "pDesktop"),
            ),
            # 15: GetDesktopSwitchIncludeExcludeViews
            STDMETHOD(
                HRESULT,
                "GetDesktopSwitchIncludeExcludeViews",
                (
                    POINTER(IVirtualDesktop),
                    POINTER(POINTER(IObjectArray)),
                    POINTER(POINTER(IObjectArray)),
                ),
            ),
            # 16: SetName
            COMMETHOD(
                [],
                HRESULT,
                "SetName",
                (["in"], POINTER(IVirtualDesktop), "pDesktop"),
                (["in"], HSTRING, "name"),
            ),
        ]


# =============================================================================
# VirtualDesktopManager wrapper class
# =============================================================================


class VirtualDesktopManager:
    """Wrapper around the Windows Virtual Desktop COM interfaces.

    Supports Windows 10 (17763+) and all Windows 11 versions.
    Handles HMONITOR parameter differences between build groups transparently.
    """

    def __init__(self):
        self._manager = None
        self._internal_manager = None
        self._uses_hmonitor = _USES_HMONITOR
        self._has_set_name = _HAS_SET_NAME

        try:
            ctypes.windll.ole32.CoInitialize(None)
        except Exception:
            pass

        try:
            self._manager = comtypes.client.CreateObject(
                CLSID_VirtualDesktopManager, interface=IVirtualDesktopManager
            )

            try:
                service_provider = comtypes.client.CreateObject(
                    CLSID_ImmersiveShell, interface=IServiceProvider
                )
                unk = service_provider.QueryService(
                    byref(CLSID_VirtualDesktopManagerInternal),
                    byref(IVirtualDesktopManagerInternal._iid_),
                )
                self._internal_manager = unk.QueryInterface(
                    IVirtualDesktopManagerInternal
                )
            except Exception as e:
                logger.warning(
                    f"Failed to initialize VirtualDesktopManagerInternal: {e}"
                )
                self._internal_manager = None

        except Exception as e:
            logger.error(f"Failed to initialize VirtualDesktopManager: {e}")

    # -------------------------------------------------------------------------
    # Internal helpers for HMONITOR-aware method calls
    #
    # Builds 22000-22621.2214 require an HMONITOR parameter for several
    # methods. We pass 0 (NULL) to use the primary monitor.
    # -------------------------------------------------------------------------

    def _get_desktops(self):
        """Get IObjectArray of all virtual desktops."""
        if self._uses_hmonitor:
            return self._internal_manager.GetDesktops(0)
        return self._internal_manager.GetDesktops()

    def _get_current_desktop_raw(self):
        """Get the current IVirtualDesktop."""
        if self._uses_hmonitor:
            return self._internal_manager.GetCurrentDesktop(0)
        return self._internal_manager.GetCurrentDesktop()

    def _create_desktop_raw(self):
        """Create a new IVirtualDesktop."""
        if self._uses_hmonitor:
            return self._internal_manager.CreateDesktopW(0)
        return self._internal_manager.CreateDesktopW()

    def _switch_desktop_raw(self, desktop):
        """Switch to the specified IVirtualDesktop."""
        if self._uses_hmonitor:
            self._internal_manager.SwitchDesktop(0, desktop)
        else:
            self._internal_manager.SwitchDesktop(desktop)

    # -------------------------------------------------------------------------
    # Public IVirtualDesktopManager methods (stable across all versions)
    # -------------------------------------------------------------------------

    def is_window_on_current_desktop(self, hwnd: int) -> bool:
        """Check if a window is on the currently active virtual desktop."""
        if not self._manager:
            return True
        try:
            return self._manager.IsWindowOnCurrentVirtualDesktop(hwnd)
        except Exception:
            return True

    def get_window_desktop_id(self, hwnd: int) -> str:
        """Get the GUID string of the virtual desktop a window is on."""
        if not self._manager:
            return ""
        try:
            guid = self._manager.GetWindowDesktopId(hwnd)
            return str(guid)
        except Exception:
            return ""

    def move_window_to_desktop(self, hwnd: int, desktop_name: str):
        """Move a window to a virtual desktop by name."""
        if not self._manager:
            return
        try:
            target_guid_str = self._resolve_to_guid(desktop_name)
            if not target_guid_str:
                logger.error(f"Desktop '{desktop_name}' not found.")
                return
            guid = GUID(target_guid_str)
            self._manager.MoveWindowToDesktop(hwnd, byref(guid))
        except Exception as e:
            logger.error(f"Failed to move window to desktop: {e}")

    # -------------------------------------------------------------------------
    # Internal helpers for name/GUID resolution
    # -------------------------------------------------------------------------

    def _get_name_from_registry(self, guid_str: str) -> str:
        """Get the user-set name for a desktop from the registry.

        Returns None if no custom name is set.
        """
        try:
            import winreg

            path = (
                "Software\\Microsoft\\Windows\\CurrentVersion"
                f"\\Explorer\\VirtualDesktops\\Desktops\\{guid_str}"
            )
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, path) as key:
                name, _ = winreg.QueryValueEx(key, "Name")
                return name
        except Exception:
            return None

    def _resolve_to_guid(self, name: str) -> str:
        """Resolve a desktop name to its GUID string.

        Also supports passing a GUID string directly.
        """
        desktops_map = {}

        try:
            desktops_array = self._get_desktops()
            count = desktops_array.GetCount()

            for i in range(count):
                unk = desktops_array.GetAt(i, byref(IVirtualDesktop._iid_))
                desktop = unk.QueryInterface(IVirtualDesktop)
                guid = desktop.GetID()
                if not guid:
                    continue
                guid_str = str(guid)

                reg_name = self._get_name_from_registry(guid_str)
                display_name = reg_name if reg_name else f"Desktop {i + 1}"

                desktops_map[display_name.lower()] = guid_str
                if name.lower() == guid_str.lower():
                    return guid_str

        except Exception as e:
            logger.error(f"Error scanning desktops for resolution: {e}")
            return None

        if name.lower() in desktops_map:
            return desktops_map[name.lower()]

        return None

    # -------------------------------------------------------------------------
    # Internal manager operations (version-aware)
    # -------------------------------------------------------------------------

    def create_desktop(self, name: str = None) -> str:
        """Create a new virtual desktop and return its name."""
        if not self._internal_manager:
            raise RuntimeError("Internal VDM not initialized")

        desktop = self._create_desktop_raw()
        guid = desktop.GetID()
        guid_str = str(guid)

        if name and self._has_set_name:
            self.rename_desktop_by_guid(guid_str, name)
            return name
        else:
            desktops = self.get_all_desktops()
            return desktops[-1]["name"]

    def remove_desktop(self, desktop_name: str):
        """Remove a virtual desktop by name."""
        if not self._internal_manager:
            raise RuntimeError("Internal VDM not initialized")

        target_guid_str = self._resolve_to_guid(desktop_name)
        if not target_guid_str:
            logger.error(f"Desktop '{desktop_name}' not found.")
            return

        target_guid = GUID(target_guid_str)
        try:
            target_desktop = self._internal_manager.FindDesktop(target_guid)
        except Exception:
            logger.error(f"Could not find desktop with GUID {target_guid_str}")
            return

        # Find a fallback desktop (first desktop that isn't the target)
        desktops_array = self._get_desktops()
        count = desktops_array.GetCount()
        fallback_desktop = None

        for i in range(count):
            unk = desktops_array.GetAt(i, byref(IVirtualDesktop._iid_))
            candidate = unk.QueryInterface(IVirtualDesktop)
            candidate_id = candidate.GetID()
            if str(candidate_id) != str(target_guid):
                fallback_desktop = candidate
                break

        if not fallback_desktop:
            logger.error("No fallback desktop found (cannot delete the only desktop)")
            return

        self._internal_manager.RemoveDesktop(target_desktop, fallback_desktop)

    def rename_desktop(self, desktop_name: str, new_name: str):
        """Rename a virtual desktop by its current name."""
        if not self._has_set_name:
            logger.warning("Rename is not supported on this Windows version.")
            return

        target_guid_str = self._resolve_to_guid(desktop_name)
        if not target_guid_str:
            logger.error(f"Desktop '{desktop_name}' not found.")
            return

        self.rename_desktop_by_guid(target_guid_str, new_name)

    def rename_desktop_by_guid(self, guid_str: str, new_name: str):
        """Rename a virtual desktop by GUID string."""
        if not self._internal_manager or not self._has_set_name:
            return

        target_guid = GUID(guid_str)
        try:
            target_desktop = self._internal_manager.FindDesktop(target_guid)
        except Exception:
            return

        hs_name = create_hstring(new_name)
        try:
            self._internal_manager.SetName(target_desktop, hs_name)
        except Exception as e:
            logger.error(f"Failed to rename desktop: {e}")
        finally:
            delete_hstring(hs_name)

    def switch_desktop(self, desktop_name: str):
        """Switch to a virtual desktop by name."""
        if not self._internal_manager:
            raise RuntimeError("Internal VDM not initialized")

        target_guid_str = self._resolve_to_guid(desktop_name)
        if not target_guid_str:
            logger.error(f"Desktop '{desktop_name}' not found")
            return

        target_guid = GUID(target_guid_str)
        try:
            target_desktop = self._internal_manager.FindDesktop(target_guid)
            self._switch_desktop_raw(target_desktop)
        except Exception as e:
            logger.error(f"Failed to switch desktop: {e}")

    def get_all_desktops(self) -> list[dict]:
        """Get a list of all virtual desktops.

        Returns:
            List of dicts with 'id' (GUID string) and 'name' keys.
        """
        if not self._internal_manager:
            return [
                {
                    "id": "00000000-0000-0000-0000-000000000000",
                    "name": "Default Desktop",
                }
            ]

        desktops_array = self._get_desktops()
        count = desktops_array.GetCount()

        result = []
        for i in range(count):
            try:
                unk = desktops_array.GetAt(i, byref(IVirtualDesktop._iid_))
                desktop = unk.QueryInterface(IVirtualDesktop)
                guid = desktop.GetID()
                if not guid:
                    continue

                guid_str = str(guid)
                reg_name = self._get_name_from_registry(guid_str)
                name = reg_name if reg_name else f"Desktop {i + 1}"

                result.append({"id": guid_str, "name": name})
            except Exception as e:
                logger.error(f"Error retrieving desktop at index {i}: {e}")
                continue

        return result

    def get_current_desktop(self) -> dict:
        """Get info about the currently active virtual desktop.

        Returns:
            Dict with 'id' (GUID string) and 'name' keys.
        """
        if not self._internal_manager:
            return {
                "id": "00000000-0000-0000-0000-000000000000",
                "name": "Default Desktop",
            }

        current_desktop = self._get_current_desktop_raw()
        guid = current_desktop.GetID()
        guid_str = str(guid)

        all_desktops = self.get_all_desktops()
        for d in all_desktops:
            if d["id"] == guid_str:
                return d

        return {"id": guid_str, "name": "Unknown"}


# =============================================================================
# Module-level convenience functions
# =============================================================================


def create_desktop(name: str = None) -> str:
    return _get_manager().create_desktop(name)


def remove_desktop(desktop_name: str):
    _get_manager().remove_desktop(desktop_name)


def rename_desktop(desktop_name: str, new_name: str):
    _get_manager().rename_desktop(desktop_name, new_name)


def switch_desktop(desktop_name: str):
    _get_manager().switch_desktop(desktop_name)


def get_all_desktops() -> list[dict]:
    return _get_manager().get_all_desktops()


def get_current_desktop() -> dict:
    return _get_manager().get_current_desktop()
