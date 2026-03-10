# get_BoundingRectangle

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-irawelementproviderfragment-get_boundingrectangle)

# IRawElementProviderFragment::get\_BoundingRectangle method (uiautomationcore.h)

Specifies the bounding rectangle of this element.

This property is read-only.

## Syntax

```
HRESULT get_BoundingRectangle(
  UiaRect *pRetVal
);
```

## Parameters

`pRetVal`

## Return value

None

## Remarks

The bounding rectangle is defined by the location of the top left corner on the screen, and the dimensions.

No clipping is required if the element is partly obscured or partly off-screen. The IsOffscreen property should be set to indicate whether the rectangle is actually visible.

Not all points within the bounding rectangle are necessarily clickable.

#### Examples

The following example implementation by a list item provider calculates the bounding rectangle for the item
based on its height and position within the containing list box.

```
HRESULT STDMETHODCALLTYPE ListItemProvider::get_BoundingRectangle(UiaRect * pRetVal)
{
    if (pRetVal == NULL) return E_INVALIDARG;

    UiaRect parentRect;
    HRESULT hr = m_parentProvider->get_BoundingRectangle(&parentRect);
    pRetVal->left = parentRect.left;
    pRetVal->top = parentRect.top + (m_pParentControl->m_itemHeight * m_itemIndex);
    pRetVal->width = parentRect.width;
    pRetVal->height = m_pParentControl->m_itemHeight;
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

[IRawElementProviderFragment](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementproviderfragment)

---
