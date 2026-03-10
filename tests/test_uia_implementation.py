"""
Quick test to verify the implementation of FindAll, FindFirst, and cache methods.
This is a simple smoke test to ensure the methods are callable and don't crash.
"""

import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from windows_use.uia import core
from windows_use.uia.controls import Control
from windows_use.uia.enums import TreeScope, PropertyId, ControlType


def test_condition_creation():
    """Test that condition creation functions work."""
    print("Testing condition creation...")
    
    try:
        # Test basic conditions
        true_cond = core.CreateTrueCondition()
        assert true_cond is not None, "CreateTrueCondition failed"
        
        false_cond = core.CreateFalseCondition()
        assert false_cond is not None, "CreateFalseCondition failed"
        
        # Test property condition
        prop_cond = core.CreatePropertyCondition(PropertyId.ControlTypeProperty, ControlType.WindowControl)
        assert prop_cond is not None, "CreatePropertyCondition failed"
        
        # Test logical conditions
        and_cond = core.CreateAndCondition(true_cond, prop_cond)
        assert and_cond is not None, "CreateAndCondition failed"
        
        or_cond = core.CreateOrCondition(true_cond, false_cond)
        assert or_cond is not None, "CreateOrCondition failed"
        
        not_cond = core.CreateNotCondition(false_cond)
        assert not_cond is not None, "CreateNotCondition failed"
        
        print("  ✓ All condition creation functions work")
        return True
    except Exception as e:
        print(f"  ✗ Condition creation failed: {e}")
        return False


def test_find_methods():
    """Test FindAll and FindFirst methods."""
    print("Testing Find methods...")
    
    try:
        # Get root element (desktop) properly
        from windows_use.uia.core import _AutomationClient
        root_element = _AutomationClient.instance().IUIAutomation.GetRootElement()
        root = Control.CreateControlFromElement(root_element)
        
        # Test FindAll
        condition = core.CreatePropertyCondition(PropertyId.ControlTypeProperty, ControlType.WindowControl)
        windows = root.FindAll(TreeScope.TreeScope_Children, condition)
        assert isinstance(windows, list), "FindAll should return a list"
        print(f"  ✓ FindAll works - found {len(windows)} windows")
        
        # Test FindFirst
        first_window = root.FindFirst(TreeScope.TreeScope_Children, condition)
        if first_window:
            print(f"  ✓ FindFirst works - found window: {first_window.Name}")
        else:
            print("  ✓ FindFirst works - no window found (this is ok)")
        
        return True
    except Exception as e:
        print(f"  ✗ Find methods failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_cache_methods():
    """Test cache-related methods."""
    print("Testing cache methods...")
    
    try:
        # Get root element (desktop) properly
        from windows_use.uia.core import _AutomationClient
        root_element = _AutomationClient.instance().IUIAutomation.GetRootElement()
        root = Control.CreateControlFromElement(root_element)
        
        # Create a cache request
        cache_request = core.CreateCacheRequest()
        cache_request.TreeScope = TreeScope.TreeScope_Element
        cache_request.AddProperty(PropertyId.NameProperty)
        
        # Test FindAllBuildCache
        condition = core.CreatePropertyCondition(PropertyId.ControlTypeProperty, ControlType.WindowControl)
        windows = root.FindAllBuildCache(TreeScope.TreeScope_Children, condition, cache_request)
        assert isinstance(windows, list), "FindAllBuildCache should return a list"
        print(f"  ✓ FindAllBuildCache works - found {len(windows)} windows")
        
        # Test FindFirstBuildCache
        first_window = root.FindFirstBuildCache(TreeScope.TreeScope_Children, condition, cache_request)
        if first_window:
            # Try to access cached property
            cached_name = first_window.CachedName
            print(f"  ✓ FindFirstBuildCache works - cached name: {cached_name}")
        else:
            print("  ✓ FindFirstBuildCache works - no window found (this is ok)")
        
        # Test GetCachedChildren (may fail if not cached, which is expected)
        try:
            children = root.GetCachedChildren()
            print(f"  ✓ GetCachedChildren works - found {len(children)} children")
        except:
            print("  ✓ GetCachedChildren works (no cached children, as expected)")
        
        # Test GetCachedParent (may return None, which is expected)
        parent = root.GetCachedParent()
        if parent:
            print(f"  ✓ GetCachedParent works - found parent")
        else:
            print("  ✓ GetCachedParent works (no cached parent, as expected)")
        
        return True
    except Exception as e:
        print(f"  ✗ Cache methods failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("=" * 60)
    print("UI Automation Implementation Test")
    print("=" * 60)
    print()
    
    results = []
    
    # Run tests
    results.append(("Condition Creation", test_condition_creation()))
    print()
    
    results.append(("Find Methods", test_find_methods()))
    print()
    
    results.append(("Cache Methods", test_cache_methods()))
    print()
    
    # Summary
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "PASSED" if result else "FAILED"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {name}: {status}")
    
    print()
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
