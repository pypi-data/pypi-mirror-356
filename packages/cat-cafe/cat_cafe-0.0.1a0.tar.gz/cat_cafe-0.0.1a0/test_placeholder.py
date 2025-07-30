#!/usr/bin/env python3
"""
Quick test script for the placeholder package
"""

import sys
sys.path.insert(0, 'src')

import cat_cafe

def test_placeholder():
    print("Testing cat-cafe placeholder package...")
    
    # Test version
    print(f"Version: {cat_cafe.__version__}")
    
    # Test placeholder_info function
    info = cat_cafe.placeholder_info()
    print(f"Package info: {info}")
    
    print("✅ Placeholder package working correctly!")

if __name__ == "__main__":
    test_placeholder()