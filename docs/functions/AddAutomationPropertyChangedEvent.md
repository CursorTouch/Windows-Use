# AddAutomationPropertyChangedEvent

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-iproxyproviderwineventsink-addautomationpropertychangedevent)

# IProxyProviderWinEventSink::AddAutomationPropertyChangedEvent method (uiautomationcore.h)

Raises a property-changed event.

## Syntax

```
HRESULT AddAutomationPropertyChangedEvent(
  [in] IRawElementProviderSimple *pProvider,
  [in] PROPERTYID                id,
  [in] VARIANT                   newValue
);
```

## Parameters

`[in] pProvider`

Type: **[IRawElementProviderSimple](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementprovidersimple)\***

A pointer to the provider for the element that will raise the event.

`[in] id`

Type: **PROPERTYID**

The identifier of the property that is to be changed. For a list of property IDs, see [Property Identifiers](/en-us/windows/desktop/WinAuto/uiauto-entry-propids).

`[in] newValue`

Type: **[VARIANT](/en-us/windows/desktop/WinAuto/variant-structure)**

The new value for the changed property.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[IProxyProviderWinEventSink](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iproxyproviderwineventsink)

---
