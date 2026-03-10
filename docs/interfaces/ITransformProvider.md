# ITransformProvider

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-itransformprovider)

# ITransformProvider interface (uiautomationcore.h)

Provides access
to controls that can be moved, resized, and/or rotated within a two-dimensional space.

## Inheritance

The **ITransformProvider** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **ITransformProvider** also has these types of members:

## Methods

The **ITransformProvider** interface has these methods.

|  |
| --- |
| [ITransformProvider::get\_CanMove](nf-uiautomationcore-itransformprovider-get_canmove)   Indicates whether the control can be moved. |
| [ITransformProvider::get\_CanResize](nf-uiautomationcore-itransformprovider-get_canresize)   Indicates whether the control can be resized. |
| [ITransformProvider::get\_CanRotate](nf-uiautomationcore-itransformprovider-get_canrotate)   Indicates whether the control can be rotated. |
| [ITransformProvider::Move](nf-uiautomationcore-itransformprovider-move)   Moves the control. |
| [ITransformProvider::Resize](nf-uiautomationcore-itransformprovider-resize)   Resizes the control. |
| [ITransformProvider::Rotate](nf-uiautomationcore-itransformprovider-rotate)   Rotates the control. |

## Remarks

Implemented on a Microsoft UI Automation provider that must support the [Transform](/en-us/windows/desktop/WinAuto/uiauto-implementingtransform) control pattern.

Support for this control pattern is not limited to objects on the desktop.
This control pattern must also be implemented by the children of a
container object as long as the children can be moved, resized, or rotated freely within the boundaries of the container.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[ITransformProvider2](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-itransformprovider2)

[UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

---
