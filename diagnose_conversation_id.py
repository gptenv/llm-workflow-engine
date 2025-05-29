#!/usr/bin/env python3
"""
LWE Conversation ID Diagnostic Tool

This tool helps diagnose conversation_id feature issues.
Run this script to check your configuration and test the feature.

Usage: python diagnose_conversation_id.py
"""

import sys
import os

# Add LWE to path
sys.path.insert(0, os.path.abspath('.'))

try:
    from lwe.core.config import Config
    from lwe.backends.api.request import ApiRequest
    from unittest.mock import Mock
    from langchain_core.messages import AIMessage
except ImportError as e:
    print(f"❌ Error importing LWE modules: {e}")
    print("Make sure you're running this from the LWE root directory")
    sys.exit(1)

def check_configuration():
    """Check if conversation_id is properly configured"""
    print("=== Configuration Check ===")
    
    config = Config()
    send_conversation_id = config.get("backend_options.send_conversation_id", False)
    
    print(f"send_conversation_id setting: {send_conversation_id}")
    
    if not send_conversation_id:
        print("❌ ISSUE: send_conversation_id is not enabled!")
        print("   Fix: Add 'backend_options.send_conversation_id: true' to your config")
        return False
    else:
        print("✅ send_conversation_id is enabled")
        return True

def test_extraction_capabilities():
    """Test conversation_id extraction capabilities"""
    print("\n=== Extraction Capability Test ===")
    
    config = Config()
    config.set("backend_options.send_conversation_id", True)
    
    provider = Mock()
    provider.name = "provider_chat_openai"
    
    request = ApiRequest(config=config, provider=provider, input="test")
    
    tests = [
        ("_conversation_id attribute", lambda: create_response_with_attr()),
        ("response_metadata", lambda: create_response_with_metadata()),
        ("additional_kwargs (custom APIs)", lambda: create_response_with_additional()),
    ]
    
    all_passed = True
    for test_name, create_response in tests:
        print(f"Testing {test_name}...")
        response = create_response()
        request.extracted_conversation_id = None
        request.extract_message_content(response)
        extracted = request.get_extracted_conversation_id()
        
        if extracted:
            print(f"  ✅ SUCCESS: Extracted '{extracted}'")
        else:
            print(f"  ❌ FAILED: No conversation_id extracted")
            all_passed = False
    
    return all_passed

def create_response_with_attr():
    response = AIMessage(content="Hello")
    response._conversation_id = "conv-attr-123"
    return response

def create_response_with_metadata():
    response = AIMessage(content="Hello")
    response.response_metadata = {"conversation_id": "conv-meta-456"}
    return response

def create_response_with_additional():
    response = AIMessage(content="Hello")
    response.additional_kwargs = {"conversation_id": "conv-additional-789"}
    return response

def show_debug_instructions():
    """Show instructions for debugging"""
    print("\n=== Debug Instructions ===")
    
    print("1. Enable debug logging in your config:")
    print("   logging:")
    print("     level: DEBUG")
    print()
    print("2. Look for these log messages when testing:")
    print("   - 'Adding conversation_id to request: <id>'")
    print("   - 'Extracted conversation_id from additional_kwargs: <id>'")
    print("   - 'Storing external conversation_id for conversation <id>: <external_id>'")
    print()
    print("3. Test with your custom API:")
    print("   - First message: Check if conversation_id is extracted from response")
    print("   - Second message: Check if conversation_id is sent in request")

def show_sample_config():
    """Show sample configuration"""
    print("\n=== Sample Configuration ===")
    
    config_sample = """
# Enable conversation_id feature
backend: api
backend_options:
  send_conversation_id: true
  auto_create_first_user: your_username

# Use OpenAI provider with custom API
model_customizations:
  openai_api_base: "https://your-custom-api.com/v1"
  openai_api_key: "your-api-key"

# Enable debug logging
logging:
  level: DEBUG
"""
    print(config_sample)

def main():
    print("🔍 LWE Conversation ID Diagnostic Tool")
    print("=" * 50)
    
    config_ok = check_configuration()
    extraction_ok = test_extraction_capabilities()
    
    show_sample_config()
    show_debug_instructions()
    
    print("\n" + "=" * 50)
    print("📋 SUMMARY")
    
    if config_ok and extraction_ok:
        print("✅ All checks passed!")
        print()
        print("If the feature still isn't working:")
        print("1. Enable debug logging and check the log messages")
        print("2. Verify your custom API returns conversation_id in responses")
        print("3. Most custom APIs return it in additional_kwargs")
    else:
        print("❌ Issues found!")
        if not config_ok:
            print("  - Fix configuration first")
        if not extraction_ok:
            print("  - Extraction capabilities failed (this shouldn't happen)")
    
    print()
    print("💡 The conversation_id feature should now work with custom APIs")
    print("   that return conversation_id in any of the supported formats.")

if __name__ == "__main__":
    main()