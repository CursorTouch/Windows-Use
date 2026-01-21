import comtypes.client
from comtypes import GUID, IUnknown, COMMETHOD, HRESULT
from ctypes import POINTER
from ctypes.wintypes import HWND, BOOL
import logging
import threading
import sys
import ctypes
from ctypes import HRESULT, POINTER, c_void_p, c_uint32, byref
from ctypes.wintypes import HWND, BOOL, UINT, INT, WCHAR, LPVOID
from comtypes import GUID, IUnknown, COMMETHOD, STDMETHOD

logger = logging.getLogger(__name__)

import secrets
import string

_thread_local = threading.local()

# Global mapping for Simple ID (Short) <-> GUID (Long)
_SIMPLE_TO_GUID = {}
_GUID_TO_SIMPLE = {}
_MAP_LOCK = threading.Lock()

def _get_simple_id(guid_str: str) -> str:
    """Gets or creates a simple 8-char ID for a given GUID string."""
    guid_str = guid_str.upper() # Normalize GUIDs
    with _MAP_LOCK:
        if guid_str in _GUID_TO_SIMPLE:
            return _GUID_TO_SIMPLE[guid_str]
        
        # Generate unique short ID
        while True:
            # 8 char random hex-like string (easy to read)
            alphabet = string.ascii_lowercase + string.digits
            short_id = ''.join(secrets.choice(alphabet) for _ in range(8))
            if short_id not in _SIMPLE_TO_GUID:
                break
        
        _SIMPLE_TO_GUID[short_id] = guid_str
        _GUID_TO_SIMPLE[guid_str] = short_id
        return short_id

def _resolve_guid(simple_id: str) -> str:
    """Resolves a simple ID to its GUID string."""
    with _MAP_LOCK:
        if simple_id in _SIMPLE_TO_GUID:
            return _SIMPLE_TO_GUID[simple_id]
        # Fallback: maybe the user passed a real GUID?
        return simple_id

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

# Internal COM Interfaces for Windows 11
CLSID_ImmersiveShell = GUID("{C2F03A33-21F5-47FA-B4BB-156362A2F239}")
CLSID_VirtualDesktopManagerInternal = GUID("{C5E0CDCA-7B6E-41B2-9FC4-D93975CC467B}")
IID_IServiceProvider = GUID("{6D5140C1-7436-11CE-8034-00AA006009FA}")

class IServiceProvider(IUnknown):
    _iid_ = IID_IServiceProvider
    _methods_ = [
        COMMETHOD([], HRESULT, "QueryService",
                  (['in'], GUID, "guidService"),
                  (['in'], GUID, "riid"),
                  (['out'], POINTER(POINTER(IUnknown)), "ppvObject")),
    ]

# IObjectArray for iterating desktops
class IObjectArray(IUnknown):
    _iid_ = GUID("{92CA9DCD-5622-4BBA-A805-5E9F541BD8CC}")
    _methods_ = [
        COMMETHOD([], HRESULT, "GetCount",
                  (['out'], POINTER(UINT), "pcObjects")),
        COMMETHOD([], HRESULT, "GetAt",
                  (['in'], UINT, "uiIndex"),
                  (['in'], GUID, "riid"),
                  (['out'], POINTER(POINTER(IUnknown)), "ppv")),
    ]

# Wrapper for HSTRING
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

def create_hstring(text):
    if not _WindowsCreateString:
        return HSTRING(0)
    hs = HSTRING()
    hr = _WindowsCreateString(text, len(text), byref(hs))
    if hr != 0:
        raise OSError(f"WindowsCreateString failed: {hr}")
    return hs

def delete_hstring(hs):
    if _WindowsDeleteString and hs:
        _WindowsDeleteString(hs)

# Interface definitions depend on build number
BUILD = sys.getwindowsversion().build

if BUILD >= 26100:
    IID_IVirtualDesktopManagerInternal = GUID("{53F5CA0B-158F-4124-900C-057158060B27}")
    IID_IVirtualDesktop = GUID("{3F07F4BE-B107-441A-AF0F-39D82529072C}")
elif BUILD >= 22621:
    IID_IVirtualDesktopManagerInternal = GUID("{A3175F2D-239C-4BD2-8AA0-EEBA8B0B138E}")
    IID_IVirtualDesktop = GUID("{3F07F4BE-B107-441A-AF0F-39D82529072C}")
else:
    # Windows 10 (Build 19041+)
    IID_IVirtualDesktopManagerInternal = GUID("{F31574D6-B682-4CDC-BD56-1827860ABEC6}")
    IID_IVirtualDesktop = GUID("{FF72FFDD-BE7E-43FC-9C03-AD81681E88E4}")

