# get_accState

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-iaccessible-get_accstate)

# IAccessible::get\_accState method (oleacc.h)

The **IAccessible::get\_accState** method retrieves the current state of the specified object. All objects support this property.

## Syntax

```
HRESULT get_accState(
  [in]          VARIANT varChild,
  [out, retval] VARIANT *pvarState
);
```

## Parameters

`[in] varChild`

Type: **VARIANT**

Specifies whether the retrieved state information belongs to the object or of one of the object's child elements. This parameter is either CHILDID\_SELF (to obtain information about the object) or a child ID (to obtain information about the object's child element). For more information about initializing the [VARIANT](/en-us/windows/desktop/WinAuto/variant-structure), see [How Child IDs Are Used in Parameters](/en-us/windows/desktop/WinAuto/how-child-ids-are-used-in-parameters).

`[out, retval] pvarState`

Type: **VARIANT\***

Address of a [VARIANT structure](/en-us/windows/desktop/WinAuto/variant-structure) that receives information that describes the object's state. The **vt** member is VT\_I4, and the **lVal** member is one or more of the [object state constants](/en-us/windows/desktop/WinAuto/object-state-constants).

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns S\_OK.

If not successful, returns one of the values in the table that follows, or another standard [COM error code](/en-us/windows/desktop/WinAuto/return-values). Servers return these values, but clients must always check output parameters to ensure that they contain valid values. For more information, see [Checking IAccessible Return Values](/en-us/windows/desktop/WinAuto/checking-iaccessible-return-values).

| Error | Description |
| --- | --- |
| **E\_INVALIDARG** | An argument is not valid. |

## Remarks

If predefined state values are returned, clients call [GetStateText](/en-us/windows/desktop/api/oleacc/nf-oleacc-getstatetexta) to retrieve a localized string that describes the object's state.

The actual state of a child often depends on the state of its ancestors. For example, controls in an application's main window are not focusable when a modal dialog box is open, but the controls may not report this state. To verify the state information of a child object, call **get\_accState** for the parent object.

**Note to server developers:**You must use the predefined state constants.

### Server Example

The following example code shows a possible implementation of this method for a custom list box that maintains its own child elements (list items), only one of which can be selected at a time. If the client requests the state of the list box itself, the method passes the call to the standard accessible object that serves the control window. For child items, different flags are returned depending on whether the item is selected or not.

```
// m_pStdAccessibleObject is the standard accessible object returned by CreateAccessibleObject. 
// m_pControl is the custom control instance that returns this accessible object. 

HRESULT STDMETHODCALLTYPE AccServer::get_accState( 
    VARIANT varChild,
    VARIANT *pvarState)
{
    if (varChild.vt != VT_I4)
    {
        pvarState->vt = VT_EMPTY;
        return E_INVALIDARG;
    }
    if (varChild.lVal == CHILDID_SELF)
    {
        return m_pStdAccessibleObject->get_accState(varChild, pvarState);
    }
    else  // For list items. 
    {
        DWORD flags = STATE_SYSTEM_SELECTABLE;
        int index = (int)varChild.lVal - 1;
        if (index == m_pControl->GetSelectedIndex())
        {
            flags |= STATE_SYSTEM_SELECTED;
        }
        pvarState->vt = VT_I4;
        pvarState->lVal = flags; 
    }
    return S_OK;
};
```

### Client Example

The following example function displays the states of the specified accessible object or a child element.

```
HRESULT PrintState(IAccessible* pAcc, long childId)
{
    if (pAcc == NULL)
    {
        return E_INVALIDARG;    
    }
    VARIANT      varChild;
    varChild.vt = VT_I4;
    varChild.lVal = childId;
    VARIANT varResult;
    HRESULT hr = pAcc->get_accState(varChild, &varResult);
    long stateBits = 0;
    if ((hr == S_OK) && (varResult.vt == VT_I4))
    {
        printf("State: ");
        stateBits = (DWORD)varResult.lVal;
        for (DWORD mask = 1; mask <= 0x8000; mask <<= 1)
        {
            if (mask & stateBits)
            {

                // Get the length of the string. 
                UINT stateLength = GetStateText(mask, NULL, 0);

                // Allocate memory for the string. Add one character to 
                // the length you got in the previous call to make room 
                // for the null character. 
                LPTSTR lpszStateString = (LPTSTR)malloc(
                    (stateLength + 1) * sizeof(TCHAR));
                if (lpszStateString != NULL)
                {
                    // Get the string. 
                    GetStateText(mask, 
                        lpszStateString, stateLength + 1); 
#ifdef UNICODE
                    printf("%S\n", lpszStateString);
#else
                    printf(("%s\n", lpszStateString);
#endif
                    // Free the allocated memory
                    free(lpszStateString);
                }
                else 
                {
                    return E_OUTOFMEMORY;
                }
            }
        }
    }
    return hr;
}
```

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 2000 Professional [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | oleacc.h |
| **Library** | Oleacc.lib |
| **DLL** | Oleacc.dll |
| **Redistributable** | Active Accessibility 1.3 RDK on Windows NT 4.0 and Windows 95 |

## See also

[GetStateText](/en-us/windows/desktop/api/oleacc/nf-oleacc-getstatetexta)

[IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible)

[Object State Constants](/en-us/windows/desktop/WinAuto/object-state-constants)

[State Property](/en-us/windows/desktop/WinAuto/state-property)

[VARIANT](/en-us/windows/desktop/WinAuto/variant-structure)

---
