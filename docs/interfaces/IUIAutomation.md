# IUIAutomation

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomation)

# IUIAutomation interface (uiautomationclient.h)

Exposes methods that enable Microsoft UI Automation client applications to discover, access, and filter UI Automation elements. UI Automation exposes every element of the UI Automation as an object represented by the **IUIAutomation** interface. The members of this interface are not specific to a particular element.

## Inheritance

The **IUIAutomation** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IUIAutomation** also has these types of members:

## Methods

The **IUIAutomation** interface has these methods.

|  |
| --- |
| [IUIAutomation::AddAutomationEventHandler](nf-uiautomationclient-iuiautomation-addautomationeventhandler)   Registers a method that handles Microsoft UI Automation events.Note  Before implementing an event handler, you should be familiar with the threading issues described in Understanding Threading Issues. |
| [IUIAutomation::AddFocusChangedEventHandler](nf-uiautomationclient-iuiautomation-addfocuschangedeventhandler)   Registers a method that handles focus-changed events.Note  Before implementing an event handler, you should be familiar with the threading issues described in Understanding Threading Issues. |
| [IUIAutomation::AddPropertyChangedEventHandler](nf-uiautomationclient-iuiautomation-addpropertychangedeventhandler)   Registers a method that handles and array of property-changed events. |
| [IUIAutomation::AddPropertyChangedEventHandlerNativeArray](nf-uiautomationclient-iuiautomation-addpropertychangedeventhandlernativearray)   Registers a method that handles a native array of property-changed events. |
| [IUIAutomation::AddStructureChangedEventHandler](nf-uiautomationclient-iuiautomation-addstructurechangedeventhandler)   Registers a method that handles structure-changed events.Note  Before implementing an event handler, you should be familiar with the threading issues described in Understanding Threading Issues. |
| [IUIAutomation::CheckNotSupported](nf-uiautomationclient-iuiautomation-checknotsupported)   Checks a provided VARIANT to see if it contains the Not Supported identifier. |
| [IUIAutomation::CompareElements](nf-uiautomationclient-iuiautomation-compareelements)   Compares two UI Automation elements to determine whether they represent the same underlying UI element. |
| [IUIAutomation::CompareRuntimeIds](nf-uiautomationclient-iuiautomation-compareruntimeids)   Compares two integer arrays containing run-time identifiers (IDs) to determine whether their content is the same and they belong to the same UI element. |
| [IUIAutomation::CreateAndCondition](nf-uiautomationclient-iuiautomation-createandcondition)   Creates a condition that selects elements that match both of two conditions. |
| [IUIAutomation::CreateAndConditionFromArray](nf-uiautomationclient-iuiautomation-createandconditionfromarray)   Creates a condition that selects elements based on multiple conditions, all of which must be true. |
| [IUIAutomation::CreateAndConditionFromNativeArray](nf-uiautomationclient-iuiautomation-createandconditionfromnativearray)   Creates a condition that selects elements from a native array, based on multiple conditions that must all be true. |
| [IUIAutomation::CreateCacheRequest](nf-uiautomationclient-iuiautomation-createcacherequest)   Creates a cache request. |
| [IUIAutomation::CreateFalseCondition](nf-uiautomationclient-iuiautomation-createfalsecondition)   Creates a condition that is always false. |
| [IUIAutomation::CreateNotCondition](nf-uiautomationclient-iuiautomation-createnotcondition)   Creates a condition that is the negative of a specified condition. |
| [IUIAutomation::CreateOrCondition](nf-uiautomationclient-iuiautomation-createorcondition)   Creates a combination of two conditions where a match exists if either of the conditions is true. |
| [IUIAutomation::CreateOrConditionFromArray](nf-uiautomationclient-iuiautomation-createorconditionfromarray)   Creates a combination of two or more conditions where a match exists if any of the conditions is true. |
| [IUIAutomation::CreateOrConditionFromNativeArray](nf-uiautomationclient-iuiautomation-createorconditionfromnativearray)   Creates a combination of two or more conditions where a match exists if any one of the conditions is true. |
| [IUIAutomation::CreatePropertyCondition](nf-uiautomationclient-iuiautomation-createpropertycondition)   Creates a condition that selects elements that have a property with the specified value. |
| [IUIAutomation::CreatePropertyConditionEx](nf-uiautomationclient-iuiautomation-createpropertyconditionex)   Creates a condition that selects elements that have a property with the specified value, using optional flags. |
| [IUIAutomation::CreateProxyFactoryEntry](nf-uiautomationclient-iuiautomation-createproxyfactoryentry)   Creates a new instance of a proxy factory object. |
| [IUIAutomation::CreateTreeWalker](nf-uiautomationclient-iuiautomation-createtreewalker)   Retrieves a tree walker object that can be used to traverse the Microsoft UI Automation tree. |
| [IUIAutomation::CreateTrueCondition](nf-uiautomationclient-iuiautomation-createtruecondition)   Retrieves a predefined condition that selects all elements. |
| [IUIAutomation::ElementFromHandle](nf-uiautomationclient-iuiautomation-elementfromhandle)   Retrieves a UI Automation element for the specified window. |
| [IUIAutomation::ElementFromHandleBuildCache](nf-uiautomationclient-iuiautomation-elementfromhandlebuildcache)   Retrieves a UI Automation element for the specified window, prefetches the requested properties and control patterns, and stores the prefetched items in the cache. |
| [IUIAutomation::ElementFromIAccessible](nf-uiautomationclient-iuiautomation-elementfromiaccessible)   Retrieves a UI Automation element for the specified accessible object from a Microsoft Active Accessibility server. |
| [IUIAutomation::ElementFromIAccessibleBuildCache](nf-uiautomationclient-iuiautomation-elementfromiaccessiblebuildcache)   Retrieves a UI Automation element for the specified accessible object from a Microsoft Active Accessibility server, prefetches the requested properties and control patterns, and stores the prefetched items in the cache. |
| [IUIAutomation::ElementFromPoint](nf-uiautomationclient-iuiautomation-elementfrompoint)   Retrieves the UI Automation element at the specified point on the desktop. |
| [IUIAutomation::ElementFromPointBuildCache](nf-uiautomationclient-iuiautomation-elementfrompointbuildcache)   Retrieves the UI Automation element at the specified point on the desktop, prefetches the requested properties and control patterns, and stores the prefetched items in the cache. |
| [IUIAutomation::get\_ContentViewCondition](nf-uiautomationclient-iuiautomation-get_contentviewcondition)   Retrieves a predefined IUIAutomationCondition interface that selects content elements. |
| [IUIAutomation::get\_ContentViewWalker](nf-uiautomationclient-iuiautomation-get_contentviewwalker)   Retrieves an IUIAutomationTreeWalker interface used to discover content elements. |
| [IUIAutomation::get\_ControlViewCondition](nf-uiautomationclient-iuiautomation-get_controlviewcondition)   Retrieves a predefined IUIAutomationCondition interface that selects control elements. |
| [IUIAutomation::get\_ControlViewWalker](nf-uiautomationclient-iuiautomation-get_controlviewwalker)   Retrieves an IUIAutomationTreeWalker interface used to discover control elements. |
| [IUIAutomation::get\_ProxyFactoryMapping](nf-uiautomationclient-iuiautomation-get_proxyfactorymapping)   Retrieves an object that represents the mapping of Window classnames and associated data to individual proxy factories. |
| [IUIAutomation::get\_RawViewCondition](nf-uiautomationclient-iuiautomation-get_rawviewcondition)   Retrieves a predefined IUIAutomationCondition interface that selects all UI elements in an unfiltered view. |
| [IUIAutomation::get\_RawViewWalker](nf-uiautomationclient-iuiautomation-get_rawviewwalker)   Retrieves a tree walker object used to traverse an unfiltered view of the Microsoft UI Automation tree. |
| [IUIAutomation::get\_ReservedMixedAttributeValue](nf-uiautomationclient-iuiautomation-get_reservedmixedattributevalue)   Retrieves a static token object representing a text attribute that is a mixed attribute. |
| [IUIAutomation::get\_ReservedNotSupportedValue](nf-uiautomationclient-iuiautomation-get_reservednotsupportedvalue)   Retrieves a static token object representing a property or text attribute that is not supported. |
| [IUIAutomation::GetFocusedElement](nf-uiautomationclient-iuiautomation-getfocusedelement)   Retrieves the UI Automation element that has the input focus. |
| [IUIAutomation::GetFocusedElementBuildCache](nf-uiautomationclient-iuiautomation-getfocusedelementbuildcache)   Retrieves the UI Automation element that has the input focus, prefetches the requested properties and control patterns, and stores the prefetched items in the cache. |
| [IUIAutomation::GetPatternProgrammaticName](nf-uiautomationclient-iuiautomation-getpatternprogrammaticname)   Retrieves the registered programmatic name of a control pattern. |
| [IUIAutomation::GetPropertyProgrammaticName](nf-uiautomationclient-iuiautomation-getpropertyprogrammaticname)   Retrieves the registered programmatic name of a property. |
| [IUIAutomation::GetRootElement](nf-uiautomationclient-iuiautomation-getrootelement)   Retrieves the UI Automation element that represents the desktop. |
| [IUIAutomation::GetRootElementBuildCache](nf-uiautomationclient-iuiautomation-getrootelementbuildcache)   Retrieves the UI Automation element that represents the desktop, prefetches the requested properties and control patterns, and stores the prefetched items in the cache. |
| [IUIAutomation::IntNativeArrayToSafeArray](nf-uiautomationclient-iuiautomation-intnativearraytosafearray)   Converts an array of integers to a SAFEARRAY. |
| [IUIAutomation::IntSafeArrayToNativeArray](nf-uiautomationclient-iuiautomation-intsafearraytonativearray)   Converts a SAFEARRAY of integers to an array. |
| [IUIAutomation::PollForPotentialSupportedPatterns](nf-uiautomationclient-iuiautomation-pollforpotentialsupportedpatterns)   Retrieves the control patterns that might be supported on a UI Automation element. |
| [IUIAutomation::PollForPotentialSupportedProperties](nf-uiautomationclient-iuiautomation-pollforpotentialsupportedproperties)   Retrieves the properties that might be supported on a UI Automation element. |
| [IUIAutomation::RectToVariant](nf-uiautomationclient-iuiautomation-recttovariant)   Creates a VARIANT that contains the coordinates of a rectangle. |
| [IUIAutomation::RemoveAllEventHandlers](nf-uiautomationclient-iuiautomation-removealleventhandlers)   Removes all registered Microsoft UI Automation event handlers. |
| [IUIAutomation::RemoveAutomationEventHandler](nf-uiautomationclient-iuiautomation-removeautomationeventhandler)   Removes the specified UI Automation event handler. |
| [IUIAutomation::RemoveFocusChangedEventHandler](nf-uiautomationclient-iuiautomation-removefocuschangedeventhandler)   Removes a focus-changed event handler. |
| [IUIAutomation::RemovePropertyChangedEventHandler](nf-uiautomationclient-iuiautomation-removepropertychangedeventhandler)   Removes a property-changed event handler. |
| [IUIAutomation::RemoveStructureChangedEventHandler](nf-uiautomationclient-iuiautomation-removestructurechangedeventhandler)   Removes a structure-changed event handler. |
| [IUIAutomation::SafeArrayToRectNativeArray](nf-uiautomationclient-iuiautomation-safearraytorectnativearray)   Converts a SAFEARRAY containing rectangle coordinates to an array of type RECT. |
| [IUIAutomation::VariantToRect](nf-uiautomationclient-iuiautomation-varianttorect)   Converts a VARIANT containing rectangle coordinates to a RECT. |

## Remarks

Every UI Automation client application must obtain this interface to a [CUIAutomation](/en-us/previous-versions/windows/desktop/legacy/ff384838(v=vs.85)) object in order to gain access to the functionality of UI Automation.

The following example function creates a [CUIAutomation](/en-us/previous-versions/windows/desktop/legacy/ff384838(v=vs.85)) object and obtains the **IUIAutomation** interface.

```
IUIAutomation *g_pAutomation;

BOOL InitializeUIAutomation()
{
    CoInitialize(NULL);
    HRESULT hr = CoCreateInstance(__uuidof(CUIAutomation), NULL, CLSCTX_INPROC_SERVER, 
        __uuidof(IUIAutomation), (void**)&g_pAutomation);
    return (SUCCEEDED(hr));
}
```

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
