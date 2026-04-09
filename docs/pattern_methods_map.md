# UIA Pattern Methods Map

This document maps each pattern wrapper in `windows_use/uia/patterns.py` to the public properties and methods exposed by that wrapper.

Notes:
- Properties are listed under `Properties`.
- Callable actions are listed under `Methods`.
- `ObjectModelPattern` is present as a wrapper class, but it currently has no public members.
- UIA pattern IDs that exist in `windows_use/uia/enums.py` but do not have a wrapper class here are not listed.

## AnnotationPattern

Properties:
- `AnnotationTypeId`
- `AnnotationTypeName`
- `Author`
- `DateTime`
- `Target`

Methods:
- None

## CustomNavigationPattern

Properties:
- None

Methods:
- `Navigate`

## DockPattern

Properties:
- `DockPosition`

Methods:
- `SetDockPosition`

## DragPattern

Properties:
- `DropEffect`
- `DropEffects`
- `IsGrabbed`

Methods:
- `GetGrabbedItems`

## DropTargetPattern

Properties:
- `DropTargetEffect`
- `DropTargetEffects`

Methods:
- None

## ExpandCollapsePattern

Properties:
- `ExpandCollapseState`

Methods:
- `Collapse`
- `Expand`

## GridItemPattern

Properties:
- `Column`
- `ColumnSpan`
- `ContainingGrid`
- `Row`
- `RowSpan`

Methods:
- None

## GridPattern

Properties:
- `ColumnCount`
- `RowCount`

Methods:
- `GetItem`

## InvokePattern

Properties:
- None

Methods:
- `Invoke`

## ItemContainerPattern

Properties:
- None

Methods:
- `FindItemByProperty`

## LegacyIAccessiblePattern

Properties:
- `ChildId`
- `DefaultAction`
- `Description`
- `Help`
- `KeyboardShortcut`
- `Name`
- `Role`
- `State`
- `Value`

Methods:
- `DoDefaultAction`
- `GetSelection`
- `GetIAccessible`
- `Select`
- `SetValue`

## MultipleViewPattern

Properties:
- `CurrentView`

Methods:
- `GetSupportedViews`
- `GetViewName`
- `SetView`

## ObjectModelPattern

Properties:
- None

Methods:
- None

## RangeValuePattern

Properties:
- `IsReadOnly`
- `LargeChange`
- `Maximum`
- `Minimum`
- `SmallChange`
- `Value`

Methods:
- `SetValue`

## ScrollItemPattern

Properties:
- None

Methods:
- `ScrollIntoView`

## ScrollPattern

Properties:
- `HorizontallyScrollable`
- `HorizontalScrollPercent`
- `HorizontalViewSize`
- `VerticallyScrollable`
- `VerticalScrollPercent`
- `VerticalViewSize`

Methods:
- `Scroll`
- `SetScrollPercent`

## SelectionItemPattern

Properties:
- `IsSelected`
- `SelectionContainer`

Methods:
- `AddToSelection`
- `RemoveFromSelection`
- `Select`

## SelectionPattern

Properties:
- `CanSelectMultiple`
- `IsSelectionRequired`

Methods:
- `GetSelection`

## SpreadsheetItemPattern

Properties:
- `Formula`

Methods:
- `GetAnnotationObjects`
- `GetAnnotationTypes`

## SpreadsheetPattern

Properties:
- None

Methods:
- `GetItemByName`

## StylesPattern

Properties:
- `ExtendedProperties`
- `FillColor`
- `FillPatternColor`
- `Shape`
- `StyleId`
- `StyleName`

Methods:
- None

## SynchronizedInputPattern

Properties:
- None

Methods:
- `Cancel`
- `StartListening`

## TableItemPattern

Properties:
- None

Methods:
- `GetColumnHeaderItems`
- `GetRowHeaderItems`

## TablePattern

Properties:
- `RowOrColumnMajor`

Methods:
- `GetColumnHeaders`
- `GetRowHeaders`

## TextChildPattern

Properties:
- `TextContainer`
- `TextRange`

Methods:
- None

## TextEditPattern

Properties:
- None

Methods:
- `GetActiveComposition`
- `GetConversionTarget`

## TextPattern

Properties:
- `DocumentRange`
- `SupportedTextSelection`

Methods:
- `GetSelection`
- `GetVisibleRanges`
- `RangeFromChild`
- `RangeFromPoint`

## TogglePattern

Properties:
- `ToggleState`

Methods:
- `Toggle`
- `SetToggleState`

## TransformPattern

Properties:
- `CanMove`
- `CanResize`
- `CanRotate`

Methods:
- `Move`
- `Resize`
- `Rotate`

## ValuePattern

Properties:
- `IsReadOnly`
- `Value`

Methods:
- `SetValue`

## VirtualizedItemPattern

Properties:
- None

Methods:
- `Realize`

## WindowPattern

Properties:
- `CanMaximize`
- `CanMinimize`
- `IsModal`
- `IsTopmost`
- `WindowInteractionState`
- `WindowVisualState`

Methods:
- `Close`
- `SetWindowVisualState`
- `WaitForInputIdle`
