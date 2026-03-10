# FindItemByProperty

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationitemcontainerpattern-finditembyproperty)

# IUIAutomationItemContainerPattern::FindItemByProperty method (uiautomationclient.h)

Retrieves an element within a containing element, based on a specified property value.

## Syntax

```
HRESULT FindItemByProperty(
  [in]          IUIAutomationElement *pStartAfter,
  [in]          PROPERTYID           propertyId,
  [in]          VARIANT              value,
  [out, retval] IUIAutomationElement **pFound
);
```

## Parameters

`[in] pStartAfter`

Type: **[IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement)\***

A pointer to the element after which the search begins, or **NULL** to search all elements.

`[in] propertyId`

Type: **PROPERTYID**

The property identifier. For a list of property IDs, see [Property Identifiers](/en-us/windows/desktop/WinAuto/uiauto-entry-propids).

`[in] value`

Type: **[VARIANT](/en-us/windows/desktop/api/oaidl/ns-oaidl-variant)**

The property value.

`[out, retval] pFound`

Type: **[IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement)\*\***

Receives a pointer to the matching element.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

The provider may return an actual [IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement) interface or a placeholder if the matching element is virtualized.

This method returns E\_INVALIDARG if the property requested is not one that the container supports searching over. It is expected that most containers will support Name property, and if appropriate for the container, AutomationId and IsSelected.

This method can be slow, because it may need to traverse multiple objects to find a matching one. When used in a loop to return multiple items, no specific order is defined so long as each item is returned only once (that is, the loop should terminate). This method is also item-centric, not UI-centric, so items with multiple UI representations need to be hit only once.

When the *propertyId* parameter is specified as 0 (zero), the provider is expected to return the next item after *pStartAfter*. If *pStartAfter* is specified as **NULL** with a *propertyId* of 0, the provider should return the first item in the container. When *propertyId* is specified as 0, the *value* parameter should be VT\_EMPTY.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomationItemContainerPattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationitemcontainerpattern)

[Realize](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationvirtualizeditempattern-realize)

**Reference**

---
