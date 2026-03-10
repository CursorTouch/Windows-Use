# MSAAMENUINFO

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/ns-oleacc-msaamenuinfo)

# MSAAMENUINFO structure (oleacc.h)

Used by server developers to expose the names of owner-drawn menu items.

## Syntax

```
typedef struct tagMSAAMENUINFO {
  DWORD  dwMSAASignature;
  DWORD  cchWText;
  LPWSTR pszWText;
} MSAAMENUINFO, *LPMSAAMENUINFO;
```

## Members

`dwMSAASignature`

Type: **[DWORD](/en-us/windows/desktop/WinProg/windows-data-types)**

Must be MSAA\_MENU\_SIG, which is defined in oleacc.h.

`cchWText`

Type: **[DWORD](/en-us/windows/desktop/WinProg/windows-data-types)**

Length, in characters, of the text for the menu item, **not including** the Unicode null-terminated character.

`pszWText`

Type: **[LPWSTR](/en-us/windows/desktop/WinProg/windows-data-types)**

The text of the menu item, in Unicode, **including** the Unicode null-terminated character.

## Remarks

By associating the **MSAAMENUINFO** structure with owner-drawn menu item data, server developers can expose the menu items without having to implement [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible).

The **MSAAMENUINFO** structure is the first member of the application-specific structure (or class) that contains the data for an owner-drawn menu item, which is pointed to by the **dwItemData** member of the [MENUITEMINFO](/en-us/windows/desktop/api/winuser/ns-winuser-menuiteminfoa) structure.

The **MSAAMENUINFO** structure cannot be a member in a class that contains virtual functions because the first member of the class is always a compiler-generated pointer to a table of the virtual functions. To work around this problem, you can implement a structure that contains the **MSAAMENUINFO** as the first member, and a pointer to the class with the virtual functions as a second member, which contains the owner-drawn item data.

#### Examples

The following code fragment shows the declaration of an application-specific owner-drawn menu information structure that includes **MSAAMENUINFO**:

```
// Application-specific owner-drawn menu info struct. Owner-drawn data 
// is a pointer to one of these. MSAAMENUINFO must be the first 
// member. 
struct MenuEntry
{
    MSAAMENUINFO m_MSAA;       // MSAA info - must be first element.
    LPTSTR       m_pName;      // Menu text, for display. NULL for
                               //  separator item.
    int          m_CmdID;      // Menu command ID.
    int          m_IconIndex;  // Index of icon in bitmap.
};
```

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 2000 Professional [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Header** | oleacc.h |
| **Redistributable** | Active Accessibility 1.3 RDK on Windows NT 4.0 with SP6 and later and Windows 95 |

## See also

[Exposing Owner-Drawn Menu Items](/en-us/windows/desktop/WinAuto/exposing-owner-drawn-menu-items)

[IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible)

---
