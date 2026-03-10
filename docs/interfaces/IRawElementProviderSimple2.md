# IRawElementProviderSimple2

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-irawelementprovidersimple2)

# IRawElementProviderSimple2 interface (uiautomationcore.h)

Extends the [IRawElementProviderSimple](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementprovidersimple) interface to enable programmatically invoking context menus.

## Inheritance

The **IRawElementProviderSimple2** interface inherits from [IRawElementProviderSimple](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementprovidersimple). **IRawElementProviderSimple2** also has these types of members:

## Methods

The **IRawElementProviderSimple2** interface has these methods.

|  |
| --- |
| [IRawElementProviderSimple2::ShowContextMenu](nf-uiautomationcore-irawelementprovidersimple2-showcontextmenu)   Programmatically invokes a context menu on the target element. (IRawElementProviderSimple2.ShowContextMenu) |

## Remarks

This interface can be implemented on:

* Providers that add or override properties or control patterns on a UI element that already has a provider.

If no context menu is available directly on the element on which [ShowContextMenu](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-irawelementprovidersimple2-showcontextmenu) was invoked, the provider should attempt to invoke a context menu on the UI Automation parent of the current item.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8.1 [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2012 R2 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

---
