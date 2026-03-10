# get_DockPosition

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-idockprovider-get_dockposition)

# IDockProvider::get\_DockPosition method (uiautomationcore.h)

Indicates the current docking position of this element.

This property is read-only.

## Syntax

```
HRESULT get_DockPosition(
  DockPosition *pRetVal
);
```

## Parameters

`pRetVal`

## Return value

None

## Remarks

A docking container is a control that allows the arrangement of child elements, both horizontally and vertically, relative to the boundaries of the docking container and other elements in the container.

#### Examples

The following example shows how to return the DockPosition property.

```
    // dockPosition is a global variable of type DockPosition.

    HRESULT STDMETHODCALLTYPE BucketControl::get_DockPosition(DockPosition *pRetVal)
    {
        if (pRetVal == NULL)
        {
            return E_INVALIDARG;
        }
        *pRetVal = dockPosition;
        return S_OK;
    }
```

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |
| **DLL** | Uiautomationcore.dll |

## See also

[IDockProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-idockprovider)

[UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

---
