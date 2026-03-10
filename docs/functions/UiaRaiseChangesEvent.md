# UiaRaiseChangesEvent

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiaraisechangesevent)

# UiaRaiseChangesEvent function (uiautomationcoreapi.h)

Called by providers to notify the Microsoft UI Automation core that a change has occurred.

## Syntax

```
HRESULT UiaRaiseChangesEvent(
  [in] IRawElementProviderSimple *pProvider,
  [in] int                       eventIdCount,
  [in] UiaChangeInfo             *pUiaChanges
);
```

## Parameters

`[in] pProvider`

Type: **[IRawElementProviderSimple](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementprovidersimple)\***

The provider node where the change event occurred.

`[in] eventIdCount`

The number of changes that occurred. This is the number of [UiaChangeInfo](/en-us/windows/desktop/api/uiautomationcore/ns-uiautomationcore-uiachangeinfo) structures pointed to by the *pUiaChanges* parameter.

`[in] pUiaChanges`

A collection of pointers to [UiaChangeInfo](/en-us/windows/desktop/api/uiautomationcore/ns-uiautomationcore-uiachangeinfo) structures.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types) value indicating success or failure.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 10 [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2016 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcoreapi.h |
| **Library** | Uiautomationcore.lib |
| **DLL** | Uiautomationcore.dll |

---
