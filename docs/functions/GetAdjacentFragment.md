# GetAdjacentFragment

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-irawelementproviderwindowlesssite-getadjacentfragment)

# IRawElementProviderWindowlessSite::GetAdjacentFragment method (uiautomationcore.h)

Retrieves a fragment pointer for a fragment that is adjacent to the windowless Microsoft ActiveX control owned by this control site.

## Syntax

```
HRESULT GetAdjacentFragment(
  [in]          NavigateDirection           direction,
  [out, retval] IRawElementProviderFragment **ppParent
);
```

## Parameters

`[in] direction`

Type: **[NavigateDirection](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-navigatedirection)**

A value that indicates the adjacent fragment to retrieve (parent, next sibling, previous sibling, and so on).

`[out, retval] ppParent`

Type: **[IRawElementProviderFragment](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementproviderfragment)\*\***

Receives the adjacent fragment.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns S\_OK. Otherwise, it returns an **HRESULT** error code. The return value is E\_INVALIDARG if the direction is [NavigateDirection\_FirstChild](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-navigatedirection) or [NavigateDirection\_LastChild](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-navigatedirection), which are not valid for this method. If there is no adjacent fragment in the requested direction, the method returns S\_OK and sets *ppRetVal* to **NULL**.

## Remarks

To return the parent of the fragment, an object that implements the [IRawElementProviderFragment](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementproviderfragment) interface must be able to implement the [Navigate](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-irawelementproviderfragment-navigate) method. Implementing **Navigate** is difficult for a windowless ActiveX control because the control might be unable to determine its location in the accessible tree of the parent object. The **GetAdjacentFragment** method enables the windowless ActiveX control to query its site for the adjacent fragment, and then return that fragment to the client that called **Navigate**.

A provider typically calls this method as part of handling the [IRawElementProviderFragment::Navigate](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-irawelementproviderfragment-navigate) method.

#### Examples

The following C++ code example shows how to implement the **GetAdjacentFragment** method.

```
IFACEMETHODIMP CProviderWindowlessSite::GetAdjacentFragment(
        enum NavigateDirection direction, IRawElementProviderFragment **ppFragment)   
{
    if (ppFragment == NULL)
    {
        return E_INVALIDARG;
    }
    
    *ppFragment = NULL;
    HRESULT hr = S_OK;

    switch (direction)
    {
        case NavigateDirection_Parent:
            {  
                IRawElementProviderSimple *pSimple = NULL;

                // Call an application-defined function to retrieve the
                // parent provider interface.
                hr = GetParentProvider(&pSimple);  
                if (SUCCEEDED(hr))  
                {  
                    // Get the parent's IRawElementProviderFragment interface.
                    hr = pSimple->QueryInterface(IID_PPV_ARGS(ppFragment));  
                    pSimple->Release();  
                } 
            }  
            break;  
  
        case NavigateDirection_FirstChild:
        case NavigateDirection_LastChild:
            hr = E_INVALIDARG;
            break;

        // Ignore NavigateDirection_NextSibling and NavigateDirection_PreviousSibling
        // because there are no adjacent fragments.
        default:  
            break;  
    }  
  
    return hr;  
}
```

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2012 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[IRawElementProviderWindowlessSite](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementproviderwindowlesssite)

---
