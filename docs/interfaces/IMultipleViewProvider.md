# IMultipleViewProvider

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-imultipleviewprovider)

# IMultipleViewProvider interface (uiautomationcore.h)

Provides access
to controls that provide, and are able to switch between, multiple representations of
the same set of information or child controls.

## Inheritance

The **IMultipleViewProvider** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IMultipleViewProvider** also has these types of members:

## Methods

The **IMultipleViewProvider** interface has these methods.

|  |
| --- |
| [IMultipleViewProvider::get\_CurrentView](nf-uiautomationcore-imultipleviewprovider-get_currentview)   Identifies the current view that the control is using to display information or child controls. |
| [IMultipleViewProvider::GetSupportedViews](nf-uiautomationcore-imultipleviewprovider-getsupportedviews)   Retrieves a collection of control-specific view identifiers. (IMultipleViewProvider.GetSupportedViews) |
| [IMultipleViewProvider::GetViewName](nf-uiautomationcore-imultipleviewprovider-getviewname)   Retrieves the name of a control-specific view. (IMultipleViewProvider.GetViewName) |
| [IMultipleViewProvider::SetCurrentView](nf-uiautomationcore-imultipleviewprovider-setcurrentview)   Sets the current control-specific view. |

## Remarks

Implemented on a Microsoft UI Automation provider that must support the
[MultipleView](/en-us/windows/desktop/WinAuto/uiauto-implementingmultipleview) control pattern.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

---
