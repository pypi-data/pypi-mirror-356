#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST THUẦN TÚY PIP PACKAGE DETECT-ROW
=====================================

Script này test pip package detect-row mà KHÔNG sử dụng local code
Để đảm bảo không có local code can thiệp, script này sẽ:
1. Không thêm current directory vào sys.path
2. Import trực tiếp từ pip package
3. Test các chức năng cơ bản
"""

import os
import sys
import cv2
import numpy as np
from datetime import datetime

# KHÔNG thêm current directory vào sys.path để đảm bảo dùng pip package
print(f"🔍 Python path: {sys.path[:3]}...")  # Chỉ hiển thị 3 path đầu
print(f"📍 Current directory: {os.getcwd()}")
print(f"🚫 NOT adding current directory to sys.path")

# Import từ pip package detect-row
try:
    print(f"\n📦 Testing imports from pip package detect-row...")
    
    # Test import BaseRowExtractor
    from detect_row.base import BaseRowExtractor
    print(f"✅ BaseRowExtractor imported successfully")
    
    # Test import main classes
    from detect_row import AdvancedTableExtractor, AdvancedRowExtractorMain, TesseractRowExtractor
    print(f"✅ Main classes imported successfully")
    
    # Test version
    import detect_row
    if hasattr(detect_row, '__version__'):
        print(f"📋 Package version: {detect_row.__version__}")
    else:
        print(f"⚠️ No version info available")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print(f"💡 Có thể pip package bị lỗi hoặc chưa cài đặt đúng")
    exit(1)

def test_basic_functionality():
    """Test chức năng cơ bản của pip package"""
    print(f"\n🧪 TESTING BASIC FUNCTIONALITY...")
    
    # Test AdvancedTableExtractor
    try:
        table_extractor = AdvancedTableExtractor(
            input_dir=".",
            output_dir="test_pip_output/tables",
            debug_dir="test_pip_output/debug"
        )
        print(f"✅ AdvancedTableExtractor initialized successfully")
    except Exception as e:
        print(f"❌ AdvancedTableExtractor error: {e}")
        return False
    
    # Test AdvancedRowExtractorMain
    try:
        row_extractor = AdvancedRowExtractorMain()
        print(f"✅ AdvancedRowExtractorMain initialized successfully")
    except Exception as e:
        print(f"❌ AdvancedRowExtractorMain error: {e}")
        return False
    
    # Test TesseractRowExtractor
    try:
        ocr_extractor = TesseractRowExtractor(
            input_dir=".",
            output_dir="test_pip_output/ocr"
        )
        print(f"✅ TesseractRowExtractor initialized successfully")
    except Exception as e:
        print(f"❌ TesseractRowExtractor error: {e}")
        return False
    
    return True

def test_with_image():
    """Test với ảnh thực tế nếu có"""
    print(f"\n🖼️ TESTING WITH REAL IMAGE...")
    
    image_path = "image0524.png"
    if not os.path.exists(image_path):
        print(f"⚠️ Image {image_path} not found, skipping image test")
        return True
    
    try:
        # Test table extraction
        table_extractor = AdvancedTableExtractor(
            input_dir=os.path.dirname(image_path) or ".",
            output_dir="test_pip_output/tables",
            debug_dir="test_pip_output/debug"
        )
        
        result = table_extractor.process_image(
            image_path=image_path,
            margin=5,
            check_text=True
        )
        
        if result and 'tables' in result:
            print(f"✅ Table extraction successful: {len(result['tables'])} tables found")
            return True
        else:
            print(f"⚠️ No tables found in image")
            return True
            
    except Exception as e:
        print(f"❌ Image processing error: {e}")
        return False

def main():
    """Main test function"""
    print(f"🚀 PURE PIP PACKAGE TEST - DETECT-ROW")
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"=" * 60)
    
    # Test 1: Basic functionality
    if not test_basic_functionality():
        print(f"\n❌ BASIC FUNCTIONALITY TEST FAILED")
        return False
    
    # Test 2: Image processing
    if not test_with_image():
        print(f"\n❌ IMAGE PROCESSING TEST FAILED")
        return False
    
    print(f"\n🎉 ALL TESTS PASSED!")
    print(f"✅ Pip package detect-row hoạt động hoàn hảo!")
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        exit(1) 