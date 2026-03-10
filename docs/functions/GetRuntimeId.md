# GetRuntimeId

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-irawelementproviderfragment-getruntimeid)

# IRawElementProviderFragment::GetRuntimeId method (uiautomationcore.h)

Retrieves the runtime identifier of an element.

## Syntax

```
HRESULT GetRuntimeId(
  [out, retval] SAFEARRAY **pRetVal
);
```

## Parameters

`[out, retval] pRetVal`

Type: **[SAFEARRAY](/en-us/windows/win32/api/oaidl/ns-oaidl-safearray)\*\***

Receives a pointer to the runtime identifier. This parameter is passed uninitialized.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

Implementations should return **NULL** for a top-level element that is hosted in a window.
Other elements should return an array that contains **UiaAppendRuntimeId**
(defined in Uiautomationcoreapi.h),
followed by a value that is unique within an instance of the fragment.

#### Examples

The following implementation for a list item returns a runtime identifier made up of the
**UiaAppendRuntimeId** constant and the index of the item within the list.

```
HRESULT STDMETHODCALLTYPE ListItemProvider::GetRuntimeId(SAFEARRAY ** pRetVal)
{
    if (pRetVal == NULL) 
    {
        return E_INVALIDARG;
    }
    
    int rId[] = { UiaAppendRuntimeId, m_itemIndex };
    SAFEARRAY *psa = SafeArrayCreateVector(VT_I4, 0, 2);
    if (psa == NULL)
    {
        return E_OUTOFMEMORY;
    }
    
    for (LONG i = 0; i < 2; i++)
    {
        SafeArrayPutElement(psa, &i, (void*)&(rId[i]));
    }
    
    *pRetVal = psa;
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

[Best Practices for Using Safe Arrays](/en-us/windows/desktop/WinAuto/uiauto-workingwithsafearrays)

**Conceptual**

[IRawElementProviderFragment](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementproviderfragment)

**Reference**

---
