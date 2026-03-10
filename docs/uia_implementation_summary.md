# UI Automation Cache and Find Methods Implementation

## Summary

Successfully implemented the following UI Automation methods in `windows_use/uia/controls.py`:

### Find Methods

1. **`FindAll(scope, condition)`**
   - Finds all UI Automation elements that satisfy the specified condition
   - Returns a list of Control objects
   - Uses TreeScope to define search scope (Children, Descendants, Subtree, etc.)

2. **`FindAllBuildCache(scope, condition, cacheRequest)`**
   - Same as FindAll but caches properties and patterns for better performance
   - Reduces COM calls by pre-fetching data

3. **`FindFirst(scope, condition)`**
   - Finds the first UI Automation element that satisfies the condition
   - Returns a single Control object or None
   - More efficient than FindAll when you only need one element

4. **`FindFirstBuildCache(scope, condition, cacheRequest)`**
   - Same as FindFirst but with caching support

### Cache Methods

5. **`GetCachedChildren()`**
   - Retrieves cached child elements
   - Only works if children were cached in the cache request
   - Returns a list of Control objects

6. **`GetCachedParent()`**
   - Retrieves the cached parent element
   - Returns a Control object or None

7. **`GetCachedPattern(patternId)`**
   - Retrieves a cached pattern interface
   - Returns a pattern object or None

8. **`GetCachedPatternAs(patternId, riid)`**
   - Retrieves a cached pattern with a specific interface ID
   - Advanced usage for specific COM interfaces

9. **`GetCachedPropertyValue(propertyId)`**
   - Retrieves a cached property value
   - Returns the property value or None

10. **`GetCachedPropertyValueEx(propertyId, ignoreDefaultValue)`**
    - Retrieves a cached property value with option to ignore defaults
    - More control over default value handling

## Helper Functions Added to `core.py`

To support the find methods, the following condition creation functions were added:

- **`CreateTrueCondition()`** - Matches all elements
- **`CreateFalseCondition()`** - Matches no elements
- **`CreatePropertyCondition(propertyId, value)`** - Matches elements with specific property values
- **`CreateAndCondition(condition1, condition2)`** - Logical AND of two conditions
- **`CreateOrCondition(condition1, condition2)`** - Logical OR of two conditions
- **`CreateNotCondition(condition)`** - Logical NOT of a condition

## Usage Examples

### Basic FindAll Example

```python
from windows_use.uia import core
from windows_use.uia.controls import Control
from windows_use.uia.enums import TreeScope, PropertyId, ControlType

# Get root element
root = Control()

# Create condition to find buttons
condition = core.CreatePropertyCondition(PropertyId.ControlTypeProperty, ControlType.ButtonControl)

# Find all buttons
buttons = root.FindAll(TreeScope.TreeScope_Descendants, condition)
print(f"Found {len(buttons)} buttons")
```

### Using Cache for Performance

```python
# Create cache request
cache_request = core.CreateCacheRequest()
cache_request.TreeScope = TreeScope.TreeScope_Element
cache_request.AddProperty(PropertyId.NameProperty)
cache_request.AddProperty(PropertyId.ClassNameProperty)

# Find with cache
condition = core.CreatePropertyCondition(PropertyId.ControlTypeProperty, ControlType.WindowControl)
windows = root.FindAllBuildCache(TreeScope.TreeScope_Children, condition, cache_request)

# Access cached properties (faster, no additional COM calls)
for window in windows:
    print(window.CachedName, window.CachedClassName)
```

### Complex Conditions

```python
# Find enabled buttons only
button_cond = core.CreatePropertyCondition(PropertyId.ControlTypeProperty, ControlType.ButtonControl)
enabled_cond = core.CreatePropertyCondition(PropertyId.IsEnabledProperty, True)
combined = core.CreateAndCondition(button_cond, enabled_cond)

enabled_buttons = root.FindAll(TreeScope.TreeScope_Descendants, combined)
```

## Benefits

1. **Performance**: Cache methods reduce COM calls significantly
2. **Flexibility**: Condition system allows complex element searches
3. **Compatibility**: Follows Microsoft UI Automation API conventions
4. **Type Safety**: Proper type hints for better IDE support

## Testing

A comprehensive example script has been created at:
`examples/uia_findall_example.py`

This demonstrates:
- Finding elements with various conditions
- Using cache requests
- Complex condition combinations
- Accessing cached properties

## Documentation References

All methods include links to the official Microsoft documentation:
- https://docs.microsoft.com/en-us/windows/win32/api/uiautomationclient/

## Notes

- All methods include proper error handling with try/except blocks
- COM errors are caught and handled gracefully
- Methods return empty lists or None instead of raising exceptions
- Type hints are provided for better code completion
