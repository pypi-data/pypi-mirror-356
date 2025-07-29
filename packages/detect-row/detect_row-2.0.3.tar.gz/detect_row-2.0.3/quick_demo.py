#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEMO NHANH - HỆ THỐNG TRÍCH XUẤT BẢNG
=====================================

Script demo nhanh để test các tính năng chính:
- Tạo ảnh mẫu nếu chưa có
- Test trích xuất bảng cơ bản
- Test trích xuất cột với merge
- Hiển thị kết quả trực quan

Cách sử dụng:
    python quick_demo.py
    python quick_demo.py --create-sample
    python quick_demo.py --show-results
"""

import os
import sys
import cv2
import numpy as np
import argparse
from pathlib import Path

# Add current directory to path
sys.path.insert(0, '.')

def create_sample_table_image():
    """Tạo ảnh bảng mẫu để test"""
    print("🎨 Tạo ảnh bảng mẫu...")
    
    # Tạo ảnh trắng
    img = np.ones((800, 1200, 3), dtype=np.uint8) * 255
    
    # Title
    cv2.putText(img, 'DANH SACH BINH CHON', (400, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    
    # Table 1 - Main table
    x1, y1, x2, y2 = 50, 100, 1150, 400
    
    # Outer border
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 0), 2)
    
    # Header row
    cv2.rectangle(img, (x1, y1), (x2, y1+50), (220, 220, 220), -1)
    cv2.rectangle(img, (x1, y1), (x2, y1+50), (0, 0, 0), 1)
    
    # Column headers
    headers = ['STT', 'HO VA TEN', 'DONG Y', 'KHONG DONG Y']
    col_widths = [100, 500, 275, 275]
    x_pos = x1
    
    for i, (header, width) in enumerate(zip(headers, col_widths)):
        if i > 0:
            cv2.line(img, (x_pos, y1), (x_pos, y2), (0, 0, 0), 1)
        
        # Text
        text_x = x_pos + width//2 - len(header)*8
        cv2.putText(img, header, (text_x, y1+30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
        x_pos += width
    
    # Data rows
    data = [
        ['1', 'NGUYEN VAN A', 'X', ''],
        ['2', 'TRAN THI B', '', 'X'],  
        ['3', 'LE VAN C', 'X', ''],
        ['4', 'PHAM THI D', 'X', ''],
        ['5', 'HOANG VAN E', '', 'X']
    ]
    
    for row_idx, row_data in enumerate(data):
        y_row = y1 + 50 + (row_idx + 1) * 50
        
        # Row line
        cv2.line(img, (x1, y_row), (x2, y_row), (0, 0, 0), 1)
        
        # Cell data
        x_pos = x1
        for col_idx, (cell_data, width) in enumerate(zip(row_data, col_widths)):
            if col_idx > 0:
                cv2.line(img, (x_pos, y1+50), (x_pos, y2), (0, 0, 0), 1)
            
            if cell_data:
                text_x = x_pos + width//2 - len(cell_data)*8
                cv2.putText(img, cell_data, (text_x, y_row-15), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
            x_pos += width
    
    # Table 2 - Summary table
    x1, y1, x2, y2 = 50, 450, 600, 550
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 0), 2)
    cv2.line(img, (x1+200, y1), (x1+200, y2), (0, 0, 0), 1)
    cv2.line(img, (x1+400, y1), (x1+400, y2), (0, 0, 0), 1)
    cv2.line(img, (x1, y1+50), (x2, y1+50), (0, 0, 0), 1)
    
    # Summary headers
    cv2.putText(img, 'TONG KET', (x1+10, y1+30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
    cv2.putText(img, 'DONG Y', (x1+210, y1+30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
    cv2.putText(img, 'KHONG DONG Y', (x1+410, y1+30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
    
    # Summary data
    cv2.putText(img, 'KET QUA', (x1+10, y1+80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.putText(img, '3', (x1+250, y1+80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.putText(img, '2', (x1+450, y1+80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    
    # Table 3 - Small info table
    x1, y1, x2, y2 = 700, 450, 1150, 550
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 0), 2)
    cv2.line(img, (x1, y1+50), (x2, y1+50), (0, 0, 0), 1)
    
    cv2.putText(img, 'THONG TIN', (x1+150, y1+30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
    cv2.putText(img, 'Ngay: 18/06/2025', (x1+10, y1+80), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
    
    # Save image
    os.makedirs('input', exist_ok=True)
    cv2.imwrite('input/demo_table.jpg', img)
    print("✅ Đã tạo ảnh mẫu: input/demo_table.jpg")
    return 'input/demo_table.jpg'

def run_basic_extraction():
    """Chạy trích xuất cơ bản"""
    print("\n🔄 Chạy trích xuất bảng cơ bản...")
    
    try:
        from detect_row import AdvancedTableExtractor
        
        # Table extraction
        table_extractor = AdvancedTableExtractor(
            input_dir="input",
            output_dir="output/demo/tables",
            debug_dir="debug/demo"
        )
        
        tables = table_extractor.extract_tables_from_image("demo_table.jpg")
        
        if tables:
            print(f"✅ Phát hiện {len(tables)} bảng:")
            for i, table in enumerate(tables):
                print(f"   📋 Bảng {i+1}: {table['width']}x{table['height']} pixels")
        else:
            print("❌ Không phát hiện bảng nào")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi trích xuất bảng: {e}")
        return False

def run_column_extraction():
    """Chạy trích xuất cột với merge"""
    print("\n📊 Chạy trích xuất cột với merge...")
    
    try:
        from detect_row import AdvancedColumnExtractor
        
        # Check if tables exist
        table_dir = Path("output/demo/tables")
        if not table_dir.exists():
            print("❌ Chưa có bảng để trích xuất cột")
            return False
        
        table_files = list(table_dir.glob("*.jpg"))
        if not table_files:
            print("❌ Không tìm thấy file bảng")
            return False
        
        # Column groups for demo
        column_groups = {
            'stt': [1],
            'ho_ten': [2], 
            'dong_y': [3],
            'khong_dong_y': [4],
            'thong_tin_ca_nhan': [1, 2],
            'ket_qua_binh_chon': [3, 4],
            'toan_bo': [1, 2, 3, 4]
        }
        
        total_columns = 0
        
        for table_file in table_files:
            table_name = table_file.stem
            print(f"   🔄 Xử lý {table_name}...")
            
            column_extractor = AdvancedColumnExtractor(
                input_dir=str(table_dir),
                output_dir=f"output/demo/columns/{table_name}",
                debug_dir=f"debug/demo/columns/{table_name}"
            )
            
            columns = column_extractor.extract_columns_from_image(
                table_file.name,
                column_groups=column_groups
            )
            
            if columns:
                individual_count = len([c for c in columns if len(c['columns']) == 1])
                merged_count = len([c for c in columns if len(c['columns']) > 1])
                print(f"      ✅ {individual_count} cột riêng + {merged_count} cột merge")
                total_columns += len(columns)
            else:
                print(f"      ❌ Không trích xuất được cột")
        
        print(f"✅ Tổng cộng: {total_columns} files cột")
        return True
        
    except Exception as e:
        print(f"❌ Lỗi trích xuất cột: {e}")
        return False

def show_results():
    """Hiển thị kết quả demo"""
    print("\n📋 KẾT QUẢ DEMO:")
    print("=" * 50)
    
    # Count files
    def count_files(directory, pattern="*.jpg"):
        if os.path.exists(directory):
            return len(list(Path(directory).rglob(pattern)))
        return 0
    
    # Input
    input_count = count_files("input")
    print(f"📁 Input: {input_count} ảnh")
    
    # Tables
    table_count = count_files("output/demo/tables")
    print(f"📋 Bảng: {table_count} files")
    
    # Columns
    column_count = count_files("output/demo/columns")
    print(f"📊 Cột: {column_count} files")
    
    # Debug
    debug_count = count_files("debug/demo")
    print(f"🐛 Debug: {debug_count} files")
    
    # Show structure
    if os.path.exists("output/demo"):
        print(f"\n📁 Cấu trúc kết quả:")
        for root, dirs, files in os.walk("output/demo"):
            level = root.replace("output/demo", "").count(os.sep)
            indent = " " * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = " " * 2 * (level + 1)
            for file in files[:5]:  # Show first 5 files
                print(f"{subindent}{file}")
            if len(files) > 5:
                print(f"{subindent}... và {len(files) - 5} files khác")

def check_dependencies():
    """Kiểm tra dependencies cơ bản"""
    print("🔍 Kiểm tra dependencies...")
    
    required = ['cv2', 'numpy']
    missing = []
    
    for module in required:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module}")
            missing.append(module)
    
    if missing:
        print(f"\n❌ Thiếu dependencies: {', '.join(missing)}")
        print("Cài đặt với: pip install opencv-python numpy")
        return False
    
    # Check package
    try:
        from detect_row import AdvancedTableExtractor
        print("✅ detect_row package")
    except ImportError:
        print("❌ detect_row package không import được")
        return False
    
    return True

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Demo nhanh hệ thống trích xuất bảng')
    parser.add_argument('--create-sample', action='store_true',
                       help='Tạo ảnh mẫu')
    parser.add_argument('--show-results', action='store_true',
                       help='Chỉ hiển thị kết quả')
    parser.add_argument('--skip-extraction', action='store_true',
                       help='Bỏ qua trích xuất')
    
    args = parser.parse_args()
    
    print("🚀 DEMO NHANH - HỆ THỐNG TRÍCH XUẤT BẢNG")
    print("=" * 50)
    
    # Show results only
    if args.show_results:
        show_results()
        return
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Demo không thể chạy do thiếu dependencies")
        return
    
    # Create sample if requested or no input exists
    if args.create_sample or not os.path.exists('input/demo_table.jpg'):
        create_sample_table_image()
    
    if args.skip_extraction:
        print("\n⏭️ Bỏ qua trích xuất")
        show_results()
        return
    
    # Run extraction
    success = True
    
    # 1. Table extraction
    if not run_basic_extraction():
        success = False
    
    # 2. Column extraction
    if success and not run_column_extraction():
        success = False
    
    # 3. Show results
    if success:
        show_results()
        print(f"\n🎉 Demo hoàn thành thành công!")
        print(f"   • Kiểm tra kết quả trong output/demo/")
        print(f"   • Xem debug files trong debug/demo/")
        print(f"   • Chạy workflow đầy đủ với: python run_complete_workflow.py")
    else:
        print(f"\n❌ Demo có lỗi!")
        print(f"   • Kiểm tra dependencies với: python system_check.py")
        print(f"   • Xem log errors ở trên")

if __name__ == "__main__":
    main() 