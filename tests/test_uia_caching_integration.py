"""
Test script to verify UIA caching integration.

This script tests the caching implementation.
Note: enable_caching and other_apps/active_app arguments have been removed in latest Tree API.
"""

import time
import logging
from windows_use.agent.tree.service import Tree
from windows_use.agent.desktop.service import Desktop

# Configure logging to see cache performance stats
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def test_caching_performance():
    """Test Tree.get_state with current API."""
    
    logger.info("=" * 70)
    logger.info("UIA TREE STATE TEST")
    logger.info("=" * 70)
    
    # Create desktop instance
    desktop = Desktop()
    
    # Test get_state
    logger.info("\n" + "=" * 70)
    logger.info("TESTING Tree.get_state")
    logger.info("=" * 70)
    
    tree = Tree(desktop)
    start_time = time.perf_counter()
    
    try:
        # Get actual handles from desktop to make a real call if possible
        # or just use dummy handles for a unit-like integration test.
        # the Desktop.get_state uses get_controls_handles etc.
        state = tree.get_state(active_window_handle=None, other_windows_handles=[])
        duration = time.perf_counter() - start_time
        
        logger.info(f"Time: {duration:.3f}s")
        if state.interactive_nodes is not None:
            logger.info(f"Interactive elements found: {len(state.interactive_nodes)}")
        if state.scrollable_nodes is not None:
            logger.info(f"Scrollable elements found: {len(state.scrollable_nodes)}")
        if state.root_node:
            logger.info(f"Root Node: {state.root_node.name} ({state.root_node.control_type})")
    except Exception as e:
        logger.error(f"Error during tree test: {e}")
        raise e

if __name__ == "__main__":
    try:
        test_caching_performance()
    except Exception as e:
        logger.error(f"Test failed with error: {e}", exc_info=True)
