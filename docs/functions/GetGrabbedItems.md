# GetGrabbedItems

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-idragprovider-getgrabbeditems)

# IDragProvider::GetGrabbedItems method (uiautomationcore.h)

Retrieves the collection of elements that are being dragged as part of a drag operation.

## Syntax

```
HRESULT GetGrabbedItems(
  [out, retval, optional] SAFEARRAY **pRetVal
);
```

## Parameters

`[out, retval, optional] pRetVal`

An array of VT\_UNKNOWN pointers to the [IRawElementProviderSimple](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementprovidersimple) interfaces
of the elements that are being dragged. This parameter is **NULL** if only a single item is being dragged.

## Return value

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

If the user is dragging multiple items, the items are represented by a single master element with an associated set of grabbed elements. The master element raises the appropriate events, to avoid having a large set of duplicate events. The client can call **GetGrabbedItems** to retrieve the full list of grabbed items. The provider should allocate a [SAFEARRAY](/en-us/windows/win32/api/oaidl/ns-oaidl-safearray) of appropriate length and add the Component Object Model (COM) pointers of the elements that are part of the drag operation.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2012 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[IDragProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-idragprovider)

---
