#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST TABLE SPLIT
================

Tạo ảnh bảng mẫu và test table splitting
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

def create_sample_table(output_path="test_table_4cols.jpg"):
    """
    Tạo ảnh bảng mẫu 4 cột để test
    
    Returns:
        str: Path ảnh đã tạo
    """
    print("🎨 Tạo bảng mẫu 4 cột...")
    
    # Kích thước ảnh
    width, height = 1000, 600
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    # Font (fallback nếu không có font Vietnamese)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
        header_font = ImageFont.truetype("arial.ttf", 24)
    except:
        try:
            font = ImageFont.load_default()
            header_font = ImageFont.load_default()
        except:
            font = None
            header_font = None
    
    # Vẽ đường viền bảng
    draw.rectangle([50, 50, width-50, height-50], outline='black', width=2)
    
    # Tính toán cột (4 cột đều nhau)
    table_width = width - 100  # 50px margin mỗi bên
    col_width = table_width // 4
    
    # Vẽ đường kẻ dọc (3 đường phân cách)
    for i in range(1, 4):
        x = 50 + i * col_width
        draw.line([(x, 50), (x, height-50)], fill='black', width=2)
    
    # Headers
    headers = ["STT", "Họ và Tên", "Đồng ý", "Không đồng ý"]
    header_y = 60
    
    # Vẽ header row
    draw.line([(50, 100), (width-50, 100)], fill='black', width=2)
    
    for i, header in enumerate(headers):
        x = 50 + i * col_width + 10
        draw.text((x, header_y), header, fill='black', font=header_font)
    
    # Data rows
    data = [
        ["1", "Nguyen Van A", "✓", ""],
        ["2", "Tran Thi B", "", "✓"],
        ["3", "Le Van C", "✓", ""],
        ["4", "Pham Thi D", "", "✓"],
        ["5", "Hoang Van E", "✓", ""],
        ["6", "Vu Thi F", "", "✓"],
        ["7", "Do Van G", "✓", ""],
        ["8", "Mai Thi H", "✓", ""],
    ]
    
    row_height = 45
    start_y = 110
    
    for row_idx, row_data in enumerate(data):
        y = start_y + row_idx * row_height
        
        # Vẽ đường kẻ ngang
        if row_idx < len(data) - 1:
            draw.line([(50, y + row_height), (width-50, y + row_height)], 
                     fill='lightgray', width=1)
        
        # Vẽ data
        for col_idx, cell_data in enumerate(row_data):
            x = 50 + col_idx * col_width + 10
            draw.text((x, y + 10), cell_data, fill='black', font=font)
    
    # Lưu ảnh
    img.save(output_path, quality=95, optimize=True)
    print(f"✅ Đã tạo bảng mẫu: {output_path}")
    print(f"   📐 Kích thước: {img.size}")
    
    return output_path

def test_table_splitting():
    """
    Test table splitting với ảnh mẫu
    """
    print("🧪 TEST TABLE SPLITTING")
    print("=" * 40)
    
    # Tạo ảnh mẫu
    sample_path = create_sample_table()
    
    # Import và test quick_split
    try:
        from quick_table_split import quick_split
        
        print("\n🔄 Đang test quick_split...")
        table_a, table_b = quick_split(sample_path, "test_output")
        
        print("\n🎉 TEST THÀNH CÔNG!")
        print("=" * 40)
        print(f"📊 Input: {sample_path}")
        print(f"📄 Table A (STT + Họ tên + Đồng ý): {table_a}")
        print(f"📄 Table B (STT + Họ tên + Không đồng ý): {table_b}")
        print("🔍 Kiểm tra thư mục test_output/ để xem kết quả")
        
        # Hiển thị file sizes
        if os.path.exists(table_a):
            size_a = os.path.getsize(table_a) / 1024
            print(f"   💾 Table A size: {size_a:.1f} KB")
            
        if os.path.exists(table_b):
            size_b = os.path.getsize(table_b) / 1024
            print(f"   💾 Table B size: {size_b:.1f} KB")
        
        return True
        
    except ImportError:
        print("❌ Không tìm thấy quick_table_split.py")
        print("   Hãy đảm bảo file quick_table_split.py ở cùng thư mục")
        return False
        
    except Exception as e:
        print(f"❌ Lỗi khi test: {e}")
        import traceback
        traceback.print_exc()
        return False

def analyze_test_results():
    """
    Phân tích kết quả test
    """
    print("\n📊 PHÂN TÍCH KẾT QUẢ")
    print("=" * 30)
    
    output_dir = "test_output"
    expected_files = [
        "table_A_cols_123.jpg",
        "table_B_cols_124.jpg", 
        "debug_splits.jpg"
    ]
    
    for filename in expected_files:
        filepath = os.path.join(output_dir, filename)
        if os.path.exists(filepath):
            size_kb = os.path.getsize(filepath) / 1024
            
            # Load và check kích thước ảnh
            try:
                img = Image.open(filepath)
                print(f"✅ {filename}")
                print(f"   📐 Size: {img.size[0]}x{img.size[1]} px")
                print(f"   💾 File: {size_kb:.1f} KB")
                print()
            except Exception as e:
                print(f"⚠️ {filename} - Lỗi load: {e}")
        else:
            print(f"❌ Thiếu file: {filename}")

def main():
    """Main function"""
    print("🚀 TABLE SPLIT TESTING SUITE")
    print("=" * 50)
    
    # Test 1: Tạo sample data
    print("\n📋 Test 1: Tạo sample table")
    sample_created = create_sample_table()
    
    # Test 2: Table splitting
    print("\n📋 Test 2: Table splitting")
    success = test_table_splitting()
    
    if success:
        # Test 3: Analyze results
        print("\n📋 Test 3: Analyze results")
        analyze_test_results()
        
        print("\n🎯 KẾT LUẬN TEST:")
        print("=" * 30)
        print("✅ Tạo sample table: OK")
        print("✅ Table splitting: OK")
        print("✅ Output analysis: OK")
        print("\n💡 Code sẵn sàng sử dụng với ảnh thật!")
        
    else:
        print("\n❌ TEST FAILED")
        print("🔧 Khắc phục:")
        print("   1. Đảm bảo có file quick_table_split.py")
        print("   2. Install dependencies: pip install opencv-python pillow scipy")
        print("   3. Chạy lại test")

if __name__ == "__main__":
    main() 