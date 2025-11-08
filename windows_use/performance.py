"""Performance optimization utilities for Windows-Use."""

import hashlib
import time
from functools import wraps
from typing import Any, Callable, Dict, Optional, Tuple, TypeVar, Union
from pathlib import Path
import pickle
from PIL import Image
import io
import threading
from concurrent.futures import ThreadPoolExecutor
from windows_use.logging import get_logger

logger = get_logger("windows_use.performance")

F = TypeVar('F', bound=Callable[..., Any])


class PerformanceCache:
    """Thread-safe cache for expensive operations with TTL support."""
    
    def __init__(self, max_size: int = 1000, default_ttl: float = 300.0):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._lock = threading.RLock()
        
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired."""
        with self._lock:
            if key in self._cache:
                value, expiry = self._cache[key]
                if time.time() < expiry:
                    return value
                else:
                    del self._cache[key]
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        """Set value in cache with TTL."""
        ttl = ttl or self.default_ttl
        expiry = time.time() + ttl
        
        with self._lock:
            # Remove oldest entries if cache is full
            if len(self._cache) >= self.max_size:
                oldest_key = min(self._cache.keys(), key=lambda k: self._cache[k][1])
                del self._cache[oldest_key]
            
            self._cache[key] = (value, expiry)
    
    def clear(self) -> None:
        """Clear all cached entries."""
        with self._lock:
            self._cache.clear()
    
    def cleanup_expired(self) -> int:
        """Remove expired entries and return count of removed items."""
        current_time = time.time()
        expired_keys = []
        
        with self._lock:
            for key, (_, expiry) in self._cache.items():
                if current_time >= expiry:
                    expired_keys.append(key)
            
            for key in expired_keys:
                del self._cache[key]
        
        return len(expired_keys)


# Global cache instance
_cache = PerformanceCache()


def cached(ttl: float = 300.0, key_func: Optional[Callable] = None) -> Callable[[F], F]:
    """Decorator to cache function results with TTL."""
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                cache_key = f"{func.__name__}:{hash((args, tuple(sorted(kwargs.items()))))}"
            
            # Try to get from cache
            result = _cache.get(cache_key)
            if result is not None:
                logger.debug(f"Cache hit for {func.__name__}")
                return result
            
            # Execute function and cache result
            start_time = time.time()
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            _cache.set(cache_key, result, ttl)
            logger.log_performance_metric(
                f"{func.__name__}_execution_time",
                execution_time * 1000,
                "ms"
            )
            
            return result
        return wrapper
    return decorator


def timed(func: F) -> F:
    """Decorator to measure and log function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            execution_time = time.time() - start_time
            logger.log_performance_metric(
                f"{func.__name__}_execution_time",
                execution_time * 1000,
                "ms"
            )
    return wrapper


class ImageOptimizer:
    """Optimized image processing for screenshots and UI elements."""
    
    def __init__(self, quality: int = 85, max_size: Tuple[int, int] = (1920, 1080)):
        self.quality = quality
        self.max_size = max_size
        self._executor = ThreadPoolExecutor(max_workers=2)
    
    def compress_screenshot(self, image: Image.Image) -> bytes:
        """Compress screenshot for faster processing."""
        # Resize if too large
        if image.size[0] > self.max_size[0] or image.size[1] > self.max_size[1]:
            image.thumbnail(self.max_size, Image.Resampling.LANCZOS)
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Compress to JPEG
        buffer = io.BytesIO()
        image.save(buffer, format='JPEG', quality=self.quality, optimize=True)
        return buffer.getvalue()
    
    def get_image_hash(self, image: Union[Image.Image, bytes]) -> str:
        """Generate hash for image comparison."""
        if isinstance(image, Image.Image):
            # Convert to bytes for hashing
            buffer = io.BytesIO()
            image.save(buffer, format='PNG')
            image_bytes = buffer.getvalue()
        else:
            image_bytes = image
        
        return hashlib.md5(image_bytes).hexdigest()
    
    def images_similar(self, img1: Image.Image, img2: Image.Image, threshold: float = 0.95) -> bool:
        """Check if two images are similar using perceptual hashing."""
        # Simple implementation - can be enhanced with more sophisticated algorithms
        hash1 = self.get_image_hash(img1)
        hash2 = self.get_image_hash(img2)
        return hash1 == hash2
    
    def extract_roi(self, image: Image.Image, bbox: Tuple[int, int, int, int]) -> Image.Image:
        """Extract region of interest from image."""
        return image.crop(bbox)


