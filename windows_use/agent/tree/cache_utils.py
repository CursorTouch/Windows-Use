"""
UIA Caching Utilities for Performance Optimization

This module provides utilities for implementing UI Automation caching
to reduce cross-process COM calls during tree traversal.
"""

from windows_use.uia import CacheRequest, PropertyId, PatternId, TreeScope, Control
from typing import Optional, Any
import logging

logger = logging.getLogger(__name__)


class CacheRequestFactory:
    """Factory for creating optimized cache requests for different scenarios."""
    
    @staticmethod
    def create_tree_traversal_cache() -> CacheRequest:
        """
        Creates a cache request optimized for tree traversal.
        Caches all commonly accessed properties and patterns.
        
        This cache request is designed to minimize COM calls during
        the tree_traversal() operation in tree/service.py.
        
        Returns:
            CacheRequest configured for tree traversal
        """
        cache_request = CacheRequest()
        
        # Set scope to cache element and its children
        # This allows us to get children with pre-cached properties
        cache_request.TreeScope = TreeScope.TreeScope_Element | TreeScope.TreeScope_Children
        
        # Basic identification properties
        cache_request.AddProperty(PropertyId.NameProperty)
        cache_request.AddProperty(PropertyId.AutomationIdProperty)
        cache_request.AddProperty(PropertyId.LocalizedControlTypeProperty)
        cache_request.AddProperty(PropertyId.AcceleratorKeyProperty)
        cache_request.AddProperty(PropertyId.ClassNameProperty)
        cache_request.AddProperty(PropertyId.ControlTypeProperty)
        
        # State properties for visibility and interaction checks
        cache_request.AddProperty(PropertyId.IsEnabledProperty)
        cache_request.AddProperty(PropertyId.IsOffscreenProperty)
        cache_request.AddProperty(PropertyId.IsControlElementProperty)
        cache_request.AddProperty(PropertyId.HasKeyboardFocusProperty)
        cache_request.AddProperty(PropertyId.IsKeyboardFocusableProperty)
        
        # Layout properties
        cache_request.AddProperty(PropertyId.BoundingRectangleProperty)
        
        # REMOVED: Expensive patterns and less critical properties to improve performance
        # Patterns like LegacyIAccessible are very expensive to marshal for every element.
        # We will fetch them live only for the few elements that actually need them.
        
        return cache_request
    
    @staticmethod
    def create_visibility_check_cache() -> CacheRequest:
        """
        Creates a lightweight cache request for quick visibility checks.
        
        This is optimized for the is_element_visible() method.
        
        Returns:
            CacheRequest configured for visibility checks
        """
        cache_request = CacheRequest()
        cache_request.TreeScope = TreeScope.TreeScope_Element
        
        # Only cache properties needed for visibility checks
        cache_request.AddProperty(PropertyId.IsControlElementProperty)
        cache_request.AddProperty(PropertyId.BoundingRectangleProperty)
        cache_request.AddProperty(PropertyId.IsOffscreenProperty)
        cache_request.AddProperty(PropertyId.ControlTypeProperty)
        
        return cache_request
    
    @staticmethod
    def create_interaction_check_cache() -> CacheRequest:
        """
        Creates a cache request for interaction checks.
        
        This is optimized for the is_element_interactive() method.
        
        Returns:
            CacheRequest configured for interaction checks
        """
        cache_request = CacheRequest()
        cache_request.TreeScope = TreeScope.TreeScope_Element
        
        # Properties needed for interaction checks
        cache_request.AddProperty(PropertyId.ControlTypeProperty)
        cache_request.AddProperty(PropertyId.IsEnabledProperty)
        cache_request.AddProperty(PropertyId.IsKeyboardFocusableProperty)
        cache_request.AddProperty(PropertyId.IsOffscreenProperty)
        cache_request.AddProperty(PropertyId.BoundingRectangleProperty)
        cache_request.AddProperty(PropertyId.IsControlElementProperty)
        
        # Pattern for role and action checks
        cache_request.AddPattern(PatternId.LegacyIAccessiblePattern)
        
        return cache_request
    
    @staticmethod
    def create_scroll_check_cache() -> CacheRequest:
        """
        Creates a cache request for scrollability checks.
        
        This is optimized for the is_element_scrollable() method.
        
        Returns:
            CacheRequest configured for scroll checks
        """
        cache_request = CacheRequest()
        cache_request.TreeScope = TreeScope.TreeScope_Element
        
        cache_request.AddProperty(PropertyId.ControlTypeProperty)
        cache_request.AddProperty(PropertyId.IsOffscreenProperty)
        
        # Scroll pattern for scrollability checks
        cache_request.AddPattern(PatternId.ScrollPattern)
        
        return cache_request


