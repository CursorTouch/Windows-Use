# IAccPropServices

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nn-oleacc-iaccpropservices)

# IAccPropServices interface (oleacc.h)

Exposes methods for annotating accessible elements and for manipulating identity strings.

## Inheritance

The **IAccPropServices** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IAccPropServices** also has these types of members:

## Methods

The **IAccPropServices** interface has these methods.

|  |
| --- |
| [IAccPropServices::ClearHmenuProps](nf-oleacc-iaccpropservices-clearhmenuprops)   This method wraps ClearProps, and provides a convenient entry point for callers who are annotating HMENU-based accessible elements. |
| [IAccPropServices::ClearHwndProps](nf-oleacc-iaccpropservices-clearhwndprops)   This method wraps SetPropValue, SetPropServer, and ClearProps, and provides a convenient entry point for callers who are annotating HWND-based accessible elements. |
| [IAccPropServices::ClearProps](nf-oleacc-iaccpropservices-clearprops)   Servers use ClearProps to restore default values to properties of accessible elements that they had previously annotated. |
| [IAccPropServices::ComposeHmenuIdentityString](nf-oleacc-iaccpropservices-composehmenuidentitystring)   Callers use ComposeHmenuIdentityString to retrieve an identity string for an HMENU-based accessible element. |
| [IAccPropServices::ComposeHwndIdentityString](nf-oleacc-iaccpropservices-composehwndidentitystring)   Callers use ComposeHwndIdentityString to retrieve an identity string. |
| [IAccPropServices::DecomposeHmenuIdentityString](nf-oleacc-iaccpropservices-decomposehmenuidentitystring)   Use this method to determine the HMENU, object ID, and child ID for the accessible element identified by the identity string. |
| [IAccPropServices::DecomposeHwndIdentityString](nf-oleacc-iaccpropservices-decomposehwndidentitystring)   Use this method to determine the HWND, object ID, and child ID for the accessible element identified by the identity string. |
| [IAccPropServices::SetHmenuProp](nf-oleacc-iaccpropservices-sethmenuprop)   This method wraps SetPropValue, providing a convenient entry point for callers who are annotating HMENU-based accessible elements. If the new value is a string, you can use IAccPropServices::SetHmenuPropStr instead. |
| [IAccPropServices::SetHmenuPropServer](nf-oleacc-iaccpropservices-sethmenupropserver)   This method wraps SetPropServer, providing a convenient entry point for callers who are annotating HMENU-based accessible elements. |
| [IAccPropServices::SetHmenuPropStr](nf-oleacc-iaccpropservices-sethmenupropstr)   This method wraps SetPropValue, providing a more convenient entry point for callers who are annotating HMENU-based accessible elements. |
| [IAccPropServices::SetHwndProp](nf-oleacc-iaccpropservices-sethwndprop)   This method wraps SetPropValue, providing a convenient entry point for callers who are annotating HWND-based accessible elements. If the new value is a string, you can use IAccPropServices::SetHwndPropStr instead. |
| [IAccPropServices::SetHwndPropServer](nf-oleacc-iaccpropservices-sethwndpropserver)   This method wraps SetPropServer, providing a convenient entry point for callers who are annotating HWND-based accessible elements. |
| [IAccPropServices::SetHwndPropStr](nf-oleacc-iaccpropservices-sethwndpropstr)   This method wraps SetPropValue, providing a more convenient entry point for callers who are annotating HWND-based accessible elements. |
| [IAccPropServices::SetPropServer](nf-oleacc-iaccpropservices-setpropserver)   Servers use SetPropServer to specify a callback object to be used to annotate an array of properties for the accessible element. |
| [IAccPropServices::SetPropValue](nf-oleacc-iaccpropservices-setpropvalue)   Use SetPropValue to identify the accessible element to be annotated, specify the property to be annotated, and provide a new value for that property. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | oleacc.h |

---
