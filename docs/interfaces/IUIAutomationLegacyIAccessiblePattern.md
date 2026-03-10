# IUIAutomationLegacyIAccessiblePattern

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationlegacyiaccessiblepattern)

# IUIAutomationLegacyIAccessiblePattern interface (uiautomationclient.h)

Exposes methods and properties that enable Microsoft UI Automation clients to retrieve UI information from Microsoft Active Accessibility (MSAA) servers.

## Inheritance

The **IUIAutomationLegacyIAccessiblePattern** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IUIAutomationLegacyIAccessiblePattern** also has these types of members:

## Methods

The **IUIAutomationLegacyIAccessiblePattern** interface has these methods.

|  |
| --- |
| [IUIAutomationLegacyIAccessiblePattern::DoDefaultAction](nf-uiautomationclient-iuiautomationlegacyiaccessiblepattern-dodefaultaction)   Performs the Microsoft Active Accessibility default action for the element. (IUIAutomationLegacyIAccessiblePattern.DoDefaultAction) |
| [IUIAutomationLegacyIAccessiblePattern::get\_CachedChildId](nf-uiautomationclient-iuiautomationlegacyiaccessiblepattern-get_cachedchildid)   Retrieves the cached Microsoft Active Accessibility child identifier for the element. |
| [IUIAutomationLegacyIAccessiblePattern::get\_CachedDefaultAction](nf-uiautomationclient-iuiautomationlegacyiaccessiblepattern-get_cacheddefaultaction)   Retrieves the Microsoft Active Accessibility cached default action for the element. |
| [IUIAutomationLegacyIAccessiblePattern::get\_CachedDescription](nf-uiautomationclient-iuiautomationlegacyiaccessiblepattern-get_cacheddescription)   Retrieves the cached Microsoft Active Accessibility description of the element. |
| [IUIAutomationLegacyIAccessiblePattern::get\_CachedHelp](nf-uiautomationclient-iuiautomationlegacyiaccessiblepattern-get_cachedhelp)   Retrieves the cached Microsoft Active Accessibility help string for the element. |
| [IUIAutomationLegacyIAccessiblePattern::get\_CachedKeyboardShortcut](nf-uiautomationclient-iuiautomationlegacyiaccessiblepattern-get_cachedkeyboardshortcut)   Retrieves the cached Microsoft Active Accessibility keyboard shortcut property for the element. |
| [IUIAutomationLegacyIAccessiblePattern::get\_CachedName](nf-uiautomationclient-iuiautomationlegacyiaccessiblepattern-get_cachedname)   Retrieves the cached Microsoft Active Accessibility name property of the element. |
| [IUIAutomationLegacyIAccessiblePattern::get\_CachedRole](nf-uiautomationclient-iuiautomationlegacyiaccessiblepattern-get_cachedrole)   Retrieves the cached Microsoft Active Accessibility role of the element. |
| [IUIAutomationLegacyIAccessiblePattern::get\_CachedState](nf-uiautomationclient-iuiautomationlegacyiaccessiblepattern-get_cachedstate)   Retrieves the cached Microsoft Active Accessibility state identifier for the element. |
| [IUIAutomationLegacyIAccessiblePattern::get\_CachedValue](nf-uiautomationclient-iuiautomationlegacyiaccessiblepattern-get_cachedvalue)   Retrieves the cached Microsoft Active Accessibility value property. |
| [IUIAutomationLegacyIAccessiblePattern::get\_CurrentChildId](nf-uiautomationclient-iuiautomationlegacyiaccessiblepattern-get_currentchildid)   Retrieves the Microsoft Active Accessibility child identifier for the element. |
| [IUIAutomationLegacyIAccessiblePattern::get\_CurrentDefaultAction](nf-uiautomationclient-iuiautomationlegacyiaccessiblepattern-get_currentdefaultaction)   Retrieves the Microsoft Active Accessibility current default action for the element. |
| [IUIAutomationLegacyIAccessiblePattern::get\_CurrentDescription](nf-uiautomationclient-iuiautomationlegacyiaccessiblepattern-get_currentdescription)   Retrieves the Microsoft Active Accessibility description of the element. |
| [IUIAutomationLegacyIAccessiblePattern::get\_CurrentHelp](nf-uiautomationclient-iuiautomationlegacyiaccessiblepattern-get_currenthelp)   Retrieves the Microsoft Active Accessibility help string for the element. |
| [IUIAutomationLegacyIAccessiblePattern::get\_CurrentKeyboardShortcut](nf-uiautomationclient-iuiautomationlegacyiaccessiblepattern-get_currentkeyboardshortcut)   Retrieves the Microsoft Active Accessibility keyboard shortcut property for the element. |
| [IUIAutomationLegacyIAccessiblePattern::get\_CurrentName](nf-uiautomationclient-iuiautomationlegacyiaccessiblepattern-get_currentname)   Retrieves the Microsoft Active Accessibility name property of the element. |
| [IUIAutomationLegacyIAccessiblePattern::get\_CurrentRole](nf-uiautomationclient-iuiautomationlegacyiaccessiblepattern-get_currentrole)   Retrieves the Microsoft Active Accessibility role identifier of the element. |
| [IUIAutomationLegacyIAccessiblePattern::get\_CurrentState](nf-uiautomationclient-iuiautomationlegacyiaccessiblepattern-get_currentstate)   Retrieves the Microsoft Active Accessibility state identifier for the element. |
| [IUIAutomationLegacyIAccessiblePattern::get\_CurrentValue](nf-uiautomationclient-iuiautomationlegacyiaccessiblepattern-get_currentvalue)   Retrieves the Microsoft Active Accessibility value property. |
| [IUIAutomationLegacyIAccessiblePattern::GetCachedSelection](nf-uiautomationclient-iuiautomationlegacyiaccessiblepattern-getcachedselection)   Retrieves the cached Microsoft Active Accessibility property that identifies the selected children of this element. |
| [IUIAutomationLegacyIAccessiblePattern::GetCurrentSelection](nf-uiautomationclient-iuiautomationlegacyiaccessiblepattern-getcurrentselection)   Retrieves the Microsoft Active Accessibility property that identifies the selected children of this element. |
| [IUIAutomationLegacyIAccessiblePattern::GetIAccessible](nf-uiautomationclient-iuiautomationlegacyiaccessiblepattern-getiaccessible)   Retrieves an IAccessible object that corresponds to the Microsoft UI Automation element. |
| [IUIAutomationLegacyIAccessiblePattern::Select](nf-uiautomationclient-iuiautomationlegacyiaccessiblepattern-select)   Performs a Microsoft Active Accessibility selection. (IUIAutomationLegacyIAccessiblePattern.Select) |
| [IUIAutomationLegacyIAccessiblePattern::SetValue](nf-uiautomationclient-iuiautomationlegacyiaccessiblepattern-setvalue)   Sets the Microsoft Active Accessibility value property for the element. |

## Remarks

This interface is obtained just like any other control pattern. It enables UI Automation clients to gather MSAA properties more efficiently, taking advantage of the caching system, and also enables UI Automation clients to interact with native Microsoft Active Accessibility servers that support the **IAccessible** interface.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[Control Pattern Interfaces for Clients](/en-us/windows/desktop/WinAuto/uiauto-client-controlpatterninterfaces)

---