class CachedPropertyAccessor:
    """
    Helper class to safely access properties with automatic fallback.
    
    This class provides a unified interface for accessing both cached
    and non-cached properties, with automatic fallback to live property
    access if cached access fails.
    """
    
    @staticmethod
    def get_property(node: Control, property_name: str, use_cache: bool = True) -> Any:
        """
        Get a property value, using cache if available.
        """
        if use_cache and hasattr(node, '_is_cached') and node._is_cached:
            cached_attr = f'Cached{property_name}'
            
            # 1. Try Control wrapper property first
            # Note: Do NOT use hasattr(node, cached_attr) as it triggers the property access
            # and bubbles up COMError if the property is not in the cache.
            try:
                return getattr(node, cached_attr)
            except Exception:
                pass
            
            # 2. Try underlying Element property directly
            # This handles properties that are missing from the Control wrapper
            try:
                return getattr(node.Element, cached_attr)
            except Exception:
                logger.debug(f"Failed to access cached property {property_name} on Element")
        
        # Fallback to regular property access (Live)
        try:
            val = getattr(node, property_name)
        except Exception as e:
            logger.warning(f"Failed to access property {property_name}: {e}")
            raise
    
    # Convenience methods for commonly accessed properties
    
    @staticmethod
    def get_name(node: Control, use_cache: bool = True) -> str:
        """Get the Name property."""
        return CachedPropertyAccessor.get_property(node, 'Name', use_cache)
    
    @staticmethod
    def get_class_name(node: Control, use_cache: bool = True) -> str:
        """Get the ClassName property."""
        if use_cache and hasattr(node, '_is_cached') and node._is_cached:
            try:
                val = node.Element.CachedClassName
                return val
            except: pass
        
        val = node.ClassName
        return val
    
    @staticmethod
    def get_automation_id(node: Control, use_cache: bool = True) -> str:
        """Get the AutomationId property."""
        # Wrapper might handle this one, but safe to default
        return CachedPropertyAccessor.get_property(node, 'AutomationId', use_cache)
    
    @staticmethod
    def get_control_type_name(node: Control, use_cache: bool = True) -> str:
        """Get the ControlTypeName property."""
        # Special case: need to convert int to string
        if use_cache and hasattr(node, '_is_cached') and node._is_cached:
            try:
                control_type = node.Element.CachedControlType
                from windows_use.uia import ControlTypeNames
                val = ControlTypeNames.get(control_type, "Unknown")
                return val
            except: pass
            
        val = node.ControlTypeName
        return val
    
    @staticmethod
    def get_localized_control_type(node: Control, use_cache: bool = True) -> str:
        """Get the LocalizedControlType property."""
        return CachedPropertyAccessor.get_property(node, 'LocalizedControlType', use_cache)
    
    @staticmethod
    def get_is_enabled(node: Control, use_cache: bool = True) -> bool:
        """Get the IsEnabled property."""
        if use_cache and hasattr(node, '_is_cached') and node._is_cached:
            try:
                val = bool(node.Element.CachedIsEnabled)
                return val
            except: pass
            
        val = node.IsEnabled
        return val
    
    @staticmethod
    def get_is_offscreen(node: Control, use_cache: bool = True) -> bool:
        """Get the IsOffscreen property."""
        if use_cache and hasattr(node, '_is_cached') and node._is_cached:
            try:
                val = bool(node.Element.CachedIsOffscreen)
                return val
            except: pass
            
        val = node.IsOffscreen
        return val
    
    @staticmethod
    def get_is_control_element(node: Control, use_cache: bool = True) -> bool:
        """Get the IsControlElement property."""
        if use_cache and hasattr(node, '_is_cached') and node._is_cached:
            try:
                val = bool(node.Element.CachedIsControlElement)
                return val
            except: pass
            
        val = node.IsControlElement
        return val
    
    @staticmethod
    def get_has_keyboard_focus(node: Control, use_cache: bool = True) -> bool:
        """Get the HasKeyboardFocus property."""
        if use_cache and hasattr(node, '_is_cached') and node._is_cached:
            try:
                val = bool(node.Element.CachedHasKeyboardFocus)
                return val
            except: pass
            
        val = node.HasKeyboardFocus
        return val
    
    @staticmethod
    def get_is_keyboard_focusable(node: Control, use_cache: bool = True) -> bool:
        """Get the IsKeyboardFocusable property."""
        if use_cache and hasattr(node, '_is_cached') and node._is_cached:
            try:
                val = bool(node.Element.CachedIsKeyboardFocusable)
                return val
            except: pass
            
        val = node.IsKeyboardFocusable
        return val
    
    @staticmethod
    def get_bounding_rectangle(node: Control, use_cache: bool = True):
        """Get the BoundingRectangle property."""
        if use_cache and hasattr(node, '_is_cached') and node._is_cached:
            try:
                # Raw COM RECT needs wrapping
                rect = node.Element.CachedBoundingRectangle
                val = Rect(rect.left, rect.top, rect.right, rect.bottom)
                return val
            except Exception as e: 
                # logger.debug(f"Failed CachedBoundingRectangle: {e}")
                pass
            
        val = node.BoundingRectangle
        return val
    
    @staticmethod
    def get_accelerator_key(node: Control, use_cache: bool = True) -> str:
        """Get the AcceleratorKey property."""
        if use_cache and hasattr(node, '_is_cached') and node._is_cached:
             try:
                val = node.Element.CachedAcceleratorKey
                return val
             except: pass
             
        val = node.AcceleratorKey
        return val


