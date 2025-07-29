#!/usr/bin/env python3
"""
Demo trích xuất cột từ bảng
==========================

Script này minh họa cách sử dụng AdvancedColumnExtractor để:
1. Tìm tối đa 3 bảng trong ảnh 
2. Crop từng bảng
3. Trích xuất cột từ mỗi bảng
4. Lưu từng cột riêng biệt và gộp cột theo nhóm
"""

import os
import sys
import logging
from pathlib import Path

# Thêm thư mục gốc vào Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from detect_row.advanced_column_extractor import AdvancedColumnExtractor

def setup_logging():
    """Thiết lập logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('column_extraction.log', encoding='utf-8')
        ]
    )
    
    # Thiết lập encoding UTF-8 cho console trên Windows
    if os.name == 'nt':  # Windows
        try:
            # Thiết lập console UTF-8
            os.system('chcp 65001 > nul')
        except:
            pass

def main():
    """Hàm chính demo"""
    
    # Thiết lập logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    print("🚀 Demo Trích Xuất Cột Từ Bảng")
    print("=" * 50)
    
    # Cấu hình đường dẫn
    input_dir = "input"
    output_dir = "output/columns"  
    debug_dir = "debug/columns"
    
    # Tạo các thư mục nếu chưa tồn tại
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(debug_dir, exist_ok=True)
    
    # Khởi tạo AdvancedColumnExtractor
    print(f"📂 Khởi tạo AdvancedColumnExtractor...")
    print(f"   📥 Input: {input_dir}")
    print(f"   📤 Output: {output_dir}")
    print(f"   🔧 Debug: {debug_dir}")
    
    extractor = AdvancedColumnExtractor(
        input_dir=input_dir,
        output_dir=output_dir,
        debug_dir=debug_dir,
        min_column_width=30  # Chiều rộng tối thiểu của cột
    )
    
    # Định nghĩa nhóm cột cần gộp
    column_groups = {
        "first_two": [1, 2],     # Gộp cột 1 và 2 
        "third": [3],            # Cột 3 riêng
        "fourth": [4],           # Cột 4 riêng
        "last_columns": [5, 6, 7]  # Gộp các cột cuối
    }
    
    print(f"🔗 Cấu hình nhóm cột:")
    for group_name, columns in column_groups.items():
        print(f"   {group_name}: cột {columns}")
    
    # Tìm tất cả file ảnh trong thư mục input
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    input_path = Path(input_dir)
    
    image_files = []
    for ext in image_extensions:
        image_files.extend(input_path.glob(f'*{ext}'))
        image_files.extend(input_path.glob(f'*{ext.upper()}'))
    
    if not image_files:
        print(f"❌ Không tìm thấy file ảnh nào trong thư mục {input_dir}")
        print(f"   Hỗ trợ các định dạng: {', '.join(image_extensions)}")
        return
    
    print(f"📷 Tìm thấy {len(image_files)} file ảnh:")
    for img_file in image_files:
        print(f"   📄 {img_file.name}")
    
    # Xử lý từng ảnh
    total_tables = 0
    total_columns = 0
    
    for image_file in image_files:
        print(f"\n🔍 Xử lý ảnh: {image_file.name}")
        print("-" * 30)
        
        try:
            # Xử lý ảnh với tối đa 3 bảng
            result = extractor.process_image(
                image_path=image_file.name,
                save_individual=True,        # Lưu từng cột riêng
                column_groups=column_groups, # Gộp cột theo nhóm
                max_tables=3                 # Tối đa 3 bảng
            )
            
            if result["success"]:
                tables_processed = result["tables_processed"]
                individual_files = len(result["individual_files"])
                merged_files = len(result["merged_files"])
                
                total_tables += tables_processed
                total_columns += individual_files
                
                print(f"✅ Kết quả xử lý {image_file.name}:")
                print(f"   📊 Số bảng xử lý: {tables_processed}")
                print(f"   📁 File cột riêng: {individual_files}")
                print(f"   📁 File cột gộp: {merged_files}")
                
                # Chi tiết từng bảng
                for table_info in result["tables_info"]:
                    table_name = table_info["table_name"]
                    columns_count = table_info["columns_count"]
                    bbox = table_info["bbox"]
                    size = table_info["cropped_size"]
                    
                    print(f"   📊 {table_name}: {columns_count} cột, vị trí {bbox}, kích thước {size}")
                    print(f"      📄 Cột riêng: {len(table_info['individual_files'])}")
                    print(f"      📄 Cột gộp: {len(table_info['merged_files'])}")
                
            else:
                print(f"❌ Lỗi xử lý {image_file.name}: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            logger.error(f"Lỗi khi xử lý {image_file.name}: {str(e)}")
            print(f"❌ Lỗi: {str(e)}")
    
    # Tổng kết
    print(f"\n🎉 TỔNG KẾT")
    print("=" * 50)
    print(f"📷 Tổng số ảnh xử lý: {len(image_files)}")
    print(f"📊 Tổng số bảng trích xuất: {total_tables}")
    print(f"📁 Tổng số cột trích xuất: {total_columns}")
    print(f"📂 Kết quả lưu tại:")
    print(f"   📁 Cột riêng: {output_dir}/individual_columns/")
    print(f"   📁 Cột gộp: {output_dir}/merged_columns/")
    print(f"   🔧 Debug: {debug_dir}/")
    
    # Hiển thị một số file kết quả
    individual_dir = Path(output_dir) / "individual_columns"
    merged_dir = Path(output_dir) / "merged_columns"
    
    if individual_dir.exists():
        individual_files = list(individual_dir.glob("*.jpg"))
        if individual_files:
            print(f"\n📁 Ví dụ file cột riêng (hiển thị tối đa 5):")
            for i, f in enumerate(individual_files[:5]):
                print(f"   {i+1}. {f.name}")
    
    if merged_dir.exists():
        merged_files = list(merged_dir.glob("*.jpg"))
        if merged_files:
            print(f"\n📁 Ví dụ file cột gộp (hiển thị tối đa 5):")
            for i, f in enumerate(merged_files[:5]):
                print(f"   {i+1}. {f.name}")

if __name__ == "__main__":
    main()