class IVirtualDesktop(IUnknown):
    _iid_ = IID_IVirtualDesktop
    # Methods for 22621+
    _methods_ = [
        STDMETHOD(HRESULT, "IsViewVisible", (POINTER(IUnknown), POINTER(UINT))), # IApplicationView
        COMMETHOD([], HRESULT, "GetID", (['out'], POINTER(GUID), "pGuid")),
        COMMETHOD([], HRESULT, "GetName", (['out'], POINTER(HSTRING), "pName")),
        COMMETHOD([], HRESULT, "GetWallpaperPath", (['out'], POINTER(HSTRING), "pPath")),
        COMMETHOD([], HRESULT, "IsRemote", (['out'], POINTER(HWND), "pW")),
    ]

# Needed placeholders
class IApplicationView(IUnknown):
    _iid_ = GUID("{372E1D3B-38D3-42E4-A15B-8AB2B178F513}") # Generic match

class IVirtualDesktopManagerInternal(IUnknown):
    _iid_ = IID_IVirtualDesktopManagerInternal
    if BUILD >= 26100:
         _methods_ = [
            COMMETHOD([], HRESULT, "GetCount", (['out'], POINTER(UINT), "pCount")),
            STDMETHOD(HRESULT, "MoveViewToDesktop", (POINTER(IApplicationView), POINTER(IVirtualDesktop))),
            STDMETHOD(HRESULT, "CanViewMoveDesktops", (POINTER(IApplicationView), POINTER(UINT))),
            COMMETHOD([], HRESULT, "GetCurrentDesktop", (['out'], POINTER(POINTER(IVirtualDesktop)), "pDesktop")),
            COMMETHOD([], HRESULT, "GetDesktops", (['out'], POINTER(POINTER(IObjectArray)), "array")),
            STDMETHOD(HRESULT, "GetAdjacentDesktop", (POINTER(IVirtualDesktop), UINT, POINTER(POINTER(IVirtualDesktop)))),
            STDMETHOD(HRESULT, "SwitchDesktop", (POINTER(IVirtualDesktop),)),
            STDMETHOD(HRESULT, "SwitchDesktopAndMoveForegroundView", (POINTER(IVirtualDesktop),)),
            COMMETHOD([], HRESULT, "CreateDesktopW", (['out'], POINTER(POINTER(IVirtualDesktop)), "pDesktop")),
            STDMETHOD(HRESULT, "MoveDesktop", (POINTER(IVirtualDesktop), UINT)),
            COMMETHOD([], HRESULT, "RemoveDesktop", (['in'], POINTER(IVirtualDesktop), "destroyDesktop"), (['in'], POINTER(IVirtualDesktop), "fallbackDesktop")),
            COMMETHOD([], HRESULT, "FindDesktop", (['in'], POINTER(GUID), "pGuid"), (['out'], POINTER(POINTER(IVirtualDesktop)), "pDesktop")),
            STDMETHOD(HRESULT, "GetDesktopSwitchIncludeExcludeViews", (POINTER(IVirtualDesktop), POINTER(POINTER(IObjectArray)), POINTER(POINTER(IObjectArray)))),
            COMMETHOD([], HRESULT, "SetName", (['in'], POINTER(IVirtualDesktop), "pDesktop"), (['in'], HSTRING, "name")),
            # Others omitted for now
        ]
    elif BUILD >= 22621:
         _methods_ = [
            COMMETHOD([], HRESULT, "GetCount", (['out'], POINTER(UINT), "pCount")),
            STDMETHOD(HRESULT, "MoveViewToDesktop", (POINTER(IApplicationView), POINTER(IVirtualDesktop))),
            STDMETHOD(HRESULT, "CanViewMoveDesktops", (POINTER(IApplicationView), POINTER(UINT))),
            COMMETHOD([], HRESULT, "GetCurrentDesktop", (['out'], POINTER(POINTER(IVirtualDesktop)), "pDesktop")),
            COMMETHOD([], HRESULT, "GetDesktops", (['out'], POINTER(POINTER(IObjectArray)), "array")),
            STDMETHOD(HRESULT, "GetAdjacentDesktop", (POINTER(IVirtualDesktop), UINT, POINTER(POINTER(IVirtualDesktop)))),
            STDMETHOD(HRESULT, "SwitchDesktop", (POINTER(IVirtualDesktop),)),
            COMMETHOD([], HRESULT, "CreateDesktopW", (['out'], POINTER(POINTER(IVirtualDesktop)), "pDesktop")),
            STDMETHOD(HRESULT, "MoveDesktop", (POINTER(IVirtualDesktop), UINT)),
            COMMETHOD([], HRESULT, "RemoveDesktop", (['in'], POINTER(IVirtualDesktop), "destroyDesktop"), (['in'], POINTER(IVirtualDesktop), "fallbackDesktop")),
            COMMETHOD([], HRESULT, "FindDesktop", (['in'], POINTER(GUID), "pGuid"), (['out'], POINTER(POINTER(IVirtualDesktop)), "pDesktop")),
            STDMETHOD(HRESULT, "GetDesktopSwitchIncludeExcludeViews", (POINTER(IVirtualDesktop), POINTER(POINTER(IObjectArray)), POINTER(POINTER(IObjectArray)))),
            COMMETHOD([], HRESULT, "SetName", (['in'], POINTER(IVirtualDesktop), "pDesktop"), (['in'], HSTRING, "name")),
        ]
    else:
        # Windows 10
         _methods_ = [
            COMMETHOD([], HRESULT, "GetCount", (['out'], POINTER(UINT), "pCount")),
            STDMETHOD(HRESULT, "MoveViewToDesktop", (POINTER(IApplicationView), POINTER(IVirtualDesktop))),
            STDMETHOD(HRESULT, "CanViewMoveDesktops", (POINTER(IApplicationView), POINTER(UINT))),
            COMMETHOD([], HRESULT, "GetCurrentDesktop", (['out'], POINTER(POINTER(IVirtualDesktop)), "pDesktop")),
            COMMETHOD([], HRESULT, "GetDesktops", (['out'], POINTER(POINTER(IObjectArray)), "array")),
            STDMETHOD(HRESULT, "GetAdjacentDesktop", (POINTER(IVirtualDesktop), UINT, POINTER(POINTER(IVirtualDesktop)))),
            STDMETHOD(HRESULT, "SwitchDesktop", (POINTER(IVirtualDesktop),)),
            COMMETHOD([], HRESULT, "CreateDesktopW", (['out'], POINTER(POINTER(IVirtualDesktop)), "pDesktop")),
            COMMETHOD([], HRESULT, "RemoveDesktop", (['in'], POINTER(IVirtualDesktop), "destroyDesktop"), (['in'], POINTER(IVirtualDesktop), "fallbackDesktop")),
            COMMETHOD([], HRESULT, "FindDesktop", (['in'], POINTER(GUID), "pGuid"), (['out'], POINTER(POINTER(IVirtualDesktop)), "pDesktop")),
            # No SetName on this interface for Win10 typically
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
            
            # Initialize Internal Manager
            try:
                service_provider = comtypes.client.CreateObject(CLSID_ImmersiveShell, interface=IServiceProvider)
                unk = service_provider.QueryService(CLSID_VirtualDesktopManagerInternal, IVirtualDesktopManagerInternal._iid_)
                self._internal_manager = unk.QueryInterface(IVirtualDesktopManagerInternal)
            except Exception as e:
                logger.warning(f"Failed to initialize VirtualDesktopManagerInternal: {e}")
                self._internal_manager = None

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
            return _get_simple_id(str(guid))
        except Exception:
            return ""

    def move_window_to_desktop(self, hwnd: int, desktop_id: str):
        """
        Moves a window to the specified virtual desktop (by GUID string).
        """
        if not self._manager:
            return
        try:
            target_guid_str = _resolve_guid(desktop_id)
            guid = GUID(target_guid_str)
            self._manager.MoveWindowToDesktop(hwnd, guid)
        except Exception as e:
            logger.error(f"Failed to move window to desktop: {e}")

    def create_desktop(self, name: str = None) -> str:
        """
        Creates a new virtual desktop and returns its ID.
        Optionally sets the name of the new desktop.
        """
        if not self._internal_manager:
            raise RuntimeError("Internal VDM not initialized")
        
        desktop = self._internal_manager.CreateDesktopW()
        guid = desktop.GetID()
        guid_str = str(guid)
        
        # Get simple ID
        simple_id = _get_simple_id(guid_str)

        if name:
            self.rename_desktop(simple_id, name) # Use simple ID internally too now
            
        return simple_id

    def remove_desktop(self, desktop_id: str):
        """
        Removes a virtual desktop by ID. 
        Will try to fallback to the first available desktop that is not the one being deleted.
        """
        if not self._internal_manager:
            raise RuntimeError("Internal VDM not initialized")
        
        target_guid_str = _resolve_guid(desktop_id)
        target_guid = GUID(target_guid_str)
        
        # We need the IVirtualDesktop object for the target
        try:
             target_desktop = self._internal_manager.FindDesktop(target_guid)
        except Exception:
             logger.error(f"Could not find desktop with ID {desktop_id}")
             return

        # Find a fallback desktop
        desktops_array = self._internal_manager.GetDesktops()
        count = desktops_array.GetCount()
        fallback_desktop = None
        
        for i in range(count):
            unk = desktops_array.GetAt(i, IVirtualDesktop._iid_)
            candidate = unk.QueryInterface(IVirtualDesktop)
            candidate_id = candidate.GetID()
            if str(candidate_id) != str(target_guid):
                fallback_desktop = candidate
                break
        
        if not fallback_desktop:
            # If no other desktop, we can't delete the only one? Or create one?
            # Windows usually prevents deleting the last one.
            logger.error("No fallback desktop found (cannot delete the only desktop)")
            return

        self._internal_manager.RemoveDesktop(target_desktop, fallback_desktop)

    def rename_desktop(self, desktop_id: str, new_name: str):
        """
        Renames a virtual desktop.
        """
        if not self._internal_manager:
            raise RuntimeError("Internal VDM not initialized")
        
        target_guid_str = _resolve_guid(desktop_id)
        target_guid = GUID(target_guid_str)
        try:
             target_desktop = self._internal_manager.FindDesktop(target_guid)
        except Exception:
             logger.error(f"Could not find desktop with ID {desktop_id}")
             return

        hs_name = create_hstring(new_name)
        try:
            # Check if SetName method exists (it might not on Windows 10)
            if hasattr(self._internal_manager, "SetName"):
                self._internal_manager.SetName(target_desktop, hs_name)
            else:
                logger.warning("Rename desktop is not supported on this Windows build.")
        except Exception as e:
            logger.error(f"Failed to rename desktop: {e}")
        finally:
            delete_hstring(hs_name)

    def switch_desktop(self, desktop_id: str):
        """
        Switches to the specified virtual desktop.
        """
        if not self._internal_manager:
            raise RuntimeError("Internal VDM not initialized")
        
        target_guid_str = _resolve_guid(desktop_id)
        target_guid = GUID(target_guid_str)
        try:
             target_desktop = self._internal_manager.FindDesktop(target_guid)
        except Exception:
             logger.error(f"Could not find desktop with ID {desktop_id}")
             return

        self._internal_manager.SwitchDesktop(target_desktop)

    def get_all_desktops(self) -> list[dict]:
        """
        Returns a list of all virtual desktops.
        Each entry is a dict: {'id': str, 'name': str}
        """
        if not self._internal_manager:
            raise RuntimeError("Internal VDM not initialized")
        
        desktops_array = self._internal_manager.GetDesktops()
        count = desktops_array.GetCount()
        
        result = []
        for i in range(count):
            try:
                unk = desktops_array.GetAt(i, IVirtualDesktop._iid_)
                desktop = unk.QueryInterface(IVirtualDesktop)
                guid = desktop.GetID()
                simple_id = _get_simple_id(str(guid))
                
                name = ""
                try:
                    # Windows 10 interface might not support GetName commonly or it might fail
                    if hasattr(desktop, "GetName"):
                        hname = desktop.GetName()
                        name = ctypes.wstring_at(hname)
                        delete_hstring(hname)
                except Exception:
                    pass # Name retrieval failed, ignore
                
                if not name:
                    name = f"Desktop {i+1}"

                result.append({'id': simple_id, 'name': name})
            except Exception as e:
                logger.error(f"Error retrieving desktop at index {i}: {e}")
                continue
                
        return result


    def get_current_desktop(self) -> dict:
        """
        Returns info about the current virtual desktop.
        Returns: {'id': str, 'name': str}
        """
        if not self._internal_manager:
            raise RuntimeError("Internal VDM not initialized")
        
        current_desktop = self._internal_manager.GetCurrentDesktop()
        guid = current_desktop.GetID()
        simple_id = _get_simple_id(str(guid))
        
        name = ""
        try:
             # Windows 10 interface might not support GetName commonly or it might fail
            if hasattr(current_desktop, "GetName"):
                hname = current_desktop.GetName()
                name = ctypes.wstring_at(hname)
                delete_hstring(hname)
        except Exception:
            pass 
        
        if not name:
            # Fallback logic
            desktops_array = self._internal_manager.GetDesktops()
            count = desktops_array.GetCount()
            current_guid_str = str(guid)
            
            found_name = "Current Desktop"
            for i in range(count):
                try:
                    unk = desktops_array.GetAt(i, IVirtualDesktop._iid_)
                    candidate = unk.QueryInterface(IVirtualDesktop)
                    candidate_guid_str = str(candidate.GetID())
                    if candidate_guid_str == current_guid_str:
                        found_name = f"Desktop {i+1}"
                        break
                except Exception:
                    continue
            name = found_name

        return {'id': simple_id, 'name': name}

def create_desktop(name: str = None) -> str:
    return _get_manager().create_desktop(name)

def remove_desktop(desktop_id: str):
    _get_manager().remove_desktop(desktop_id)

def rename_desktop(desktop_id: str, new_name: str):
    _get_manager().rename_desktop(desktop_id, new_name)

def switch_desktop(desktop_id: str):
    _get_manager().switch_desktop(desktop_id)

def get_all_desktops() -> list[dict]:
    return _get_manager().get_all_desktops()

def get_current_desktop() -> dict:
    return _get_manager().get_current_desktop()

