#!/usr/bin/env python3
"""Test the reorganized architecture."""

import tempfile
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_architecture():
    """Test the new architecture without circular imports."""
    try:
        # Test storage imports
        from patronus.prompts.storage import LocalPromptStorage, StorageInfo
        print("✓ Storage imports successful")
        
        # Test provider imports
        from patronus.prompts.providers import LocalPromptProvider, APIPromptProvider
        print("✓ Provider imports successful")
        
        # Test CLI imports
        from patronus.cli.commands.prompts import pull, tidy
        print("✓ CLI command imports successful")
        
        # Test provider factory from clients
        from patronus.prompts.clients import PromptClient
        print("✓ Client imports successful")
        
        # Test storage instantiation
        with tempfile.TemporaryDirectory() as temp_dir:
            storage = LocalPromptStorage(temp_dir)
            print("✓ Storage instantiation successful")
            
            # Test provider instantiation
            provider = LocalPromptProvider(temp_dir)
            print("✓ Provider instantiation successful")
            
            # Test client with new providers
            client = PromptClient()
            print("✓ Client instantiation successful")
        
        print("\n✅ All tests passed! Architecture is correct.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_architecture()
    sys.exit(0 if success else 1)