class CachedControlHelper:
    """Helper class for working with cached controls."""
    
    @staticmethod
    def build_cached_control(node: Control, cache_request: Optional[CacheRequest] = None) -> Control:
        """
        Build a cached version of a control.
        
        Args:
            node: The control to cache
            cache_request: Optional custom cache request. If None, uses tree traversal cache.
        
        Returns:
            A control with cached properties, or the original control if caching fails
        """
        if cache_request is None:
            cache_request = CacheRequestFactory.create_tree_traversal_cache()
        
        try:
            cached_node = node.BuildUpdatedCache(cache_request)
            cached_node._is_cached = True
            return cached_node
        except Exception as e:
            logger.debug(f"Failed to build cached control: {e}")
            return node
    
    @staticmethod
    def get_cached_children(node: Control, cache_request: Optional[CacheRequest] = None) -> list[Control]:
        """
        Get children with pre-cached properties.
        
        This is the most significant optimization - it retrieves all children
        with their properties already cached, eliminating the need for individual
        property access calls on each child.
        
        Args:
            node: The parent control
            cache_request: Optional custom cache request. If None, uses tree traversal cache.
        
        Returns:
            List of children with cached properties
        """
        if cache_request is None:
            cache_request = CacheRequestFactory.create_tree_traversal_cache()
        
        # Ensure the cache request includes children
        # Note: We do NOT set this here to avoid modifying shared cache request objects
        # The caller is responsible for providing a CacheRequest with TreeScope_Children
        if (cache_request.TreeScope & TreeScope.TreeScope_Children) == 0:
             logger.warning("Cache request passed to get_cached_children does not have Children scope!")
        
        try:
            # Build updated cache that includes children
            cached_node = node.BuildUpdatedCache(cache_request)
            
            # Get children - use GetCachedChildren to avoid walking the tree with ViewWalker
            children = cached_node.GetCachedChildren()
            
            # Mark children as cached
            for child in children:
                child._is_cached = True
            
            logger.debug(f"Retrieved {len(children)} cached children")
            return children
        except Exception as e:
            logger.debug(f"Failed to get cached children, falling back to regular access: {e}")
            return node.GetChildren()
    
    @staticmethod
    def invalidate_cache(node: Control) -> None:
        """
        Invalidate the cache marker on a control.
        
        This forces subsequent property accesses to use live data.
        
        Args:
            node: The control to invalidate
        """
        if hasattr(node, '_is_cached'):
            delattr(node, '_is_cached')



