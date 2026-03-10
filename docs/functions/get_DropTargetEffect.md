# get_DropTargetEffect

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-idroptargetprovider-get_droptargeteffect)

# IDropTargetProvider::get\_DropTargetEffect method (uiautomationcore.h)

Retrieves a localized string that describes the effect that happens when the user drops the grabbed element on this drop target.

This property is read-only.

## Syntax

```
HRESULT get_DropTargetEffect(
  BSTR *pRetVal
);
```

## Parameters

`pRetVal`

## Return value

None

## Remarks

This property describes the default effect that happens when the user drops a grabbed element on a target, such as moving or copying the element. This property can be a short string such as "move", or a longer one such as "insert into Main group". The string is always localized.

If this property changes, the provider must notify clients by firing a [UIA\_AutomationPropertyChangedEventId](/en-us/windows/desktop/WinAuto/uiauto-event-ids) event.

#### Examples

```
IFACEMETHODIMP CRegionProvider::get_DropTargetEffect(BSTR * pDefaultDropAction)
{
    WCHAR wszDropAction[100];
    LoadString(g_hInstance, IDS_REGION_DEFAULTDROPACTION1, wszDropAction, 
        ARRAYSIZE(wszDropAction));
    *pDefaultDropAction = ::SysAllocString(wszDropAction);
    return (*pDefaultDropAction == nullptr) ? E_OUTOFMEMORY : S_OK;
}
```

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2012 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[IDropTargetProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-idroptargetprovider)

---
