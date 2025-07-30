#!/usr/bin/env python3
"""
Demo trich xuat cot tu bang - Phien ban don gian
===============================================

Phien ban don gian khong co emoji de tranh loi encoding tren Windows
"""

import os
import sys
import logging
from pathlib import Path

# Thêm thư mục gốc vào Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from detect_row.advanced_column_extractor import AdvancedColumnExtractor

def setup_logging():
    """Thiết lập logging đơn giản"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('column_extraction.log', encoding='utf-8')
        ]
    )

def main():
    """Hàm chính demo"""
    
    # Thiết lập logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    print("Demo Trich Xuat Cot Tu Bang")
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
    print(f"Khoi tao AdvancedColumnExtractor...")
    print(f"   Input: {input_dir}")
    print(f"   Output: {output_dir}")
    print(f"   Debug: {debug_dir}")
    
    extractor = AdvancedColumnExtractor(
        input_dir=input_dir,
        output_dir=output_dir,
        debug_dir=debug_dir,
        min_column_width=30
    )
    
    # Định nghĩa nhóm cột cần gộp
    column_groups = {
        "first_two": [1, 2],
        "third": [3],
        "fourth": [4],
        "last_columns": [5, 6, 7]
    }
    
    print(f"Cau hinh nhom cot:")
    for group_name, columns in column_groups.items():
        print(f"   {group_name}: cot {columns}")
    
    # Tìm tất cả file ảnh trong thư mục input
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    input_path = Path(input_dir)
    
    image_files = []
    for ext in image_extensions:
        image_files.extend(input_path.glob(f'*{ext}'))
        image_files.extend(input_path.glob(f'*{ext.upper()}'))
    
    if not image_files:
        print(f"Khong tim thay file anh nao trong thu muc {input_dir}")
        print(f"   Ho tro cac dinh dang: {', '.join(image_extensions)}")
        return
    
    print(f"Tim thay {len(image_files)} file anh:")
    for img_file in image_files:
        print(f"   {img_file.name}")
    
    # Xử lý từng ảnh
    total_tables = 0
    total_columns = 0
    
    for image_file in image_files:
        print(f"\nXu ly anh: {image_file.name}")
        print("-" * 30)
        
        try:
            # Xử lý ảnh với tối đa 3 bảng
            result = extractor.process_image(
                image_path=image_file.name,
                save_individual=True,
                column_groups=column_groups,
                max_tables=3
            )
            
            if result["success"]:
                tables_processed = result["tables_processed"]
                individual_files = len(result["individual_files"])
                merged_files = len(result["merged_files"])
                
                total_tables += tables_processed
                total_columns += individual_files
                
                print(f"Ket qua xu ly {image_file.name}:")
                print(f"   So bang xu ly: {tables_processed}")
                print(f"   File cot rieng: {individual_files}")
                print(f"   File cot gop: {merged_files}")
                
                # Chi tiết từng bảng
                for table_info in result["tables_info"]:
                    table_name = table_info["table_name"]
                    columns_count = table_info["columns_count"]
                    bbox = table_info["bbox"]
                    size = table_info["cropped_size"]
                    
                    print(f"   {table_name}: {columns_count} cot, vi tri {bbox}, kich thuoc {size}")
                    print(f"      Cot rieng: {len(table_info['individual_files'])}")
                    print(f"      Cot gop: {len(table_info['merged_files'])}")
                
            else:
                print(f"Loi xu ly {image_file.name}: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            logger.error(f"Loi khi xu ly {image_file.name}: {str(e)}")
            print(f"Loi: {str(e)}")
    
    # Tổng kết
    print(f"\nTONG KET")
    print("=" * 50)
    print(f"Tong so anh xu ly: {len(image_files)}")
    print(f"Tong so bang trich xuat: {total_tables}")
    print(f"Tong so cot trich xuat: {total_columns}")
    print(f"Ket qua luu tai:")
    print(f"   Cot rieng: {output_dir}/individual_columns/")
    print(f"   Cot gop: {output_dir}/merged_columns/")
    print(f"   Debug: {debug_dir}/")
    
    # Hiển thị một số file kết quả
    individual_dir = Path(output_dir) / "individual_columns"
    merged_dir = Path(output_dir) / "merged_columns"
    
    if individual_dir.exists():
        individual_files = list(individual_dir.glob("*.jpg"))
        if individual_files:
            print(f"\nVi du file cot rieng (hien thi toi da 5):")
            for i, f in enumerate(individual_files[:5]):
                print(f"   {i+1}. {f.name}")
    
    if merged_dir.exists():
        merged_files = list(merged_dir.glob("*.jpg"))
        if merged_files:
            print(f"\nVi du file cot gop (hien thi toi da 5):")
            for i, f in enumerate(merged_files[:5]):
                print(f"   {i+1}. {f.name}")

if __name__ == "__main__":
    main() 