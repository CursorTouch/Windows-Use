"""Performance tests for Windows-Use components."""

import pytest
import time
from unittest.mock import Mock, patch
from PIL import Image
from windows_use.performance import (
    PerformanceCache, cached, timed, ImageOptimizer, 
    UIElementCache, ScreenshotManager, RetryManager
)


class TestPerformanceCache:
    """Test the performance cache implementation."""
    
    def test_cache_basic_operations(self):
        """Test basic cache set/get operations."""
        cache = PerformanceCache(max_size=10, default_ttl=1.0)
        
        # Test set and get
        cache.set("key1", "value1")
        assert cache.get("key1") == "value1"
        
        # Test non-existent key
        assert cache.get("nonexistent") is None
    
    def test_cache_ttl_expiration(self):
        """Test that cache entries expire after TTL."""
        cache = PerformanceCache(max_size=10, default_ttl=0.1)
        
        cache.set("key1", "value1")
        assert cache.get("key1") == "value1"
        
        # Wait for expiration
        time.sleep(0.2)
        assert cache.get("key1") is None


class TestImageOptimizer:
    """Test the image optimizer."""
    
    def test_image_hash_generation(self):
        """Test image hash generation."""
        optimizer = ImageOptimizer()
        
        # Create a simple test image
        image = Image.new('RGB', (100, 100), color='red')
        hash1 = optimizer.get_image_hash(image)
        
        # Same image should produce same hash
        hash2 = optimizer.get_image_hash(image)
        assert hash1 == hash2
        
        # Different image should produce different hash
        image2 = Image.new('RGB', (100, 100), color='blue')
        hash3 = optimizer.get_image_hash(image2)
        assert hash1 != hash3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])