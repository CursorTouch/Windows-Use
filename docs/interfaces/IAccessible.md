# IAccessible

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nn-oleacc-iaccessible)

# IAccessible interface (oleacc.h)

Exposes methods and properties that make a user interface element and its children accessible to client applications.

## Inheritance

The **IAccessible** interface inherits from the [IDispatch](/en-us/previous-versions/windows/desktop/api/oaidl/nn-oaidl-idispatch) interface. **IAccessible** also has these types of members:

## Methods

The **IAccessible** interface has these methods.

|  |
| --- |
| [IAccessible::accDoDefaultAction](nf-oleacc-iaccessible-accdodefaultaction)   The IAccessible::accDoDefaultAction method performs the specified object's default action. Not all objects have a default action. |
| [IAccessible::accHitTest](nf-oleacc-iaccessible-acchittest)   The IAccessible::accHitTest method retrieves the child element or child object that is displayed at a specific point on the screen. |
| [IAccessible::accLocation](nf-oleacc-iaccessible-acclocation)   The IAccessible::accLocation method retrieves the specified object's current screen location. All visual objects must support this method. Sound objects do not support this method. |
| [IAccessible::accNavigate](nf-oleacc-iaccessible-accnavigate)   The IAccessible::accNavigate method traverses to another UI element within a container and retrieves the object. This method is optional. |
| [IAccessible::accSelect](nf-oleacc-iaccessible-accselect)   The IAccessible::accSelect method modifies the selection or moves the keyboard focus of the specified object. All objects that support selection or receive the keyboard focus must support this method. |
| [IAccessible::get\_accChild](nf-oleacc-iaccessible-get_accchild)   The IAccessible::get\_accChild method retrieves an IDispatch for the specified child, if one exists. All objects must support this property. |
| [IAccessible::get\_accChildCount](nf-oleacc-iaccessible-get_accchildcount)   The IAccessible::get\_accChildCount method retrieves the number of children that belong to this object. All objects must support this property. |
| [IAccessible::get\_accDefaultAction](nf-oleacc-iaccessible-get_accdefaultaction)   The IAccessible::get\_accDefaultAction method retrieves a string that indicates the object's default action. Not all objects have a default action. |
| [IAccessible::get\_accDescription](nf-oleacc-iaccessible-get_accdescription)   The IAccessible::get\_accDescription method retrieves a string that describes the visual appearance of the specified object. Not all objects have a description. |
| [IAccessible::get\_accFocus](nf-oleacc-iaccessible-get_accfocus)   The IAccessible::get\_accFocus method retrieves the object that has the keyboard focus. All objects that may receive the keyboard focus must support this property. |
| [IAccessible::get\_accHelp](nf-oleacc-iaccessible-get_acchelp)   The IAccessible::get\_accHelp method retrieves the Help property string of an object. Not all objects support this property. |
| [IAccessible::get\_accHelpTopic](nf-oleacc-iaccessible-get_acchelptopic)   The IAccessible::get\_accHelpTopic method retrieves the full path of the WinHelp file that is associated with the specified object; it also retrieves the identifier of the appropriate topic within that file. |
| [IAccessible::get\_accKeyboardShortcut](nf-oleacc-iaccessible-get_acckeyboardshortcut)   The IAccessible::get\_accKeyboardShortcut method retrieves the specified object's shortcut key or access key, also known as the mnemonic. All objects that have a shortcut key or an access key support this property. |
| [IAccessible::get\_accName](nf-oleacc-iaccessible-get_accname)   The IAccessible::get\_accName method retrieves the name of the specified object. All objects support this property. |
| [IAccessible::get\_accParent](nf-oleacc-iaccessible-get_accparent)   The IAccessible::get\_accParent method retrieves the IDispatch of the object's parent. All objects support this property. |
| [IAccessible::get\_accRole](nf-oleacc-iaccessible-get_accrole)   The IAccessible::get\_accRole method retrieves information that describes the role of the specified object. All objects support this property. |
| [IAccessible::get\_accSelection](nf-oleacc-iaccessible-get_accselection)   The IAccessible::get\_accSelection method retrieves the selected children of this object. All objects that support selection must support this property. |
| [IAccessible::get\_accState](nf-oleacc-iaccessible-get_accstate)   The IAccessible::get\_accState method retrieves the current state of the specified object. All objects support this property. |
| [IAccessible::get\_accValue](nf-oleacc-iaccessible-get_accvalue)   The IAccessible::get\_accValue method retrieves the value of the specified object. Not all objects have a value. |
| [IAccessible::put\_accName](nf-oleacc-iaccessible-put_accname)   The IAccessible::put\_accName method is no longer supported. Client applications should use a control-specific workaround, such as the SetWindowText function. Servers should return E\_NOTIMPL. |
| [IAccessible::put\_accValue](nf-oleacc-iaccessible-put_accvalue)   The IAccessible::put\_accValue method sets the value of the specified object. Not all objects have a value. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 2000 Professional [desktop apps only] |
| **Minimum supported server** | Windows 2000 Server [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | oleacc.h |

## See also

[IDispatch](/en-us/windows/desktop/WinAuto/idispatch-interface)

---
