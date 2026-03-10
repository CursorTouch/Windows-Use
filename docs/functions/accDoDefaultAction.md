# accDoDefaultAction

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-iaccessible-accdodefaultaction)

# IAccessible::accDoDefaultAction method (oleacc.h)

The **IAccessible::accDoDefaultAction** method performs the specified object's default action. Not all objects have a default action.

## Syntax

```
HRESULT accDoDefaultAction(
  [in] VARIANT varChild
);
```

## Parameters

`[in] varChild`

Type: **VARIANT**

Specifies whether the default action belongs to the object or one of the object's child elements. For more information about initializing the [VARIANT](/en-us/windows/desktop/WinAuto/variant-structure), see [How Child IDs Are Used in Parameters](/en-us/windows/desktop/WinAuto/how-child-ids-are-used-in-parameters).

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns S\_OK.

If not successful, returns one of the values in the table that follows, or another standard [COM error code](/en-us/windows/desktop/WinAuto/return-values).

| Error | Description |
| --- | --- |
| **DISP\_E\_MEMBERNOTFOUND** | The object does not support the method. This value is returned for controls that do not perform actions, such as edit fields. |
| **E\_INVALIDARG** | An argument is not valid. |

## Remarks

Clients retrieve a string that describes the object's default action by calling **IAccessible::get\_accDefaultAction**.

**Note to client developers:**When used on a menu item in a standard system menu, **accDoDefaultAction** returns S\_OK but fails to perform the action if the character used in the access key (the underlined character in the text of a menu item name, also called a mnemonic) is ?, !, @, or any other character that requires the SHIFT key or another modifier key. This also happens on international keyboards with an access key character that requires the ALT GR key to be pressed. This is not an issue for menus in other applications, such as Microsoft Office or Windows Internet Explorer. For more information about access keys, see [IAccessible::get\_accKeyboardShortcut](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessible-get_acckeyboardshortcut).

Also, while **accDoDefaultAction** is supposed to return immediately, some implementations block the return. For example, if clicking a link displays a dialog, some implementations will block the return until the dialog is dismissed. Such delays can prevent client applications from processing a dialog box. Servers should avoid implementations that block returns.

### Server Example

The following example shows a possible implementation for a custom list control whose default action is a double-click a child item. To prevent blocking, the method posts a custom message that, when received by the control window, triggers an action, such as displaying item properties.

```
// Assume a previous definition such as this: 
// #define CUSTOMLB_DEFERDOUBLECLICK   (WM_USER + 1) 

HRESULT STDMETHODCALLTYPE AccServer::accDoDefaultAction( 
    VARIANT varChild) 
{
    if (varChild.vt != VT_I4)
    {
        return E_INVALIDARG;
    }
    if (varChild.lVal != CHILDID_SELF)
    {
        // It is assumed that the control does its own checking to see which 
        // item has the focus when it receives this message.
        PostMessage(m_hwnd, CUSTOMLB_DEFERDOUBLECLICK, 0, 0);
    }
    return S_OK;
};
```

### Client Example

The following example function performs the default action on a control.

```
HRESULT DoAction(IAccessible* pAcc)
{
        VARIANT varId;
        varId.vt = VT_I4;
        varId.lVal = CHILDID_SELF;
        return pAcc->accDoDefaultAction(varId);
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
| **Redistributable** | Active Accessibility 1.3 RDK on Windows NT Server 4.0 with SP6 and later and Windows 95 |

## See also

[Appendix A: Supported User Interface Elements Reference](/en-us/windows/desktop/WinAuto/appendix-a--supported-user-interface-elements-reference)

[DefaultAction Property](/en-us/windows/desktop/WinAuto/defaultaction-property)

[IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible)

[IAccessible::get\_accDefaultAction](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessible-get_accdefaultaction)

[IAccessible::get\_accKeyboardShortcut](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessible-get_acckeyboardshortcut)

[VARIANT](/en-us/windows/desktop/WinAuto/variant-structure)

---
