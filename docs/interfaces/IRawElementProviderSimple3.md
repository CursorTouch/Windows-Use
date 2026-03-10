# IRawElementProviderSimple3

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-irawelementprovidersimple3)

# IRawElementProviderSimple3 interface (uiautomationcore.h)

Extends the [IRawElementProviderSimple2](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementprovidersimple2) interface to enable retrieving metadata about how accessible technology should say the preferred content type.

## Inheritance

The **IRawElementProviderSimple3** interface inherits from [IRawElementProviderSimple2](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementprovidersimple2). **IRawElementProviderSimple3** also has these types of members:

## Methods

The **IRawElementProviderSimple3** interface has these methods.

|  |
| --- |
| [IRawElementProviderSimple3::GetMetadataValue](nf-uiautomationcore-irawelementprovidersimple3-getmetadatavalue)   Gets metadata from the UI Automation element that indicates how the information should be interpreted. (IRawElementProviderSimple3.GetMetadataValue) |

## Remarks

Screen reading accessibility tools like Narrator use a speech synthesizer to read what an app is showing. Speech synthesizers usually read the provided content well based on the content description.

However, the speech synthesizer could use some help describing the preferred content type. The SayAs command provides accurate content reading from a Microsoft UI Automation provider to a UI Automation client (such as a screen reader) through UI Automation core APIs.

Examples:

* Given the date 10/4, is the format Month/Day or Day/Month?
  If a screen reader does not know, you could hear October 4th or 10th April.
* Given the string "10-100", is this
  "Ten to one hundred" or
  "Ten minus 100"?

  The ability to mark the "10" as a number and the "-100" as a number helps active technology (AT) read it better.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 10, version 1703 [desktop apps only] |
| **Minimum supported server** | Windows Server 2016 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[IRawElementProviderSimple2](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementprovidersimple2)

---
