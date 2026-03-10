# UiaRaiseStructureChangedEvent

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiaraisestructurechangedevent)

# UiaRaiseStructureChangedEvent function (uiautomationcoreapi.h)

Called by a provider to notify the Microsoft UI Automation core that the tree structure has changed.

## Syntax

```
HRESULT UiaRaiseStructureChangedEvent(
  [in] IRawElementProviderSimple *pProvider,
  [in] StructureChangeType       structureChangeType,
  [in] int                       *pRuntimeId,
  [in] int                       cRuntimeIdLen
);
```

## Parameters

`[in] pProvider`

Type: **[IRawElementProviderSimple](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementprovidersimple)\***

The provider node where the tree change occurred.

`[in] structureChangeType`

Type: **[StructureChangeType](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-structurechangetype)**

The type of change that occurred in the tree.

`[in] pRuntimeId`

Type: **int\***

The runtime IDs for the child elements of the provider node where the tree change occurred. This parameter is used only when *structureChangeType* is [StructureChangeType\_ChildRemoved](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-structurechangetype); it is **NULL** for all other structure-change events.

**Note**  For Windows 7, the array of integers pointed to by *pRuntimeId* can contain a partial set of IDs that identify only those elements affected by the structure change.

`[in] cRuntimeIdLen`

Type: **int**

Length of the array of integers.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this function succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

An example of a change in the tree structure is child elements being added to or removed from a list box, or being expanded or collapsed in a tree view.

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
