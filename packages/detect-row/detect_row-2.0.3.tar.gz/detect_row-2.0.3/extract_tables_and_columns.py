"""
Tách riêng từng bảng và trích xuất cột cho mỗi bảng
=================================================

Script này thực hiện:
1. Tìm và crop từng bảng riêng biệt từ ảnh gốc
2. Lưu từng bảng thành file riêng 
3. Với mỗi bảng đã crop, trích xuất các cột
4. Lưu kết quả theo cấu trúc thư mục rõ ràng
"""

import os
import sys
import cv2
import shutil
import numpy as np
from pathlib import Path

# Thêm đường dẫn để import detect_row
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from detect_row import AdvancedTableExtractor, AdvancedColumnExtractor

class TableAndColumnExtractor:
    """Class để tách bảng và trích xuất cột một cách có tổ chức"""
    
    def __init__(self, 
                 input_dir: str = "input",
                 output_dir: str = "output/tables_and_columns",
                 debug_dir: str = "debug/tables_and_columns"):
        """Khởi tạo extractor
        
        Args:
            input_dir: Thư mục chứa ảnh đầu vào
            output_dir: Thư mục lưu kết quả
            debug_dir: Thư mục lưu debug
        """
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.debug_dir = debug_dir
        
        # Tạo cấu trúc thư mục
        self.setup_directories()
        
        # Khởi tạo các extractor con
        self.table_extractor = AdvancedTableExtractor(
            input_dir=input_dir,
            output_dir=os.path.join(output_dir, "tables"),
            debug_dir=os.path.join(debug_dir, "tables")
        )
        
    def setup_directories(self):
        """Tạo cấu trúc thư mục cần thiết"""
        directories = [
            self.output_dir,
            os.path.join(self.output_dir, "tables"),           # Bảng đã crop
            os.path.join(self.output_dir, "columns"),          # Cột từ tất cả bảng
            self.debug_dir,
            os.path.join(self.debug_dir, "tables"),
            os.path.join(self.debug_dir, "columns")
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def detect_and_filter_tables(self, image: np.ndarray) -> list:
        """Phát hiện bảng sử dụng thuật toán từ extract_tables_final.py (chính xác hơn)
        
        Args:
            image: Ảnh đầu vào
            
        Returns:
            list: Danh sách các bảng đã lọc (x, y, w, h)
        """
        print(f"🔍 Sử dụng thuật toán tối ưu từ extract_tables_final.py...")
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape
        
        print("🚀 THUẬT TOÁN TỐI ƯU - Bắt cả 3 bảng riêng biệt...")
        
        # Sử dụng adaptive threshold tốt nhất từ extract_tables_final.py
        binary_adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                               cv2.THRESH_BINARY_INV, 15, 3)
        
        # Lưu debug
        debug_binary_path = os.path.join(self.debug_dir, "tables", "final_binary.jpg")
        cv2.imwrite(debug_binary_path, binary_adaptive)
        
        # Phát hiện đường kẻ với kernel nhỏ (từ extract_tables_final.py)
        h_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (w//45, 1))  # Nhỏ hơn
        h_lines = cv2.morphologyEx(binary_adaptive, cv2.MORPH_OPEN, h_kernel, iterations=1)
        
        v_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, h//45))  # Nhỏ hơn
        v_lines = cv2.morphologyEx(binary_adaptive, cv2.MORPH_OPEN, v_kernel, iterations=1)
        
        # Kết hợp
        table_structure = cv2.addWeighted(h_lines, 0.3, v_lines, 0.3, 0.0)
        
        # Lưu debug
        debug_structure_path = os.path.join(self.debug_dir, "tables", "final_structure.jpg")
        cv2.imwrite(debug_structure_path, table_structure)
        
        # Tìm contours
        contours, _ = cv2.findContours(table_structure, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Lọc contours với tiêu chí tối ưu từ extract_tables_final.py
        table_boxes = []
        
        for cnt in contours:
            area = cv2.contourArea(cnt)
            
            # Ngưỡng diện tích rất linh hoạt từ extract_tables_final.py
            min_area = 0.003 * h * w  # 0.3% - thấp hơn
            max_area = 0.25 * h * w   # 25% - cho phép lớn hơn chút
            
            if min_area <= area <= max_area:
                x, y, width, height = cv2.boundingRect(cnt)
                
                # Tiêu chí kích thước linh hoạt hơn từ extract_tables_final.py
                min_width = w * 0.12   # 12% - thấp hơn
                max_width = w * 0.90   # 90% - cao hơn
                min_height = h * 0.015 # 1.5% - thấp hơn
                max_height = h * 0.45  # 45% - cao hơn
                
                if (min_width <= width <= max_width and 
                    min_height <= height <= max_height):
                    
                    aspect_ratio = width / height
                    # Aspect ratio rộng hơn từ extract_tables_final.py
                    if 1.0 <= aspect_ratio <= 15.0:  # Rộng hơn
                        table_boxes.append((x, y, x + width, y + height))
        
        print(f"📊 Phát hiện {len(table_boxes)} bảng ứng viên")
        
        # Loại bỏ overlap và giữ độc lập (từ extract_tables_final.py)
        unique_boxes = self._remove_overlaps_final(table_boxes)
        
        # Sắp xếp từ trên xuống
        unique_boxes.sort(key=lambda x: x[1])
        
        # Chuyển đổi format từ (x1,y1,x2,y2) về (x,y,w,h)
        valid_tables = []
        for x1, y1, x2, y2 in unique_boxes:
            valid_tables.append((x1, y1, x2-x1, y2-y1))
        
        # Vẽ debug
        debug_img = image.copy()
        for i, (x, y, w, h) in enumerate(valid_tables):
            cv2.rectangle(debug_img, (x, y), (x+w, y+h), (0, 255, 0), 3)
            cv2.putText(debug_img, f"Final Table {i+1}", (x+5, y+25), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            print(f"✅ Bảng {i+1}: x={x}, y={y}, w={w}, h={h}, ratio={w/h:.2f}")
        
        debug_result_path = os.path.join(self.debug_dir, "tables", "final_result.jpg")
        cv2.imwrite(debug_result_path, debug_img)
        
        print(f"🎯 Đã phát hiện {len(valid_tables)} bảng cuối cùng")
        return valid_tables
    

    def _clean_table_borders(self, table_image: np.ndarray) -> np.ndarray:
        """Làm sạch viền bảng và loại bỏ text xung quanh bằng projection analysis
        
        Args:
            table_image: Ảnh bảng gốc
            
        Returns:
            np.ndarray: Ảnh bảng đã làm sạch
        """
        h, w = table_image.shape[:2]
        gray = cv2.cvtColor(table_image, cv2.COLOR_BGR2GRAY)
        
        # Binary threshold
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Horizontal projection để tìm vùng có nội dung
        h_projection = np.sum(binary, axis=1)
        v_projection = np.sum(binary, axis=0)
        
        # Tìm ngưỡng để loại bỏ vùng sparse (ít nội dung)
        h_threshold = np.mean(h_projection) * 0.3  # 30% trung bình
        v_threshold = np.mean(v_projection) * 0.3
        
        # Tìm vùng content chính (liên tục)
        h_content_rows = np.where(h_projection > h_threshold)[0]
        v_content_cols = np.where(v_projection > v_threshold)[0]
        
        if len(h_content_rows) == 0 or len(v_content_cols) == 0:
            return table_image
        
        # Tìm vùng liên tục lớn nhất
        h_start, h_end = h_content_rows[0], h_content_rows[-1]
        v_start, v_end = v_content_cols[0], v_content_cols[-1]
        
        # Mở rộng một chút để không cắt mất viền
        margin = 5
        h_start = max(0, h_start - margin)
        h_end = min(h, h_end + margin)
        v_start = max(0, v_start - margin)
        v_end = min(w, v_end + margin)
        
        # Crop vùng content chính
        cleaned_table = table_image[h_start:h_end, v_start:v_end]
        
        print(f"   🧹 Làm sạch bảng: {w}x{h} -> {v_end-v_start}x{h_end-h_start}")
        
        return cleaned_table
    
    def _remove_overlaps_final(self, boxes: list) -> list:
        """Loại bỏ overlap thông minh từ extract_tables_final.py"""
        if not boxes:
            return []
        
        unique_boxes = []
        for box in boxes:
            x1, y1, x2, y2 = box
            
            # Kiểm tra overlap với boxes đã có
            is_overlap = False
            for i, existing in enumerate(unique_boxes):
                ex1, ey1, ex2, ey2 = existing
                
                # Tính overlap
                overlap_area = max(0, min(x2, ex2) - max(x1, ex1)) * max(0, min(y2, ey2) - max(y1, ey1))
                box_area = (x2 - x1) * (y2 - y1)
                existing_area = (ex2 - ex1) * (ey2 - ey1)
                
                # Nếu overlap > 30%
                if overlap_area > 0.3 * min(box_area, existing_area):
                    # Giữ box có aspect ratio tốt hơn (gần với bảng thật)
                    box_aspect = (x2 - x1) / (y2 - y1)
                    existing_aspect = (ex2 - ex1) / (ey2 - ey1)
                    
                    # Aspect ratio lý tưởng cho bảng: 2.0 - 6.0
                    box_score = min(abs(box_aspect - 3.0), 3.0)
                    existing_score = min(abs(existing_aspect - 3.0), 3.0)
                    
                    if box_score < existing_score:  # Box mới tốt hơn
                        unique_boxes[i] = box
                    is_overlap = True
                    break
            
            if not is_overlap:
                unique_boxes.append(box)
        
        return unique_boxes
    
    def extract_tables_from_image(self, image_path: str) -> list:
        """Trích xuất và lưu từng bảng riêng biệt với filtered_tables
        
        Args:
            image_path: Đường dẫn ảnh
            
        Returns:
            list: Danh sách thông tin các bảng đã trích xuất
        """
        print(f"🔍 Tìm và tách các bảng từ: {image_path}")
        
        # Đọc ảnh gốc
        full_image_path = os.path.join(self.input_dir, image_path)
        image = cv2.imread(full_image_path)
        
        if image is None:
            print(f"❌ Không thể đọc ảnh: {full_image_path}")
            return []
        
        print(f"📏 Kích thước ảnh gốc: {image.shape[1]}x{image.shape[0]} pixels")
        
        # Sử dụng phương thức filtered tables mới
        tables = self.detect_and_filter_tables(image)
        
        if not tables:
            print("❌ Không phát hiện được bảng nào")
            return []
        
        print(f"📊 Đã phát hiện {len(tables)} bảng sau khi lọc")
        
        # Trích xuất và lưu từng bảng
        extracted_tables = []
        image_name = Path(image_path).stem
        
        for i, (x, y, w, h) in enumerate(tables):
            table_info = {
                'table_index': i,
                'table_name': f"{image_name}_table_{i}",
                'bbox': (x, y, w, h),
                'original_image': image_path
            }
            
            print(f"\n📋 Xử lý bảng {i+1}:")
            print(f"   📍 Vị trí: x={x}, y={y}")
            print(f"   📏 Kích thước: {w}x{h} pixels")
            print(f"   📐 Diện tích: {w*h:,} pixels")
            
            # Crop bảng từ ảnh gốc
            table_image = image[y:y+h, x:x+w]
            
            # Làm sạch bảng - loại bỏ text xung quanh
            cleaned_table = self._clean_table_borders(table_image)
            
            # Lưu bảng đã crop và làm sạch
            table_filename = f"{table_info['table_name']}.jpg"
            table_path = os.path.join(self.output_dir, "tables", table_filename)
            cv2.imwrite(table_path, cleaned_table)
            
            table_info['table_file'] = table_path
            table_info['table_image'] = cleaned_table
            
            print(f"   💾 Đã lưu bảng: {table_filename}")
            
            extracted_tables.append(table_info)
        
        return extracted_tables
    
    def extract_columns_from_table(self, table_info: dict, column_groups: dict = None) -> dict:
        """Trích xuất cột từ một bảng cụ thể
        
        Args:
            table_info: Thông tin bảng
            column_groups: Định nghĩa nhóm cột
            
        Returns:
            dict: Kết quả trích xuất cột
        """
        table_name = table_info['table_name']
        table_image = table_info['table_image']
        
        print(f"\n🔧 Trích xuất cột từ {table_name}...")
        
        # Tạo thư mục riêng cho bảng này
        table_columns_dir = os.path.join(self.output_dir, "columns", table_name)
        table_debug_dir = os.path.join(self.debug_dir, "columns", table_name)
        
        os.makedirs(table_columns_dir, exist_ok=True)
        os.makedirs(table_debug_dir, exist_ok=True)
        
        # Khởi tạo column extractor cho bảng này
        column_extractor = AdvancedColumnExtractor(
            input_dir="temp",  # Không dùng
            output_dir=table_columns_dir,
            debug_dir=table_debug_dir,
            min_column_width=20
        )
        
        # Trích xuất thông tin cột
        columns_info = column_extractor.extract_columns_from_table(table_image, table_name)
        
        if not columns_info:
            print(f"   ❌ Không trích xuất được cột nào từ {table_name}")
            return {"success": False, "columns_count": 0}
        
        print(f"   📊 Đã phát hiện {len(columns_info)} cột")
        
        # Tạo thư mục con
        individual_dir = os.path.join(table_columns_dir, "individual_columns")
        merged_dir = os.path.join(table_columns_dir, "merged_columns")
        os.makedirs(individual_dir, exist_ok=True)
        os.makedirs(merged_dir, exist_ok=True)
        
        # Lưu từng cột riêng biệt
        individual_files = []
        for column_info in columns_info:
            filepath = os.path.join(individual_dir, column_info['filename'])
            cv2.imwrite(filepath, column_info['image'])
            individual_files.append(filepath)
            print(f"   💾 Đã lưu cột {column_info['column_index']}: {column_info['filename']}")
        
        # Lưu cột đã gộp nếu có cấu hình
        merged_files = []
        if column_groups:
            # Cập nhật đường dẫn cho merged files
            temp_extractor = AdvancedColumnExtractor(
                input_dir="temp",
                output_dir=table_columns_dir,
                debug_dir=table_debug_dir
            )
            temp_extractor.merged_columns_dir = merged_dir
            
            merged_files = temp_extractor.save_merged_columns(columns_info, table_name, column_groups)
            
            for file_path in merged_files:
                filename = os.path.basename(file_path)
                print(f"   🔗 Đã gộp: {filename}")
        
        return {
            "success": True,
            "table_name": table_name,
            "columns_count": len(columns_info),
            "individual_files": individual_files,
            "merged_files": merged_files,
            "columns_info": columns_info
        }
    
    def process_image_full_workflow(self, image_path: str, column_groups: dict = None) -> dict:
        """Workflow hoàn chỉnh: tách bảng và trích xuất cột
        
        Args:
            image_path: Đường dẫn ảnh
            column_groups: Định nghĩa nhóm cột
            
        Returns:
            dict: Kết quả toàn bộ quá trình
        """
        print(f"🚀 Bắt đầu workflow hoàn chỉnh cho: {image_path}")
        print("=" * 70)
        
        # Bước 1: Tách các bảng
        extracted_tables = self.extract_tables_from_image(image_path)
        
        if not extracted_tables:
            return {
                "success": False,
                "error": "Không tìm thấy bảng nào",
                "tables_count": 0
            }
        
        print(f"\n✅ Đã tách thành công {len(extracted_tables)} bảng")
        
        # Bước 2: Trích xuất cột từ từng bảng
        tables_results = []
        total_columns = 0
        total_individual_files = 0
        total_merged_files = 0
        
        for table_info in extracted_tables:
            print(f"\n{'='*50}")
            column_result = self.extract_columns_from_table(table_info, column_groups)
            
            if column_result["success"]:
                total_columns += column_result["columns_count"]
                total_individual_files += len(column_result["individual_files"])
                total_merged_files += len(column_result["merged_files"])
            
            tables_results.append(column_result)
        
        # Tổng kết
        result = {
            "success": True,
            "image_path": image_path,
            "tables_count": len(extracted_tables),
            "total_columns": total_columns,
            "total_individual_files": total_individual_files,
            "total_merged_files": total_merged_files,
            "tables_results": tables_results,
            "extracted_tables": extracted_tables
        }
        
        print(f"\n🎉 HOÀN THÀNH WORKFLOW!")
        print(f"📊 Tổng số bảng: {result['tables_count']}")
        print(f"📊 Tổng số cột: {result['total_columns']}")
        print(f"📁 File cột riêng: {result['total_individual_files']}")
        print(f"📁 File cột gộp: {result['total_merged_files']}")
        
        return result
    
    def show_results_summary(self, result: dict):
        """Hiển thị tóm tắt kết quả"""
        if not result["success"]:
            print(f"❌ Lỗi: {result.get('error')}")
            return
        
        print(f"\n📋 TÓM TẮT KẾT QUẢ:")
        print(f"   🖼️  Ảnh gốc: {result['image_path']}")
        print(f"   📊 Số bảng: {result['tables_count']}")
        print(f"   📊 Tổng cột: {result['total_columns']}")
        print(f"   📁 File cột riêng: {result['total_individual_files']}")
        print(f"   📁 File cột gộp: {result['total_merged_files']}")
        
        print(f"\n📂 CẤU TRÚC KẾT QUẢ:")
        print(f"   {self.output_dir}/")
        print(f"   ├── tables/                    # Các bảng đã tách")
        print(f"   └── columns/                   # Cột từ từng bảng")
        
        for table_result in result["tables_results"]:
            if table_result["success"]:
                table_name = table_result["table_name"]
                print(f"       ├── {table_name}/")
                print(f"       │   ├── individual_columns/  # {len(table_result['individual_files'])} file")
                print(f"       │   └── merged_columns/      # {len(table_result['merged_files'])} file")
        
        # Hiển thị danh sách file bảng
        print(f"\n📋 CÁC BẢNG ĐÃ TÁCH:")
        for table_info in result["extracted_tables"]:
            table_file = os.path.basename(table_info["table_file"])
            bbox = table_info["bbox"]
            print(f"   📄 {table_file} (vị trí: {bbox[0]},{bbox[1]} - kích thước: {bbox[2]}x{bbox[3]})")

def parse_column_groups(groups_str: str) -> dict:
    """Parse chuỗi định nghĩa nhóm cột từ command line
    
    Format: group_name:col1,col2,col3;another_group:col1,col4
    Ví dụ: "cols_1_2:1,2;col_3:3;cols_1_2_3:1,2,3"
    
    Args:
        groups_str: Chuỗi định nghĩa nhóm cột
        
    Returns:
        dict: Dictionary các nhóm cột
    """
    if not groups_str:
        return {}
    
    column_groups = {}
    try:
        groups = groups_str.split(';')
        for group in groups:
            if ':' not in group:
                continue
            name, cols = group.split(':', 1)
            name = name.strip()
            col_indices = [int(c.strip()) for c in cols.split(',') if c.strip().isdigit()]
            if name and col_indices:
                column_groups[name] = col_indices
                print(f"📋 Nhóm '{name}': cột {col_indices}")
    except Exception as e:
        print(f"❌ Lỗi parse nhóm cột: {e}")
        return {}
    
    return column_groups

def get_default_column_groups() -> dict:
    """Trả về nhóm cột mặc định"""
    return {
        "cols_1_2": [1, 2],        # Cột 1 và 2 gộp thành 1 file
        "col_3": [3],              # Cột 3 thành file riêng
        "col_4": [4],              # Cột 4 thành file riêng
        "cols_1_2_3": [1, 2, 3],  # Merge cột 1+2 với cột 3
        "cols_1_2_4": [1, 2, 4],  # Merge cột 1+2 với cột 4
        "col_5": [5],              # Cột 5 nếu có
        "col_6": [6]               # Cột 6 nếu có
    }

def show_column_groups_help():
    """Hiển thị hướng dẫn sử dụng nhóm cột"""
    print("🔧 HƯỚNG DẪN SỬ DỤNG NHÓM CỘT:")
    print("=" * 60)
    print("📝 Format: --column-groups 'group_name:col1,col2;another_group:col3'")
    print()
    print("📋 Ví dụ:")
    print("   --column-groups 'cols_1_2:1,2;col_3:3;cols_all:1,2,3,4'")
    print("   --column-groups 'header:1;content:2,3;footer:4'")
    print("   --column-groups 'left_side:1,2;right_side:3,4;full:1,2,3,4'")
    print()
    print("📋 Nhóm mặc định nếu không chỉ định:")
    default_groups = get_default_column_groups()
    for name, cols in default_groups.items():
        print(f"   - {name}: cột {cols}")
    print()
    print("💡 Mẹo:")
    print("   - Tên nhóm chỉ dùng chữ, số và dấu gạch dưới")
    print("   - Số cột bắt đầu từ 1")
    print("   - Dùng dấu ; để phân tách các nhóm")
    print("   - Dùng dấu , để phân tách các cột trong nhóm")

def interactive_column_groups_setup() -> dict:
    """Thiết lập nhóm cột tương tác"""
    print("🎯 THIẾT LẬP NHÓM CỘT TƯƠNG TÁC")
    print("=" * 50)
    print("Nhập các nhóm cột bạn muốn tạo (Enter để kết thúc):")
    print("Format: <tên_nhóm>:<cột1,cột2,...>")
    print("Ví dụ: cols_1_2:1,2")
    print()
    
    column_groups = {}
    while True:
        try:
            user_input = input("👉 Nhập nhóm cột (hoặc Enter để kết thúc): ").strip()
            if not user_input:
                break
            
            if ':' not in user_input:
                print("❌ Format sai! Cần có dấu : để phân tách tên và cột")
                continue
            
            name, cols = user_input.split(':', 1)
            name = name.strip()
            
            try:
                col_indices = [int(c.strip()) for c in cols.split(',') if c.strip().isdigit()]
                if not col_indices:
                    print("❌ Không có cột hợp lệ!")
                    continue
                
                column_groups[name] = col_indices
                print(f"✅ Đã thêm nhóm '{name}': cột {col_indices}")
                
            except ValueError:
                print("❌ Số cột không hợp lệ!")
                
        except KeyboardInterrupt:
            print("\n⏹️ Hủy thiết lập")
            return {}
    
    if column_groups:
        print(f"\n📋 Đã thiết lập {len(column_groups)} nhóm cột:")
        for name, cols in column_groups.items():
            print(f"   - {name}: cột {cols}")
    else:
        print("📋 Sử dụng nhóm cột mặc định")
        column_groups = get_default_column_groups()
    
    return column_groups

def main():
    """Hàm chính với tùy chọn linh hoạt cho nhóm cột"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Tách bảng và trích xuất cột với tùy chọn merge linh hoạt',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ sử dụng:
  %(prog)s image.png                                    # Sử dụng nhóm cột mặc định
  %(prog)s image.png --column-groups "cols_1_2:1,2;col_3:3"  # Tự định nghĩa nhóm cột
  %(prog)s --interactive                                # Thiết lập nhóm cột tương tác
  %(prog)s --help-columns                              # Xem hướng dẫn nhóm cột
        """)
    
    parser.add_argument('image_path', nargs='?', help='Đường dẫn ảnh')
    parser.add_argument('--input-dir', default='input', help='Thư mục chứa ảnh')
    parser.add_argument('--output-dir', default='output/tables_and_columns', help='Thư mục lưu kết quả')
    parser.add_argument('--debug-dir', default='debug/tables_and_columns', help='Thư mục debug')
    
    parser.add_argument('--column-groups', type=str, 
                       help='Định nghĩa nhóm cột (format: group_name:col1,col2;another_group:col3)')
    parser.add_argument('--interactive', action='store_true', 
                       help='Thiết lập nhóm cột tương tác')
    parser.add_argument('--help-columns', action='store_true', 
                       help='Hiển thị hướng dẫn sử dụng nhóm cột')
    parser.add_argument('--no-merge', action='store_true', 
                       help='Chỉ tách cột riêng biệt, không merge')
    
    args = parser.parse_args()
    
    # Hiển thị hướng dẫn nhóm cột
    if args.help_columns:
        show_column_groups_help()
        return
    
    # Khởi tạo extractor
    extractor = TableAndColumnExtractor(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        debug_dir=args.debug_dir
    )
    
    # Xác định nhóm cột
    column_groups = None
    if args.no_merge:
        print("🚫 Chế độ không merge - chỉ tách cột riêng biệt")
        column_groups = {}
    elif args.interactive:
        column_groups = interactive_column_groups_setup()
    elif args.column_groups:
        print("🔧 Sử dụng nhóm cột tự định nghĩa:")
        column_groups = parse_column_groups(args.column_groups)
        if not column_groups:
            print("❌ Nhóm cột không hợp lệ, sử dụng mặc định")
            column_groups = get_default_column_groups()
    else:
        print("🔧 Sử dụng nhóm cột mặc định:")
        column_groups = get_default_column_groups()
        for name, cols in column_groups.items():
            print(f"   📋 {name}: cột {cols}")
    
    print()  # Dòng trống
    
    if args.image_path:
        # Xử lý ảnh cụ thể
        result = extractor.process_image_full_workflow(args.image_path, column_groups)
        extractor.show_results_summary(result)
    else:
        # Xử lý tất cả ảnh trong thư mục input
        image_files = []
        if os.path.exists(args.input_dir):
            for ext in ['*.jpg', '*.jpeg', '*.png', '*.bmp']:
                image_files.extend(Path(args.input_dir).glob(ext))
        
        if not image_files:
            print(f"⚠️ Không tìm thấy ảnh nào trong {args.input_dir}")
            return
        
        for image_file in image_files:
            print(f"\n{'='*80}")
            result = extractor.process_image_full_workflow(image_file.name, column_groups)
            extractor.show_results_summary(result)

if __name__ == "__main__":
    main()