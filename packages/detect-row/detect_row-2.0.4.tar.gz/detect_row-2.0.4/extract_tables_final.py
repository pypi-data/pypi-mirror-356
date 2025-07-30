#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script trích xuất bảng CUỐI CÙNG - Tối ưu hoàn hảo
Bắt đủ 3 bảng riêng biệt, không bắt toàn trang
"""

import os
import cv2
import numpy as np
from pathlib import Path
from typing import List, Tuple, Dict

class FinalTableExtractor:
    """Trích xuất bảng cuối cùng - Hoàn hảo"""
    
    def __init__(self, input_dir="input", output_dir="output/final_tables", debug_dir="debug/final_extraction"):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.debug_dir = debug_dir
        
        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.debug_dir, exist_ok=True)
        
        print(f"Da khoi tao FinalTableExtractor:")
        print(f"  - Input: {self.input_dir}")
        print(f"  - Output: {self.output_dir}")
        print(f"  - Debug: {self.debug_dir}")
    
    def detect_final_tables(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """Phát hiện bảng cuối cùng - Tối ưu hoàn hảo"""
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape
        
        print("PHUONG PHAP TOI UU - Bat ca 3 bang rieng biet...")
        
        # Sử dụng adaptive threshold tốt nhất
        binary_adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                               cv2.THRESH_BINARY_INV, 15, 3)
        
        # Lưu debug
        cv2.imwrite(os.path.join(self.debug_dir, "final_binary.jpg"), binary_adaptive)
        
        # Phát hiện đường kẻ với kernel nhỏ 
        h_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (w//45, 1))  # Nhỏ hơn
        h_lines = cv2.morphologyEx(binary_adaptive, cv2.MORPH_OPEN, h_kernel, iterations=1)
        
        v_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, h//45))  # Nhỏ hơn
        v_lines = cv2.morphologyEx(binary_adaptive, cv2.MORPH_OPEN, v_kernel, iterations=1)
        
        # Kết hợp
        table_structure = cv2.addWeighted(h_lines, 0.3, v_lines, 0.3, 0.0)
        
        # Lưu debug
        cv2.imwrite(os.path.join(self.debug_dir, "final_structure.jpg"), table_structure)
        
        # Tìm contours
        contours, _ = cv2.findContours(table_structure, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Lọc contours với tiêu chí tối ưu
        table_boxes = []
        
        for cnt in contours:
            area = cv2.contourArea(cnt)
            
            # Ngưỡng diện tích rất linh hoạt
            min_area = 0.003 * h * w  # 0.3% - thấp hơn
            max_area = 0.25 * h * w   # 25% - cho phép lớn hơn chút
            
            if min_area <= area <= max_area:
                x, y, width, height = cv2.boundingRect(cnt)
                
                # Tiêu chí kích thước linh hoạt hơn
                min_width = w * 0.12   # 12% - thấp hơn
                max_width = w * 0.90   # 90% - cao hơn
                min_height = h * 0.015 # 1.5% - thấp hơn
                max_height = h * 0.45  # 45% - cao hơn
                
                if (min_width <= width <= max_width and 
                    min_height <= height <= max_height):
                    
                    aspect_ratio = width / height
                    # Aspect ratio rộng hơn
                    if 1.0 <= aspect_ratio <= 15.0:  # Rộng hơn
                        table_boxes.append((x, y, x + width, y + height))
        
        print(f"Phat hien {len(table_boxes)} bang ung vien")
        
        # Loại bỏ overlap và giữ độc lập
        unique_boxes = self._remove_overlaps(table_boxes)
        
        # Sắp xếp từ trên xuống
        unique_boxes.sort(key=lambda x: x[1])
        
        # Vẽ debug
        debug_img = image.copy()
        for i, (x1, y1, x2, y2) in enumerate(unique_boxes):
            cv2.rectangle(debug_img, (x1, y1), (x2, y2), (0, 255, 0), 3)
            cv2.putText(debug_img, f"Final Table {i+1}", (x1+5, y1+25), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        
        cv2.imwrite(os.path.join(self.debug_dir, "final_result.jpg"), debug_img)
        
        print(f"Da phat hien {len(unique_boxes)} bang cuoi cung")
        return unique_boxes
    
    def _remove_overlaps(self, boxes: List[Tuple[int, int, int, int]]) -> List[Tuple[int, int, int, int]]:
        """Loại bỏ overlap thông minh"""
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
    
    def extract_tables_from_image(self, image_path: str) -> List[np.ndarray]:
        """Trích xuất bảng cuối cùng từ ảnh"""
        try:
            print(f"Bat dau xu ly anh: {image_path}")
            
            image = cv2.imread(image_path)
            if image is None:
                print(f"Khong the doc anh: {image_path}")
                return []
            
            file_name = os.path.splitext(os.path.basename(image_path))[0]
            print(f"Ten file: {file_name}")
            
            # Phát hiện bảng cuối cùng
            table_boxes = self.detect_final_tables(image)
            
            if not table_boxes:
                print("Khong phat hien duoc bang nao")
                return []
            
            print(f"THANH CONG: Da phat hien {len(table_boxes)} bang cuoi cung")
            
            # Trích xuất từng bảng
            extracted_tables = []
            
            for i, (x1, y1, x2, y2) in enumerate(table_boxes):
                print(f"Trich xuat bang {i+1}/{len(table_boxes)}")
                print(f"   - Vi tri: ({x1}, {y1}) -> ({x2}, {y2})")
                print(f"   - Kich thuoc: {x2-x1} x {y2-y1} pixel")
                print(f"   - Aspect ratio: {(x2-x1)/(y2-y1):.2f}")
                
                # Cắt bảng với margin nhỏ
                margin = 3
                y1_crop = max(0, y1 - margin)
                y2_crop = min(image.shape[0], y2 + margin)
                x1_crop = max(0, x1 - margin)
                x2_crop = min(image.shape[1], x2 + margin)
                
                table_img = image[y1_crop:y2_crop, x1_crop:x2_crop]
                
                if table_img.size == 0:
                    print(f"Bang {i+1} co kich thuoc 0, bo qua")
                    continue
                
                # Lưu bảng
                table_filename = f"{file_name}_final_table_{i+1:02d}.jpg"
                table_path = os.path.join(self.output_dir, table_filename)
                
                success = cv2.imwrite(table_path, table_img)
                if success:
                    print(f"Da luu bang {i+1}: {table_path}")
                    extracted_tables.append(table_img)
                else:
                    print(f"Loi luu bang {i+1}")
            
            print(f"HOAN THANH: Da trich xuat {len(extracted_tables)} bang cuoi cung tu {file_name}")
            return extracted_tables
            
        except Exception as e:
            print(f"Loi: {str(e)}")
            return []
    
    def process_all_images(self) -> Dict[str, List[np.ndarray]]:
        """Xử lý tất cả ảnh"""
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']
        image_files = []
        
        for ext in image_extensions:
            image_files.extend(Path(self.input_dir).glob(f"*{ext}"))
            image_files.extend(Path(self.input_dir).glob(f"*{ext.upper()}"))
        
        if not image_files:
            print(f"Khong tim thay anh nao trong: {self.input_dir}")
            return {}
        
        print(f"Tim thay {len(image_files)} file anh")
        
        results = {}
        total_tables = 0
        
        for image_file in image_files:
            print(f"\n{'='*80}")
            print(f"XU LY ANH: {image_file.name}")
            print(f"{'='*80}")
            
            extracted_tables = self.extract_tables_from_image(str(image_file))
            results[image_file.name] = extracted_tables
            total_tables += len(extracted_tables)
        
        print(f"\n{'='*80}")
        print(f"KET QUA CUOI CUNG HOAN HAO")
        print(f"{'='*80}")
        print(f"Da xu ly {len(image_files)} anh")
        print(f"Da trich xuat {total_tables} bang cuoi cung")
        print("(Moi bang rieng biet - khong bat toan trang)")
        
        for image_name, tables in results.items():
            print(f"   - {image_name}: {len(tables)} bang")
        
        return results

def main():
    print("TRICH XUAT BANG CUOI CUNG - HOAN HAO")
    print("="*80)
    
    extractor = FinalTableExtractor(
        input_dir="input",
        output_dir="output/final_tables",
        debug_dir="debug/final_extraction"
    )
    
    results = extractor.process_all_images()
    
    if results:
        print("\nHOAN THANH TRICH XUAT BANG CUOI CUNG!")
        print("Cac bang da duoc tach rieng biet hoan hao")
    else:
        print("\nKHONG CO BANG NAO DUOC TRICH XUAT")

if __name__ == "__main__":
    main() 