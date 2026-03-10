# ElementProviderFromPoint

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-irawelementproviderfragmentroot-elementproviderfrompoint)

# IRawElementProviderFragmentRoot::ElementProviderFromPoint method (uiautomationcore.h)

Retrieves the provider of the element that is at the specified point in this fragment.

## Syntax

```
HRESULT ElementProviderFromPoint(
  [in]          double                      x,
  [in]          double                      y,
  [out, retval] IRawElementProviderFragment **pRetVal
);
```

## Parameters

`[in] x`

Type: **double**

The horizontal screen coordinate.

`[in] y`

Type: **double**

The vertical screen coordinate.

`[out, retval] pRetVal`

Type: **[IRawElementProviderFragment](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementproviderfragment)\*\***

Receives a pointer to the provider of the element at (x, y), or **NULL** if none exists. This parameter is passed uninitialized.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

The returned provider should correspond to the element that would receive mouse input at the specified point.

If the point is on this element but not on any child element, either **NULL** or the provider of the fragment root is returned. If the point is on an element in another framework that is hosted by this fragment, the method returns the element that hosts that fragment (as indicated by [IRawElementProviderFragment::GetEmbeddedFragmentRoots](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-irawelementproviderfragment-getembeddedfragmentroots)).

#### Examples

The following example shows an implementation for a list box hosted in an **HWND**
whose handle is *m\_controlHwnd*.
IndexFromY retrieves the index of the list item at the cursor position,
and GetItemByIndex retrieves
the UI Automation provider for that item.

```
HRESULT STDMETHODCALLTYPE ListProvider::ElementProviderFromPoint(double x, double y, IRawElementProviderFragment** pRetVal)
{
    if (pRetVal == NULL) 
    {
        return E_INVALIDARG;
    }
    POINT pt;
    pt.x = (LONG)x;
    pt.y = (LONG)y;
    ScreenToClient(m_controlHwnd, &pt);
    int itemIndex = this->m_pControl->IndexFromY(m_controlHwnd, pt.y);
    ListItemProvider* pItem = GetItemByIndex(itemIndex);  
    if (pItem != NULL)
    {
        *pRetVal = (IRawElementProviderFragment*)pItem;
        pItem->AddRef();
    }
    else 
    {
        pRetVal = (IRawElementProviderFragment*)this;
        pItem->AddRef();
    }

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

## See also

[IRawElementProviderFragmentRoot](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementproviderfragmentroot)

---
