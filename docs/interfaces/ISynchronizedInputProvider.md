# ISynchronizedInputProvider

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-isynchronizedinputprovider)

# ISynchronizedInputProvider interface (uiautomationcore.h)

Enables Microsoft UI Automation client applications to direct the mouse or keyboard input to a specific UI element.

## Inheritance

The **ISynchronizedInputProvider** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **ISynchronizedInputProvider** also has these types of members:

## Methods

The **ISynchronizedInputProvider** interface has these methods.

|  |
| --- |
| [ISynchronizedInputProvider::Cancel](nf-uiautomationcore-isynchronizedinputprovider-cancel)   Cancels listening for input. |
| [ISynchronizedInputProvider::StartListening](nf-uiautomationcore-isynchronizedinputprovider-startlistening)   Starts listening for input of the specified type. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

---
