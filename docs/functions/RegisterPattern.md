# RegisterPattern

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-iuiautomationregistrar-registerpattern)

# IUIAutomationRegistrar::RegisterPattern method (uiautomationcore.h)

Registers a third-party control pattern.

## Syntax

```
HRESULT RegisterPattern(
  [in]  const UIAutomationPatternInfo *pattern,
  [out] PATTERNID                     *pPatternId,
  [out] PROPERTYID                    *pPatternAvailablePropertyId,
  [in]  UINT                          propertyIdCount,
  [out] PROPERTYID                    *pPropertyIds,
  [in]  UINT                          eventIdCount,
  [out] EVENTID                       *pEventIds
);
```

## Parameters

`[in] pattern`

Type: **[UIAutomationPatternInfo](/en-us/windows/desktop/api/uiautomationcore/ns-uiautomationcore-uiautomationpatterninfo)\***

A pointer to a structure that contains information about the control pattern to register.

`[out] pPatternId`

Type: **PATTERNID\***

Receives the pattern identifier.

`[out] pPatternAvailablePropertyId`

Type: **PROPERTYID\***

Receives the property identifier for the pattern. This value can be used with UI Automation client methods to determine whether the element supports the new pattern. This is equivalent to values such as [UIA\_IsInvokePatternAvailablePropertyId](/en-us/windows/desktop/WinAuto/uiauto-control-pattern-availability-propids).

`[in] propertyIdCount`

Type: **[UINT](/en-us/windows/desktop/WinProg/windows-data-types)**

The number of properties supported by the control pattern.

`[out] pPropertyIds`

Type: **PROPERTYID\***

Receives an array of identifiers for properties supported by the pattern.

`[in] eventIdCount`

Type: **[UINT](/en-us/windows/desktop/WinProg/windows-data-types)**

The number of events supported by the control pattern.

`[out] pEventIds`

Type: **EVENTID\***

Receives an array of identifiers for events that are raised by the pattern.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

The pattern, property, and event IDs retrieved by this method can be used in [IAccessibleEx](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iaccessibleex) implementations.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[IUIAutomationRegistrar](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iuiautomationregistrar)

---
