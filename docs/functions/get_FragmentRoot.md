# get_FragmentRoot

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-irawelementproviderfragment-get_fragmentroot)

# IRawElementProviderFragment::get\_FragmentRoot method (uiautomationcore.h)

Specifies the root node of the fragment.

This property is read-only.

## Syntax

```
HRESULT get_FragmentRoot(
  IRawElementProviderFragmentRoot **pRetVal
);
```

## Parameters

`pRetVal`

## Return value

None

## Remarks

A provider for a fragment root should return a pointer to its own implementation of
[IRawElementProviderFragmentRoot](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementproviderfragmentroot).

#### Examples

The following example implementation for a list item provider returns the provider for the parent list box.

```
HRESULT STDMETHODCALLTYPE ListItemProvider::get_FragmentRoot(IRawElementProviderFragmentRoot** pRetVal)
{
    if (pRetVal == NULL) return E_INVALIDARG;
    IRawElementProviderFragmentRoot* pRoot = static_cast<IRawElementProviderFragmentRoot*>(m_parentProvider);
    pRoot->AddRef();
    *pRetVal = pRoot;
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
