"""
Test AdvancedColumnExtractor với ảnh image064.png
==============================================

Script này test chức năng trích xuất cột từ ảnh image064.png
có vẻ chứa nhiều bảng theo tên thư mục.
"""

import os
import sys
import cv2
import shutil
from pathlib import Path

# Thêm đường dẫn để import detect_row
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from detect_row import AdvancedColumnExtractor

def test_image064():
    print("🚀 Test AdvancedColumnExtractor với image064.png")
    print("=" * 60)
    
    # Đường dẫn ảnh gốc
    original_image_path = r"D:\Scan\1306\mau nhieu bang\image064.png"
    
    # Kiểm tra file tồn tại
    if not os.path.exists(original_image_path):
        print(f"❌ Không tìm thấy file: {original_image_path}")
        print("   Hãy kiểm tra lại đường dẫn.")
        return
    
    print(f"✅ Tìm thấy file: {original_image_path}")
    
    # Tạo thư mục làm việc
    work_dir = "test_image064"
    input_dir = os.path.join(work_dir, "input")
    output_dir = os.path.join(work_dir, "output", "columns")
    debug_dir = os.path.join(work_dir, "debug", "columns")
    
    # Tạo thư mục
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True) 
    os.makedirs(debug_dir, exist_ok=True)
    
    # Copy ảnh vào thư mục input
    target_image_path = os.path.join(input_dir, "image064.png")
    shutil.copy2(original_image_path, target_image_path)
    print(f"📁 Đã copy ảnh vào: {target_image_path}")
    
    # Kiểm tra kích thước ảnh
    image = cv2.imread(target_image_path)
    if image is not None:
        height, width = image.shape[:2]
        print(f"📏 Kích thước ảnh: {width}x{height} pixels")
        
        # Resize nếu ảnh quá lớn (để xử lý nhanh hơn)
        if width > 2000:
            scale = 2000 / width
            new_width = int(width * scale)
            new_height = int(height * scale)
            resized_image = cv2.resize(image, (new_width, new_height))
            
            resized_path = os.path.join(input_dir, "image064_resized.png")
            cv2.imwrite(resized_path, resized_image)
            print(f"🔄 Đã resize ảnh xuống {new_width}x{new_height}: {resized_path}")
            
            # Sử dụng ảnh đã resize
            image_filename = "image064_resized.png"
        else:
            image_filename = "image064.png"
    else:
        print("❌ Không thể đọc ảnh")
        return
    
    # Khởi tạo AdvancedColumnExtractor
    print(f"\n🔧 Khởi tạo AdvancedColumnExtractor...")
    extractor = AdvancedColumnExtractor(
        input_dir=input_dir,
        output_dir=output_dir,
        debug_dir=debug_dir,
        min_column_width=20  # Giảm xuống 20px cho ảnh có thể có cột nhỏ
    )
    
    # Định nghĩa nhóm cột theo yêu cầu ban đầu
    column_groups = {
        "cols_1_2": [1, 2],  # Cột 1 và 2 gộp thành 1 file  
        "col_3": [3],        # Cột 3 thành file riêng
        "col_4": [4],        # Cột 4 thành file riêng
        "col_5": [5],        # Thêm cột 5 nếu có
        "col_6": [6]         # Thêm cột 6 nếu có
    }
    
    print(f"📊 Cấu hình nhóm cột:")
    for group_name, columns in column_groups.items():
        print(f"   {group_name}: Cột {', '.join(map(str, columns))}")
    
    print(f"\n🔍 Bắt đầu xử lý ảnh: {image_filename}")
    print("-" * 40)
    
    try:
        # Xử lý ảnh
        result = extractor.process_image(
            image_filename,
            save_individual=True,        # Lưu từng cột riêng biệt
            column_groups=column_groups  # Gộp cột theo yêu cầu
        )
        
        # Hiển thị kết quả
        if result["success"]:
            print(f"\n✅ XỬ LÝ THÀNH CÔNG!")
            print(f"📊 Số bảng được xử lý: {result['tables_processed']}")
            print(f"📁 Số file cột riêng: {len(result['individual_files'])}")
            print(f"📁 Số file cột gộp: {len(result['merged_files'])}")
            
            # Hiển thị chi tiết từng bảng
            for i, table_info in enumerate(result["tables_info"]):
                print(f"\n🗂️  BẢNG {i+1}: {table_info['table_name']}")
                print(f"   📍 Vị trí: x={table_info['bbox'][0]}, y={table_info['bbox'][1]}")
                print(f"   📏 Kích thước: {table_info['bbox'][2]}x{table_info['bbox'][3]}px")
                print(f"   📊 Số cột: {table_info['columns_count']}")
                
                # Hiển thị file cột riêng
                if table_info["individual_files"]:
                    print(f"   📄 File cột riêng:")
                    for file_path in table_info["individual_files"]:
                        filename = os.path.basename(file_path)
                        print(f"      • {filename}")
                
                # Hiển thị file cột gộp
                if table_info["merged_files"]:
                    print(f"   📄 File cột gộp:")
                    for file_path in table_info["merged_files"]:
                        filename = os.path.basename(file_path)
                        print(f"      • {filename}")
            
            # Hiển thị đường dẫn kết quả
            print(f"\n📂 KẾT QUẢ ĐƯỢC LƯU TẠI:")
            print(f"   📁 Cột riêng biệt: {os.path.join(output_dir, 'individual_columns')}")
            print(f"   📁 Cột đã gộp: {os.path.join(output_dir, 'merged_columns')}")
            print(f"   📁 Debug: {debug_dir}")
            
            # Liệt kê tất cả file đã tạo
            print(f"\n📋 DANH SÁCH FILE ĐÃ TẠO:")
            all_files = result['individual_files'] + result['merged_files']
            for file_path in sorted(all_files):
                rel_path = os.path.relpath(file_path, work_dir)
                print(f"   📄 {rel_path}")
            
            # Kiểm tra debug files
            print(f"\n🐛 DEBUG FILES:")
            debug_files = [
                "preprocessed.jpg",
                "vertical_lines_original.jpg", 
                "vertical_lines_filtered.jpg",
                "detected_vertical_lines.jpg",
                "v_projection.png"
            ]
            
            for debug_file in debug_files:
                debug_path = os.path.join(debug_dir, debug_file)
                if os.path.exists(debug_path):
                    print(f"   ✅ {debug_file}")
                else:
                    print(f"   ❌ {debug_file} (chưa tạo)")
                    
        else:
            print(f"\n❌ XỬ LÝ THẤT BẠI!")
            print(f"🔍 Lỗi: {result.get('error', 'Unknown error')}")
            
            # Gợi ý debug
            print(f"\n💡 GỢI Ý DEBUG:")
            print(f"   1. Kiểm tra ảnh debug trong: {debug_dir}")
            print(f"   2. Xem file 'preprocessed.jpg' để kiểm tra tiền xử lý")
            print(f"   3. Thử giảm min_column_width xuống 10-15px")
            print(f"   4. Thử tăng min_line_length_ratio lên 0.6-0.8")
            
    except Exception as e:
        print(f"\n❌ LỖI EXCEPTION: {str(e)}")
        import traceback
        traceback.print_exc()
        
    print(f"\n🏁 HOÀN THÀNH TEST VỚI image064.png")

def show_debug_info():
    """Hiển thị thông tin debug để điều chỉnh tham số"""
    print(f"\n🔧 THAM SỐ CÓ THỂ ĐIỀU CHỈNH:")
    print(f"   • min_column_width: Chiều rộng tối thiểu cột (mặc định: 30px)")
    print(f"   • min_line_length_ratio: Tỷ lệ độ dài đường kẻ (mặc định: 0.4)")
    print(f"   • Threshold histogram: Ngưỡng phát hiện đỉnh (mặc định: 40%)")
    print(f"\n🐛 CÁCH DEBUG:")
    print(f"   1. Xem 'preprocessed.jpg' - ảnh đã tiền xử lý")
    print(f"   2. Xem 'vertical_lines_filtered.jpg' - đường kẻ đã lọc") 
    print(f"   3. Xem 'detected_vertical_lines.jpg' - đường kẻ đã phát hiện")
    print(f"   4. Xem 'v_projection.png' - histogram projection")

if __name__ == "__main__":
    test_image064()
    show_debug_info() 