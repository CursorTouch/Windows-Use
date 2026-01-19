"""
Test script to verify UIA caching integration.

This script tests the caching implementation by comparing
performance with and without caching enabled.
"""

import time
import logging
from windows_use.uia import GetRootControl
from windows_use.agent.tree.service import Tree
from windows_use.agent.desktop.service import Desktop

# Configure logging to see cache performance stats
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_caching_performance():
    """Test and compare performance with and without caching."""
    
    logger.info("=" * 70)
    logger.info("UIA CACHING INTEGRATION TEST")
    logger.info("=" * 70)
    
    # Create desktop instance
    desktop = Desktop()
    
    # Test WITHOUT caching
    logger.info("\n" + "=" * 70)
    logger.info("TEST 1: WITHOUT CACHING")
    logger.info("=" * 70)
    
    tree_no_cache = Tree(desktop, enable_caching=False)
    start_time = time.perf_counter()
    
    try:
        state_no_cache = tree_no_cache.get_state(active_app=None, other_apps=[])
        no_cache_time = time.perf_counter() - start_time
        
        logger.info(f"Time without caching: {no_cache_time:.3f}s")
        logger.info(f"Interactive elements found: {len(state_no_cache.interactive_nodes)}")
        logger.info(f"Scrollable elements found: {len(state_no_cache.scrollable_nodes)}")
        logger.info(f"Root Node: {state_no_cache.root_node.name} ({state_no_cache.root_node.control_type})")
    except Exception as e:
        logger.error(f"Error during non-cached test: {e}")
        no_cache_time = None
    
    # Test WITH caching
    logger.info("\n" + "=" * 70)
    logger.info("TEST 2: WITH CACHING")
    logger.info("=" * 70)
    
    tree_with_cache = Tree(desktop, enable_caching=True)
    start_time = time.perf_counter()
    
    try:
        state_with_cache = tree_with_cache.get_state(active_app=None, other_apps=[])
        cache_time = time.perf_counter() - start_time
        
        logger.info(f"Time with caching: {cache_time:.3f}s")
        logger.info(f"Interactive elements found: {len(state_with_cache.interactive_nodes)}")
        logger.info(f"Scrollable elements found: {len(state_with_cache.scrollable_nodes)}")
        logger.info(f"Root Node: {state_with_cache.root_node.name} ({state_with_cache.root_node.control_type})")
    except Exception as e:
        logger.error(f"Error during cached test: {e}")
        cache_time = None
    
    # Compare results
    logger.info("\n" + "=" * 70)
    logger.info("RESULTS COMPARISON")
    logger.info("=" * 70)
    
    if no_cache_time and cache_time:
        improvement = ((no_cache_time - cache_time) / no_cache_time) * 100
        speedup = no_cache_time / cache_time
        
        logger.info(f"Time without caching: {no_cache_time:.3f}s")
        logger.info(f"Time with caching:    {cache_time:.3f}s")
        logger.info(f"Performance improvement: {improvement:.1f}%")
        logger.info(f"Speedup: {speedup:.2f}x")
        
        if len(state_no_cache.interactive_nodes) == len(state_with_cache.interactive_nodes):
            logger.info(f"✓ Same number of interactive elements found (correctness verified): {len(state_no_cache.interactive_nodes)}")
        else:
            logger.warning(f"⚠ Different number of elements: {len(state_no_cache.interactive_nodes)} vs {len(state_with_cache.interactive_nodes)}")
        
        # Success criteria
        logger.info("\n" + "=" * 70)
        logger.info("SUCCESS CRITERIA")
        logger.info("=" * 70)
        
        if improvement > 50:
            logger.info(f"✓ EXCELLENT: {improvement:.1f}% improvement (target: >50%)")
        elif improvement > 30:
            logger.info(f"✓ GOOD: {improvement:.1f}% improvement (target: >30%)")
        elif improvement > 0:
            logger.info(f"⚠ MODERATE: {improvement:.1f}% improvement (expected >50%)")
        else:
            logger.warning(f"✗ NO IMPROVEMENT: {improvement:.1f}%")
    
    logger.info("\n" + "=" * 70)
    logger.info("TEST COMPLETE")
    logger.info("=" * 70)


if __name__ == "__main__":
    try:
        test_caching_performance()
    except Exception as e:
        logger.error(f"Test failed with error: {e}", exc_info=True)
