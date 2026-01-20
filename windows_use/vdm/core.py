import comtypes.client
from comtypes import GUID, IUnknown, COMMETHOD, HRESULT
from ctypes import POINTER
from ctypes.wintypes import HWND, BOOL
import logging
import threading

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

# standard COM CLSIDs for VirtualDesktopManager
CLSID_VirtualDesktopManager = GUID("{aa509086-5ca9-4c25-8f95-589d3c07b48a}")

class IVirtualDesktopManager(IUnknown):
    _iid_ = GUID("{a5cd92ff-29be-454c-8d04-d82879fb3f1b}")
    _methods_ = [
        COMMETHOD([], HRESULT, "IsWindowOnCurrentVirtualDesktop",
                  (['in'], HWND, "topLevelWindow"),
                  (['out', 'retval'], POINTER(BOOL), "onCurrentDesktop")),
        COMMETHOD([], HRESULT, "GetWindowDesktopId",
                  (['in'], HWND, "topLevelWindow"),
                  (['out', 'retval'], POINTER(GUID), "desktopId")),
        COMMETHOD([], HRESULT, "MoveWindowToDesktop",
                  (['in'], HWND, "topLevelWindow"),
                  (['in'], GUID, "desktopId")),
    ]

class VirtualDesktopManager:
    """
    Wrapper around the Windows IVirtualDesktopManager interface.
    Allows checking if a window is on the current virtual desktop, getting its Desktop ID,
    and moving windows between desktops.
    """
    def __init__(self):
        self._manager = None
        try:
            # Ensure COM is initialized on this thread (RPC_E_CHANGED_MODE or S_OK/S_FALSE)
            # COINIT_APARTMENTTHREADED = 0x2, COINIT_MULTITHREADED = 0x0
            # We try standard init.
            import ctypes
            try:
                ctypes.windll.ole32.CoInitialize(None)
            except Exception:
                pass # Already initialized or failed, try proceeding

            self._manager = comtypes.client.CreateObject(CLSID_VirtualDesktopManager, interface=IVirtualDesktopManager)
        except Exception as e:
            logger.error(f"Failed to initialize VirtualDesktopManager: {e}")

    def is_window_on_current_desktop(self, hwnd: int) -> bool:
        """
        Checks if the specified window is on the currently active virtual desktop.
        """
        if not self._manager:
            return True # Fallback: assume visible if manager failed
        try:
            return self._manager.IsWindowOnCurrentVirtualDesktop(hwnd)
        except Exception:
            return True # Fail open

    def get_window_desktop_id(self, hwnd: int) -> str:
        """
        Returns the GUID (as a string) of the virtual desktop the window is on.
        """
        if not self._manager:
            return ""
        try:
            guid = self._manager.GetWindowDesktopId(hwnd)
            return str(guid)
        except Exception:
            return ""

    def move_window_to_desktop(self, hwnd: int, desktop_id: str):
        """
        Moves a window to the specified virtual desktop (by GUID string).
        """
        if not self._manager:
            return
        try:
            guid = GUID(desktop_id)
            self._manager.MoveWindowToDesktop(hwnd, guid)
        except Exception as e:
            logger.error(f"Failed to move window to desktop: {e}")
