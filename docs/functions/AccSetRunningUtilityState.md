# AccSetRunningUtilityState

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-accsetrunningutilitystate)

# AccSetRunningUtilityState function (oleacc.h)

Sets system values that indicate whether an assistive technology (AT) application's current state affects functionality that is typically provided by the system.

## Syntax

```
HRESULT AccSetRunningUtilityState(
  [in] HWND  hwndApp,
  [in] DWORD dwUtilityStateMask,
  [in] DWORD dwUtilityState
);
```

## Parameters

`[in] hwndApp`

Type: **HWND**

The handle of the AT application window. This parameter must not be **NULL**.

`[in] dwUtilityStateMask`

Type: **DWORD**

A  
mask that indicates the system values being set. It can be a combination of the following values:

#### ANRUS\_ON\_SCREEN\_KEYBOARD\_ACTIVE

#### ANRUS\_TOUCH\_MODIFICATION\_ACTIVE

#### ANRUS\_PRIORITY\_AUDIO\_ACTIVE

#### ANRUS\_PRIORITY\_AUDIO\_ACTIVE\_NODUCK

`[in] dwUtilityState`

Type: **DWORD**

The new settings for the system values indicated by *dwUtilityStateMask*. This parameter can be zero to reset the system values, or a combination of the following values.

| Value | Meaning |
| --- | --- |
| **ANRUS\_ON\_SCREEN\_KEYBOARD\_ACTIVE**  0x0000001 | The AT application is providing an on-screen keyboard. |
| **ANRUS\_TOUCH\_MODIFICATION\_ACTIVE**  0x0000002 | The AT application is consuming redirected touch input. |
| **ANRUS\_PRIORITY\_AUDIO\_ACTIVE**  0x0000004 | The AT application is relying on audio (such as text-to-speech) to convey essential information to the user and should remain audible over other system sounds. |
| **ANRUS\_PRIORITY\_AUDIO\_ACTIVE\_NODUCK**  0x0000008 | The AT application is relying on audio (such as text-to-speech) to convey essential information to the user but should not change relative to other system sounds. |

## Return value

Type: **STDAPI**

If successful, returns S\_OK.

If not successful, returns a standard [COM error code](/en-us/windows/desktop/WinAuto/return-values).

## Remarks

Before it exits, an AT application should reset any system values that it previously set.

This function requires the calling process to have UIAccess or higher privileges. If the caller does not have the required privileges, the call to **AccSetRunningUtilityState** fails and returns **E\_ACCESSDENIED**. For more information, see [Security Considerations for Assistive Technologies](/en-us/windows/desktop/WinAuto/uiauto-securityoverview) and [/MANIFESTUAC (Embeds UAC information in manifest)](/en-us/cpp/build/reference/manifestuac-embeds-uac-information-in-manifest).

#### Examples

This code example shows how to call the **AccSetRunningUtilityState** function.

```
if (SUCCEEDED(hr))
{
    // Tell the system that an AT application has registered with the 
    // touch redirector.
    hr = AccSetRunningUtilityState(hwndTouchWindow, 
            ANRUS_TOUCH_MODIFICATION_ACTIVE, 
            ANRUS_TOUCH_MODIFICATION_ACTIVE);
    if (FAILED(hr))
    {
        MyErrorHandler(hr); // Application-defined error handler
    }
}
```

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps only] |
| **Minimum supported server** | Windows Server 2012 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | oleacc.h |
| **Library** | Oleacc.lib |
| **DLL** | Oleacc.dll |

## See also

[Security Considerations for Assistive Technologies](/en-us/windows/desktop/WinAuto/uiauto-securityoverview)

---
