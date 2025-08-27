#!/usr/bin/env python3
"""
Test script for browser token retrieval functionality
"""

import asyncio
import os
import sys

# Add the project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chatgpt.browser_token import get_browser_access_token
from chatgpt.authorization import get_auto_browser_token, refresh_browser_token
from utils.Logger import logger


async def test_browser_token_retrieval():
    """Test the browser token retrieval functionality"""
    logger.info("=== Testing Browser Token Retrieval ===")
    
    try:
        # Test direct browser token retrieval
        logger.info("Testing direct browser token retrieval...")
        token = await get_browser_access_token()
        
        if token:
            logger.info(f"✓ Successfully retrieved token: {token[:50]}...")
            logger.info(f"  Token length: {len(token)}")
            logger.info(f"  Token type: {'JWT' if token.startswith('eyJhbGciOi') else 'Other'}")
            return True
        else:
            logger.error("✗ Failed to retrieve token")
            return False
            
    except Exception as e:
        logger.error(f"✗ Error during token retrieval: {e}")
        return False


async def test_auth_integration():
    """Test the integration with authorization module"""
    logger.info("\n=== Testing Authorization Integration ===")
    
    try:
        # Set the environment variable for testing
        os.environ['AUTO_BROWSER_TOKEN'] = 'true'
        
        # Re-import config to pick up the new env var
        import utils.config as configs
        configs.auto_browser_token = True
        
        logger.info("Testing get_auto_browser_token...")
        token = await get_auto_browser_token()
        
        if token:
            logger.info(f"✓ Authorization integration successful: {token[:50]}...")
            return True
        else:
            logger.error("✗ Authorization integration failed")
            return False
            
    except Exception as e:
        logger.error(f"✗ Error during authorization integration test: {e}")
        return False


async def main():
    """Run all tests"""
    logger.info("Starting browser token tests...")
    
    success_count = 0
    total_tests = 2
    
    # Test 1: Direct token retrieval
    if await test_browser_token_retrieval():
        success_count += 1
    
    # Test 2: Authorization integration
    if await test_auth_integration():
        success_count += 1
    
    # Summary
    logger.info(f"\n=== Test Results ===")
    logger.info(f"Tests passed: {success_count}/{total_tests}")
    
    if success_count == total_tests:
        logger.info("✓ All tests passed!")
        return 0
    else:
        logger.error("✗ Some tests failed")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)