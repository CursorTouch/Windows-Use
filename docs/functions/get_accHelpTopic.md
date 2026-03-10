# get_accHelpTopic

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-iaccessible-get_acchelptopic)

# IAccessible::get\_accHelpTopic method (oleacc.h)

The **IAccessible::get\_accHelpTopic** method retrieves the full path of the WinHelp file that is associated with the specified object; it also retrieves the identifier of the appropriate topic within that file. Not all objects support this property. This property is rarely supported or used by applications

**Note**  **IAccessible::get\_accHelpTopic** is deprecated and should not be used.

## Syntax

```
HRESULT get_accHelpTopic(
  [out] BSTR    *pszHelpFile,
  [in]  VARIANT varChild,
        long    *pidTopic
);
```

## Parameters

`[out] pszHelpFile`

Type: **BSTR\***

Address of a **BSTR** that receives the full path of the WinHelp file that is associated with the specified object.

`[in] varChild`

Type: **VARIANT**

Specifies whether the retrieved Help topic belongs to the object or one of the object's child elements. This parameter is either CHILDID\_SELF (to obtain a Help topic for the object) or a child ID (to obtain a Help topic for one of the object's child elements). For more information about initializing the [VARIANT](/en-us/windows/desktop/WinAuto/variant-structure), see [How Child IDs Are Used in Parameters](/en-us/windows/desktop/WinAuto/how-child-ids-are-used-in-parameters).

`pidTopic`

Type: **long\***

[out, retval] Address of a variable that identifies the Help file topic associated with the specified object. This value is used as the context identifier of the desired topic that passes to the [WinHelp](/en-us/windows/win32/api/winuser/nf-winuser-winhelpa) function. When calling [WinHelp](/en-us/windows/win32/api/winuser/nf-winuser-winhelpa) to display the topic, set the *uCommand* parameter to HELP\_CONTEXT, cast the value pointed to by *pidTopic* to a **DWORD**, and pass it as the *dwData* parameter.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns S\_OK.

If not successful, returns one of the values in the table that follows, or another standard [COM error code](/en-us/windows/desktop/WinAuto/return-values). Servers return these values, but clients must always check output parameters to ensure that they contain valid values. For more information, see [Checking IAccessible Return Values](/en-us/windows/desktop/WinAuto/checking-iaccessible-return-values).

| Error | Description |
| --- | --- |
| **S\_FALSE** | No Help information is available. |
| **E\_INVALIDARG** | An argument is not valid. |
| **DISP\_E\_MEMBERNOTFOUND** | The object does not support this property. |

## Remarks

Getting information from a Help file might be time and memory intensive.

**Note to server developers:**This property provides access to a Help topic in WinHelp, whereas [IAccessible::get\_accHelp](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessible-get_acchelp) returns a string. Objects are not required to support both **IAccessible::get\_accHelp** and **IAccessible::get\_accHelpTopic**, but they must support at least one. If they can easily return a string, they must support **IAccessible::get\_accHelp**; otherwise they must support **IAccessible::get\_accHelpTopic**. If both are supported, **IAccessible::get\_accHelpTopic** provides more detailed information.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 2000 Professional [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | oleacc.h |
| **Library** | Oleacc.lib |
| **DLL** | Oleacc.dll |
| **Redistributable** | Active Accessibility 1.3 RDK on Windows NT 4.0 with SP6 and later and Windows 95 |

## See also

[HelpTopic Property](/en-us/windows/desktop/WinAuto/helptopic-property)

[IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible)

[IAccessible::get\_accHelp](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessible-get_acchelp)

---