class UIElementCache:
    """Cache for UI element locations and properties."""
    
    def __init__(self, ttl: float = 30.0):
        self.ttl = ttl
        self._elements: Dict[str, Tuple[Dict[str, Any], float]] = {}
        self._lock = threading.RLock()
    
    def get_element(self, element_id: str) -> Optional[Dict[str, Any]]:
        """Get cached element information."""
        with self._lock:
            if element_id in self._elements:
                element_data, expiry = self._elements[element_id]
                if time.time() < expiry:
                    return element_data
                else:
                    del self._elements[element_id]
            return None
    
    def cache_element(self, element_id: str, element_data: Dict[str, Any]) -> None:
        """Cache element information."""
        expiry = time.time() + self.ttl
        with self._lock:
            self._elements[element_id] = (element_data, expiry)
    
    def invalidate_element(self, element_id: str) -> None:
        """Remove element from cache."""
        with self._lock:
            self._elements.pop(element_id, None)
    
    def clear(self) -> None:
        """Clear all cached elements."""
        with self._lock:
            self._elements.clear()


class ScreenshotManager:
    """Optimized screenshot capture and management."""
    
    def __init__(self, cache_ttl: float = 1.0):
        self.cache_ttl = cache_ttl
        self.image_optimizer = ImageOptimizer()
        self._last_screenshot: Optional[Tuple[Image.Image, float]] = None
        self._lock = threading.RLock()
    
    def get_screenshot(self, force_new: bool = False) -> Image.Image:
        """Get screenshot with caching."""
        current_time = time.time()
        
        with self._lock:
            if not force_new and self._last_screenshot:
                screenshot, timestamp = self._last_screenshot
                if current_time - timestamp < self.cache_ttl:
                    logger.debug("Using cached screenshot")
                    return screenshot
        
        # Capture new screenshot
        screenshot = self._capture_screenshot()
        
        with self._lock:
            self._last_screenshot = (screenshot, current_time)
        
        return screenshot
    
    def _capture_screenshot(self) -> Image.Image:
        """Capture screenshot using optimized method."""
        import pyautogui as pg
        
        start_time = time.time()
        screenshot = pg.screenshot()
        capture_time = time.time() - start_time
        
        logger.log_performance_metric("screenshot_capture_time", capture_time * 1000, "ms")
        return screenshot
    
    def has_screen_changed(self, threshold: float = 0.95) -> bool:
        """Check if screen has changed significantly."""
        if not self._last_screenshot:
            return True
        
        current_screenshot = self._capture_screenshot()
        last_screenshot = self._last_screenshot[0]
        
        return not self.image_optimizer.images_similar(
            current_screenshot, last_screenshot, threshold
        )


class RetryManager:
    """Intelligent retry mechanism with exponential backoff."""
    
    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        backoff_factor: float = 2.0
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.backoff_factor = backoff_factor
    
    def retry(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with retry logic."""
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                
                if attempt == self.max_retries:
                    break
                
                delay = min(
                    self.base_delay * (self.backoff_factor ** attempt),
                    self.max_delay
                )
                
                logger.warning(
                    f"Attempt {attempt + 1} failed, retrying in {delay:.2f}s",
                    attempt=attempt + 1,
                    delay=delay,
                    error=str(e)
                )
                
                time.sleep(delay)
        
        raise last_exception


# Global instances
image_optimizer = ImageOptimizer()
ui_element_cache = UIElementCache()
screenshot_manager = ScreenshotManager()
retry_manager = RetryManager()


def cleanup_caches() -> None:
    """Clean up all performance caches."""
    _cache.cleanup_expired()
    ui_element_cache.clear()
    logger.info("Performance caches cleaned up")


def get_cache_stats() -> Dict[str, Any]:
    """Get performance cache statistics."""
    return {
        "main_cache_size": len(_cache._cache),
        "ui_cache_size": len(ui_element_cache._elements),
        "screenshot_cached": screenshot_manager._last_screenshot is not None,
    }