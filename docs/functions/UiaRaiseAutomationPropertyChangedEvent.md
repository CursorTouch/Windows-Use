# UiaRaiseAutomationPropertyChangedEvent

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiaraiseautomationpropertychangedevent)

# UiaRaiseAutomationPropertyChangedEvent function (uiautomationcoreapi.h)

Called by providers to notify the Microsoft UI Automation core that an element property has changed.

## Syntax

```
HRESULT UiaRaiseAutomationPropertyChangedEvent(
  [in] IRawElementProviderSimple *pProvider,
  [in] PROPERTYID                id,
  [in] VARIANT                   oldValue,
  [in] VARIANT                   newValue
);
```

## Parameters

`[in] pProvider`

Type: **[IRawElementProviderSimple](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementprovidersimple)\***

The provider node where the property change event occurred.

`[in] id`

Type: **PROPERTYID**

The identifier for the property that changed. For a list of property IDs, see [Property Identifiers](/en-us/windows/desktop/WinAuto/uiauto-entry-propids).

`[in] oldValue`

Type: **[VARIANT](/en-us/windows/desktop/WinAuto/variant-structure)**

The old value of the property.

`[in] newValue`

Type: **[VARIANT](/en-us/windows/desktop/WinAuto/variant-structure)**

The new value of the property.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this function succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcoreapi.h |
| **Library** | Uiautomationcore.lib |
| **DLL** | Uiautomationcore.dll |

---
