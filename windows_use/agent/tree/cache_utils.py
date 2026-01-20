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
        
        # Try to use existing cache first if available
        try:
            # Build updated cache that includes children
            cached_node = node.BuildUpdatedCache(cache_request)
            children = cached_node.GetCachedChildren()
            
            for child in children:
                child._is_cached = True
            
            logger.debug(f"Retrieved {len(children)} cached children (newly built)")
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



