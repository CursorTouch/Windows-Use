# IUIAutomationElement

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement)

# IUIAutomationElement interface (uiautomationclient.h)

Exposes methods and properties for a UI Automation element, which represents a UI item.

## Inheritance

The **IUIAutomationElement** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IUIAutomationElement** also has these types of members:

## Methods

The **IUIAutomationElement** interface has these methods.

|  |
| --- |
| [IUIAutomationElement::BuildUpdatedCache](nf-uiautomationclient-iuiautomationelement-buildupdatedcache)   Retrieves a new UI Automation element with an updated cache. |
| [IUIAutomationElement::FindAll](nf-uiautomationclient-iuiautomationelement-findall)   Returns all UI Automation elements that satisfy the specified condition. |
| [IUIAutomationElement::FindAllBuildCache](nf-uiautomationclient-iuiautomationelement-findallbuildcache)   Returns all UI Automation elements that satisfy the specified condition, prefetches the requested properties and control patterns, and stores the prefetched items in the cache. |
| [IUIAutomationElement::FindFirst](nf-uiautomationclient-iuiautomationelement-findfirst)   Retrieves the first child or descendant element that matches the specified condition. |
| [IUIAutomationElement::FindFirstBuildCache](nf-uiautomationclient-iuiautomationelement-findfirstbuildcache)   Retrieves the first child or descendant element that matches the specified condition, prefetches the requested properties and control patterns, and stores the prefetched items in the cache. |
| [IUIAutomationElement::get\_CachedAcceleratorKey](nf-uiautomationclient-iuiautomationelement-get_cachedacceleratorkey)   Retrieves the cached accelerator key for the element. |
| [IUIAutomationElement::get\_CachedAccessKey](nf-uiautomationclient-iuiautomationelement-get_cachedaccesskey)   Retrieves the cached access key character for the element. |
| [IUIAutomationElement::get\_CachedAriaProperties](nf-uiautomationclient-iuiautomationelement-get_cachedariaproperties)   Retrieves the cached Accessible Rich Internet Applications (ARIA) properties of the element. |
| [IUIAutomationElement::get\_CachedAriaRole](nf-uiautomationclient-iuiautomationelement-get_cachedariarole)   Retrieves the cached Accessible Rich Internet Applications (ARIA) role of the element. |
| [IUIAutomationElement::get\_CachedAutomationId](nf-uiautomationclient-iuiautomationelement-get_cachedautomationid)   Retrieves the cached Microsoft UI Automation identifier of the element. |
| [IUIAutomationElement::get\_CachedBoundingRectangle](nf-uiautomationclient-iuiautomationelement-get_cachedboundingrectangle)   Retrieves the cached coordinates of the rectangle that completely encloses the element. |
| [IUIAutomationElement::get\_CachedClassName](nf-uiautomationclient-iuiautomationelement-get_cachedclassname)   Retrieves the cached class name of the element. |
| [IUIAutomationElement::get\_CachedControllerFor](nf-uiautomationclient-iuiautomationelement-get_cachedcontrollerfor)   Retrieves a cached array of UI Automation elements for which this element serves as the controller. |
| [IUIAutomationElement::get\_CachedControlType](nf-uiautomationclient-iuiautomationelement-get_cachedcontroltype)   Retrieves a cached value that indicates the control type of the element. |
| [IUIAutomationElement::get\_CachedCulture](nf-uiautomationclient-iuiautomationelement-get_cachedculture)   Retrieves a cached value that indicates the culture associated with the element. |
| [IUIAutomationElement::get\_CachedDescribedBy](nf-uiautomationclient-iuiautomationelement-get_cacheddescribedby)   Retrieves a cached array of elements that describe this element. |
| [IUIAutomationElement::get\_CachedFlowsTo](nf-uiautomationclient-iuiautomationelement-get_cachedflowsto)   Retrieves a cached array of elements that indicate the reading order after the current element. |
| [IUIAutomationElement::get\_CachedFrameworkId](nf-uiautomationclient-iuiautomationelement-get_cachedframeworkid)   Retrieves the cached name of the underlying UI framework associated with the element. |
| [IUIAutomationElement::get\_CachedHasKeyboardFocus](nf-uiautomationclient-iuiautomationelement-get_cachedhaskeyboardfocus)   A cached value that indicates whether the element has keyboard focus. |
| [IUIAutomationElement::get\_CachedHelpText](nf-uiautomationclient-iuiautomationelement-get_cachedhelptext)   Retrieves the cached help text for the element. |
| [IUIAutomationElement::get\_CachedIsContentElement](nf-uiautomationclient-iuiautomationelement-get_cachediscontentelement)   A cached value that indicates whether the element is a content element. |
| [IUIAutomationElement::get\_CachedIsControlElement](nf-uiautomationclient-iuiautomationelement-get_cachediscontrolelement)   Retrieves a cached value that indicates whether the element is a control element. |
| [IUIAutomationElement::get\_CachedIsDataValidForForm](nf-uiautomationclient-iuiautomationelement-get_cachedisdatavalidforform)   Retrieves a cached value that indicates whether the element contains valid data for the form. |
| [IUIAutomationElement::get\_CachedIsEnabled](nf-uiautomationclient-iuiautomationelement-get_cachedisenabled)   Retrieves a cached value that indicates whether the element is enabled. |
| [IUIAutomationElement::get\_CachedIsKeyboardFocusable](nf-uiautomationclient-iuiautomationelement-get_cachediskeyboardfocusable)   Retrieves a cached value that indicates whether the element can accept keyboard focus. |
| [IUIAutomationElement::get\_CachedIsOffscreen](nf-uiautomationclient-iuiautomationelement-get_cachedisoffscreen)   Retrieves a cached value that indicates whether the element is off-screen. |
| [IUIAutomationElement::get\_CachedIsPassword](nf-uiautomationclient-iuiautomationelement-get_cachedispassword)   Retrieves a cached value that indicates whether the element contains a disguised password. |
| [IUIAutomationElement::get\_CachedIsRequiredForForm](nf-uiautomationclient-iuiautomationelement-get_cachedisrequiredforform)   Retrieves a cached value that indicates whether the element is required to be filled out on a form. |
| [IUIAutomationElement::get\_CachedItemStatus](nf-uiautomationclient-iuiautomationelement-get_cacheditemstatus)   Retrieves a cached description of the status of an item within an element. |
| [IUIAutomationElement::get\_CachedItemType](nf-uiautomationclient-iuiautomationelement-get_cacheditemtype)   Retrieves a cached string that describes the type of item represented by the element. |
| [IUIAutomationElement::get\_CachedLabeledBy](nf-uiautomationclient-iuiautomationelement-get_cachedlabeledby)   Retrieves the cached element that contains the text label for this element. |
| [IUIAutomationElement::get\_CachedLocalizedControlType](nf-uiautomationclient-iuiautomationelement-get_cachedlocalizedcontroltype)   Retrieves the cached localized description of the control type of the element. |
| [IUIAutomationElement::get\_CachedName](nf-uiautomationclient-iuiautomationelement-get_cachedname)   Retrieves the cached name of the element. |
| [IUIAutomationElement::get\_CachedNativeWindowHandle](nf-uiautomationclient-iuiautomationelement-get_cachednativewindowhandle)   Retrieves the cached window handle of the element. |
| [IUIAutomationElement::get\_CachedOrientation](nf-uiautomationclient-iuiautomationelement-get_cachedorientation)   Retrieves a cached value that indicates the orientation of the element. |
| [IUIAutomationElement::get\_CachedProcessId](nf-uiautomationclient-iuiautomationelement-get_cachedprocessid)   Retrieves the cached ID of the process that hosts the element. |
| [IUIAutomationElement::get\_CachedProviderDescription](nf-uiautomationclient-iuiautomationelement-get_cachedproviderdescription)   Retrieves a cached description of the provider for this element. |
| [IUIAutomationElement::get\_CurrentAcceleratorKey](nf-uiautomationclient-iuiautomationelement-get_currentacceleratorkey)   Retrieves the accelerator key for the element. |
| [IUIAutomationElement::get\_CurrentAccessKey](nf-uiautomationclient-iuiautomationelement-get_currentaccesskey)   Retrieves the access key character for the element. |
| [IUIAutomationElement::get\_CurrentAriaProperties](nf-uiautomationclient-iuiautomationelement-get_currentariaproperties)   Retrieves the Accessible Rich Internet Applications (ARIA) properties of the element. |
| [IUIAutomationElement::get\_CurrentAriaRole](nf-uiautomationclient-iuiautomationelement-get_currentariarole)   Retrieves the Accessible Rich Internet Applications (ARIA) role of the element. |
| [IUIAutomationElement::get\_CurrentAutomationId](nf-uiautomationclient-iuiautomationelement-get_currentautomationid)   Retrieves the Microsoft UI Automation identifier of the element. |
| [IUIAutomationElement::get\_CurrentBoundingRectangle](nf-uiautomationclient-iuiautomationelement-get_currentboundingrectangle)   Retrieves the coordinates of the rectangle that completely encloses the element. |
| [IUIAutomationElement::get\_CurrentClassName](nf-uiautomationclient-iuiautomationelement-get_currentclassname)   Retrieves the class name of the element. |
| [IUIAutomationElement::get\_CurrentControllerFor](nf-uiautomationclient-iuiautomationelement-get_currentcontrollerfor)   Retrieves an array of elements for which this element serves as the controller. |
| [IUIAutomationElement::get\_CurrentControlType](nf-uiautomationclient-iuiautomationelement-get_currentcontroltype)   Retrieves the control type of the element. |
| [IUIAutomationElement::get\_CurrentCulture](nf-uiautomationclient-iuiautomationelement-get_currentculture)   Retrieves the culture identifier for the element. |
| [IUIAutomationElement::get\_CurrentDescribedBy](nf-uiautomationclient-iuiautomationelement-get_currentdescribedby)   Retrieves an array of elements that describe this element. |
| [IUIAutomationElement::get\_CurrentFlowsTo](nf-uiautomationclient-iuiautomationelement-get_currentflowsto)   Retrieves an array of elements that indicates the reading order after the current element. |
| [IUIAutomationElement::get\_CurrentFrameworkId](nf-uiautomationclient-iuiautomationelement-get_currentframeworkid)   Retrieves the name of the underlying UI framework. |
| [IUIAutomationElement::get\_CurrentHasKeyboardFocus](nf-uiautomationclient-iuiautomationelement-get_currenthaskeyboardfocus)   Indicates whether the element has keyboard focus. |
| [IUIAutomationElement::get\_CurrentHelpText](nf-uiautomationclient-iuiautomationelement-get_currenthelptext)   Retrieves the help text for the element. |
| [IUIAutomationElement::get\_CurrentIsContentElement](nf-uiautomationclient-iuiautomationelement-get_currentiscontentelement)   Indicates whether the element is a content element. |
| [IUIAutomationElement::get\_CurrentIsControlElement](nf-uiautomationclient-iuiautomationelement-get_currentiscontrolelement)   Indicates whether the element is a control element. |
| [IUIAutomationElement::get\_CurrentIsDataValidForForm](nf-uiautomationclient-iuiautomationelement-get_currentisdatavalidforform)   Indicates whether the element contains valid data for a form. |
| [IUIAutomationElement::get\_CurrentIsEnabled](nf-uiautomationclient-iuiautomationelement-get_currentisenabled)   Indicates whether the element is enabled. |
| [IUIAutomationElement::get\_CurrentIsKeyboardFocusable](nf-uiautomationclient-iuiautomationelement-get_currentiskeyboardfocusable)   Indicates whether the element can accept keyboard focus. |
| [IUIAutomationElement::get\_CurrentIsOffscreen](nf-uiautomationclient-iuiautomationelement-get_currentisoffscreen)   Indicates whether the element is off-screen. |
| [IUIAutomationElement::get\_CurrentIsPassword](nf-uiautomationclient-iuiautomationelement-get_currentispassword)   Indicates whether the element contains a disguised password. |
| [IUIAutomationElement::get\_CurrentIsRequiredForForm](nf-uiautomationclient-iuiautomationelement-get_currentisrequiredforform)   Indicates whether the element is required to be filled out on a form. |
| [IUIAutomationElement::get\_CurrentItemStatus](nf-uiautomationclient-iuiautomationelement-get_currentitemstatus)   Retrieves the description of the status of an item in an element. |
| [IUIAutomationElement::get\_CurrentItemType](nf-uiautomationclient-iuiautomationelement-get_currentitemtype)   Retrieves a description of the type of UI item represented by the element. |
| [IUIAutomationElement::get\_CurrentLabeledBy](nf-uiautomationclient-iuiautomationelement-get_currentlabeledby)   Retrieves the element that contains the text label for this element. |
| [IUIAutomationElement::get\_CurrentLocalizedControlType](nf-uiautomationclient-iuiautomationelement-get_currentlocalizedcontroltype)   Retrieves a localized description of the control type of the element. |
| [IUIAutomationElement::get\_CurrentName](nf-uiautomationclient-iuiautomationelement-get_currentname)   Retrieves the name of the element. |
| [IUIAutomationElement::get\_CurrentNativeWindowHandle](nf-uiautomationclient-iuiautomationelement-get_currentnativewindowhandle)   Retrieves the window handle of the element. |
| [IUIAutomationElement::get\_CurrentOrientation](nf-uiautomationclient-iuiautomationelement-get_currentorientation)   Retrieves a value that indicates the orientation of the element. |
| [IUIAutomationElement::get\_CurrentProcessId](nf-uiautomationclient-iuiautomationelement-get_currentprocessid)   Retrieves the identifier of the process that hosts the element. |
| [IUIAutomationElement::get\_CurrentProviderDescription](nf-uiautomationclient-iuiautomationelement-get_currentproviderdescription)   Retrieves a description of the provider for this element. |
| [IUIAutomationElement::GetCachedChildren](nf-uiautomationclient-iuiautomationelement-getcachedchildren)   Retrieves the cached child elements of this UI Automation element. |
| [IUIAutomationElement::GetCachedParent](nf-uiautomationclient-iuiautomationelement-getcachedparent)   Retrieves from the cache the parent of this UI Automation element. |
| [IUIAutomationElement::GetCachedPattern](nf-uiautomationclient-iuiautomationelement-getcachedpattern)   Retrieves from the cache the IUnknown interface of the specified control pattern of this UI Automation element. |
| [IUIAutomationElement::GetCachedPatternAs](nf-uiautomationclient-iuiautomationelement-getcachedpatternas)   Retrieves the control pattern interface of the specified pattern from the cache of this UI Automation element. |
| [IUIAutomationElement::GetCachedPropertyValue](nf-uiautomationclient-iuiautomationelement-getcachedpropertyvalue)   Retrieves a property value from the cache for this UI Automation element. |
| [IUIAutomationElement::GetCachedPropertyValueEx](nf-uiautomationclient-iuiautomationelement-getcachedpropertyvalueex)   Retrieves a property value from the cache for this UI Automation element, optionally ignoring any default value. |
| [IUIAutomationElement::GetClickablePoint](nf-uiautomationclient-iuiautomationelement-getclickablepoint)   Retrieves a point on the element that can be clicked. |
| [IUIAutomationElement::GetCurrentPattern](nf-uiautomationclient-iuiautomationelement-getcurrentpattern)   Retrieves the IUnknown interface of the specified control pattern on this UI Automation element. |
| [IUIAutomationElement::GetCurrentPatternAs](nf-uiautomationclient-iuiautomationelement-getcurrentpatternas)   Retrieves the control pattern interface of the specified pattern on this UI Automation element. |
| [IUIAutomationElement::GetCurrentPropertyValue](nf-uiautomationclient-iuiautomationelement-getcurrentpropertyvalue)   Retrieves the current value of a property for this UI Automation element. |
| [IUIAutomationElement::GetCurrentPropertyValueEx](nf-uiautomationclient-iuiautomationelement-getcurrentpropertyvalueex)   Retrieves a property value for this UI Automation element, optionally ignoring any default value. |
| [IUIAutomationElement::GetRuntimeId](nf-uiautomationclient-iuiautomationelement-getruntimeid)   Retrieves the unique identifier assigned to the UI element. |
| [IUIAutomationElement::SetFocus](nf-uiautomationclient-iuiautomationelement-setfocus)   Sets the keyboard focus to this UI Automation element. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[UI Automation Element Interfaces for Clients](/en-us/windows/desktop/WinAuto/uiauto-entry-uiautoclientinterfaces)

---
