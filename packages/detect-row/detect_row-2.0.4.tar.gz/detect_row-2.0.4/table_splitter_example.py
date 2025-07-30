#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TABLE SPLITTER EXAMPLE
======================

Code mẫu để split 1 bảng 4 cột thành 2 bảng:
- Bảng 1: Cột 1 + 2 + 3 (STT + Họ tên + Đồng ý)
- Bảng 2: Cột 1 + 2 + 4 (STT + Họ tên + Không đồng ý)

Input:  table_input.jpg (4 cột)
Output: table_dong_y.jpg (3 cột), table_khong_dong_y.jpg (3 cột)
"""

import cv2
import numpy as np
from PIL import Image
import os
from scipy import signal
from scipy.ndimage import gaussian_filter1d
from typing import Tuple, List, Optional
from itertools import combinations

class TableSplitter:
    def __init__(self, input_path: str, output_dir: str = "output"):
        """
        Khởi tạo Table Splitter
        
        Args:
            input_path (str): Đường dẫn file ảnh bảng input (4 cột)
            output_dir (str): Thư mục lưu kết quả
        """
        self.input_path = input_path
        self.output_dir = output_dir
        self.img = None
        self.gray = None
        self.height = 0
        self.width = 0
        
        # Tạo thư mục output
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
    def load_and_validate_image(self) -> bool:
        """
        Load ảnh và validate
        
        Returns:
            bool: True nếu load thành công
        """
        print(f"📂 Đang load ảnh: {self.input_path}")
        
        if not os.path.exists(self.input_path):
            print(f"❌ Không tìm thấy file: {self.input_path}")
            return False
            
        self.img = cv2.imread(self.input_path)
        if self.img is None:
            print(f"❌ Không thể đọc ảnh từ {self.input_path}")
            return False
        
        self.height, self.width = self.img.shape[:2]
        self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        
        print(f"✅ Load thành công! Kích thước: {self.width} x {self.height}")
        return True
        
    def preprocess_image(self) -> np.ndarray:
        """
        Tiền xử lý ảnh để detect cột tốt hơn
        
        Returns:
            np.ndarray: Ảnh binary đã xử lý
        """
        print("🔧 Đang tiền xử lý ảnh...")
        
        # Blur để giảm noise
        blurred = cv2.GaussianBlur(self.gray, (3, 3), 0)
        
        # Tăng contrast
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(blurred)
        
        # Threshold adaptive
        binary = cv2.adaptiveThreshold(enhanced, 255, 
                                     cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY_INV, 15, 2)
        
        print("✅ Tiền xử lý hoàn thành")
        return binary
    
    def detect_column_separators(self, binary: np.ndarray) -> List[int]:
        """
        Detect 3 đường phân cách cột (để tạo 4 cột)
        Sử dụng 4 phương pháp kết hợp
        
        Args:
            binary: Ảnh binary
            
        Returns:
            List[int]: 3 vị trí x của đường phân cách
        """
        print("🔍 Đang detect cột...")
        
        # Method 1: Hough Lines
        hough_lines = self._detect_hough_lines(binary)
        
        # Method 2: Vertical Projection
        projection_peaks = self._detect_projection_peaks(binary)
        
        # Method 3: Morphological
        morph_lines = self._detect_morphological_lines(binary)
        
        # Method 4: Text Gaps
        text_gaps = self._detect_text_gaps(binary)
        
        print(f"  🔍 Hough lines: {hough_lines}")
        print(f"  📊 Projection peaks: {projection_peaks}")
        print(f"  🔲 Morphological lines: {morph_lines}")
        print(f"  📝 Text gaps: {text_gaps}")
        
        # Combine results với weighted approach
        candidates = self._combine_weighted(hough_lines, projection_peaks, 
                                          morph_lines, text_gaps)
        
        # Optimize để có đúng 3 vị trí
        final_positions = self._optimize_positions(candidates)
        
        print(f"✅ Vị trí cột cuối cùng: {final_positions}")
        return final_positions
    
    def _detect_hough_lines(self, binary: np.ndarray) -> List[int]:
        """Detect đường thẳng dọc bằng Hough Transform"""
        edges = cv2.Canny(binary, 50, 150, apertureSize=3)
        lines = cv2.HoughLines(edges, 1, np.pi/180, threshold=int(self.height*0.3))
        
        vertical_lines = []
        if lines is not None:
            for rho, theta in lines[:, 0]:
                if abs(theta) < 0.1 or abs(theta - np.pi) < 0.1:
                    x = int(rho / np.cos(theta)) if abs(np.cos(theta)) > 0.01 else None
                    if x is not None and 10 < x < self.width - 10:
                        vertical_lines.append(x)
        
        return sorted(list(set(vertical_lines)))
    
    def _detect_projection_peaks(self, binary: np.ndarray) -> List[int]:
        """Detect peaks trong vertical projection"""
        projection = np.sum(binary, axis=0)
        smoothed = gaussian_filter1d(projection, sigma=2)
        
        median_val = np.median(smoothed)
        mad = np.median(np.abs(smoothed - median_val))
        threshold = median_val + 2 * mad
        
        peaks, _ = signal.find_peaks(smoothed, 
                                   height=threshold,
                                   distance=max(20, self.width//20),
                                   prominence=mad)
        
        return peaks.tolist()
    
    def _detect_morphological_lines(self, binary: np.ndarray) -> List[int]:
        """Detect đường kẻ bằng morphological operations"""
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, self.height//10))
        vertical_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, vertical_kernel)
        
        contours, _ = cv2.findContours(vertical_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        line_positions = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if h > self.height * 0.5 and w <= 10:
                line_positions.append(x + w//2)
        
        return sorted(line_positions)
    
    def _detect_text_gaps(self, binary: np.ndarray) -> List[int]:
        """Detect gaps giữa text regions"""
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (self.width//50, 1))
        dilated = cv2.dilate(binary, horizontal_kernel, iterations=2)
        
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        text_regions = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w > 30 and h > 10:
                text_regions.append((x, x + w))
        
        text_regions.sort()
        gaps = []
        
        if len(text_regions) > 1:
            for i in range(len(text_regions) - 1):
                gap_start = text_regions[i][1]
                gap_end = text_regions[i + 1][0]
                if gap_end - gap_start > 10:
                    gaps.append((gap_start + gap_end) // 2)
        
        return gaps
    
    def _combine_weighted(self, hough: List[int], projection: List[int], 
                         morph: List[int], text: List[int]) -> List[int]:
        """Combine kết quả với trọng số"""
        all_candidates = []
        
        # Weighted contribution
        for line in hough:
            all_candidates.extend([line] * 3)  # Weight 3
        for peak in projection:
            all_candidates.extend([peak] * 2)  # Weight 2
        for line in morph:
            all_candidates.extend([line] * 2)  # Weight 2
        for gap in text:
            all_candidates.append(gap)         # Weight 1
        
        if not all_candidates:
            raise RuntimeError("❌ Không detect được cột nào!")
        
        # Clustering
        all_candidates.sort()
        clusters = []
        current_cluster = [all_candidates[0]]
        
        for candidate in all_candidates[1:]:
            if candidate - current_cluster[-1] <= 15:
                current_cluster.append(candidate)
            else:
                clusters.append(int(np.mean(current_cluster)))
                current_cluster = [candidate]
        
        if current_cluster:
            clusters.append(int(np.mean(current_cluster)))
        
        # Filter biên
        clusters = [c for c in clusters if 20 < c < self.width - 20]
        return sorted(clusters)
    
    def _optimize_positions(self, candidates: List[int]) -> List[int]:
        """Optimize để có đúng 3 vị trí tạo 4 cột cân đối"""
        if len(candidates) < 3:
            raise RuntimeError(f"❌ Chỉ detect được {len(candidates)} cột, cần ít nhất 3!")
        
        if len(candidates) == 3:
            return candidates
        
        # Chọn 3 vị trí tối ưu bằng CV minimization
        best_score = float('inf')
        best_positions = candidates[:3]
        
        for combo in combinations(candidates, 3):
            combo = sorted(combo)
            
            # Tính 4 sections
            sections = [
                combo[0],                    # Section 1
                combo[1] - combo[0],         # Section 2
                combo[2] - combo[1],         # Section 3
                self.width - combo[2]        # Section 4
            ]
            
            # Coefficient of variation
            mean_section = np.mean(sections)
            std_section = np.std(sections)
            cv = std_section / mean_section if mean_section > 0 else float('inf')
            
            if cv < best_score:
                best_score = cv
                best_positions = combo
        
        print(f"  🎯 Optimization CV score: {best_score:.3f}")
        return list(best_positions)
    
    def create_debug_visualization(self, column_positions: List[int]) -> str:
        """Tạo ảnh debug để kiểm tra"""
        debug_img = self.img.copy()
        
        # Vẽ 3 đường phân cách
        colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255)]  # Green, Blue, Red
        for i, pos in enumerate(column_positions):
            color = colors[i]
            cv2.line(debug_img, (pos, 0), (pos, self.height), color, 3)
            cv2.putText(debug_img, f"Sep {i+1}: {pos}", 
                       (pos + 5, 30 + i*25), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.7, color, 2)
        
        # Hiển thị 4 sections
        sections = [
            column_positions[0],
            column_positions[1] - column_positions[0],
            column_positions[2] - column_positions[1], 
            self.width - column_positions[2]
        ]
        
        cv2.putText(debug_img, f"4 Sections: {sections}", 
                   (10, self.height - 20), cv2.FONT_HERSHEY_SIMPLEX, 
                   0.6, (255, 255, 255), 2)
        
        debug_path = os.path.join(self.output_dir, "debug_column_detection.jpg")
        cv2.imwrite(debug_path, debug_img)
        
        print(f"💾 Debug ảnh: {debug_path}")
        return debug_path
    
    def split_table(self) -> Tuple[str, str]:
        """
        Main function: Split bảng thành 2 ảnh
        
        Returns:
            Tuple[str, str]: (path_table_1, path_table_2)
        """
        print("🚀 Bắt đầu split bảng...")
        print("=" * 50)
        
        # Step 1: Load ảnh
        if not self.load_and_validate_image():
            raise RuntimeError("❌ Không thể load ảnh!")
        
        # Step 2: Preprocess
        binary = self.preprocess_image()
        
        # Step 3: Detect 3 đường phân cách cột
        column_positions = self.detect_column_separators(binary)
        
        # Step 4: Tạo debug visualization
        debug_path = self.create_debug_visualization(column_positions)
        
        # Step 5: Split thành 2 ảnh
        print("✂️ Đang split ảnh...")
        
        # Convert sang PIL để xử lý
        img_rgb = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img_rgb)
        
        # Tạo Bảng 1: Cột 1 + 2 + 3 (STT + Họ tên + Đồng ý)
        # Crop từ đầu đến vị trí phân cách thứ 3
        table1_pil = pil_img.crop((0, 0, column_positions[2], self.height))
        
        # Tạo Bảng 2: Cột 1 + 2 + 4 (STT + Họ tên + Không đồng ý)
        # Ghép cột 1+2 với cột 4
        left_part = pil_img.crop((0, 0, column_positions[1], self.height))  # Cột 1+2
        right_part = pil_img.crop((column_positions[2], 0, self.width, self.height))  # Cột 4
        
        # Tạo ảnh mới để ghép
        table2_width = column_positions[1] + (self.width - column_positions[2])
        table2_pil = Image.new('RGB', (table2_width, self.height), 'white')
        table2_pil.paste(left_part, (0, 0))
        table2_pil.paste(right_part, (column_positions[1], 0))
        
        # Lưu kết quả
        table1_path = os.path.join(self.output_dir, "table_dong_y.jpg")
        table2_path = os.path.join(self.output_dir, "table_khong_dong_y.jpg")
        
        table1_pil.save(table1_path, quality=95, optimize=True)
        table2_pil.save(table2_path, quality=95, optimize=True)
        
        print(f"✅ Bảng 1 (Cột 1+2+3): {table1_path}")
        print(f"   📊 Kích thước: {table1_pil.size}")
        print(f"✅ Bảng 2 (Cột 1+2+4): {table2_path}")
        print(f"   📊 Kích thước: {table2_pil.size}")
        
        return table1_path, table2_path

def demo_example():
    """
    Hàm demo với ảnh mẫu
    """
    print("🎯 TABLE SPLITTER DEMO")
    print("=" * 40)
    
    # Input file - thay đổi tên file theo ảnh của bạn
    input_file = "table_input.jpg"  # Ảnh bảng 4 cột
    
    # Kiểm tra file input
    if not os.path.exists(input_file):
        print(f"❌ Không tìm thấy: {input_file}")
        print("\n💡 Để test, bạn cần:")
        print("   1. Đặt file ảnh bảng 4 cột vào thư mục này")
        print("   2. Đổi tên thành 'table_input.jpg' hoặc sửa tên trong code")
        print("   3. Chạy lại script")
        print("\n📋 Format bảng cần:")
        print("   Cột 1: STT")
        print("   Cột 2: Họ và Tên") 
        print("   Cột 3: Đồng ý")
        print("   Cột 4: Không đồng ý")
        return
    
    try:
        # Khởi tạo và chạy
        splitter = TableSplitter(input_file, output_dir="split_output")
        
        # Split bảng
        table1_path, table2_path = splitter.split_table()
        
        print("\n🎉 HOÀN THÀNH!")
        print("=" * 40)
        print(f"📂 Thư mục output: split_output/")
        print(f"📄 Bảng 1 (STT + Họ tên + Đồng ý): {table1_path}")
        print(f"📄 Bảng 2 (STT + Họ tên + Không đồng ý): {table2_path}")
        print(f"🔍 Debug ảnh: split_output/debug_column_detection.jpg")
        
        # Hướng dẫn sử dụng tiếp
        print("\n💡 Bạn có thể:")
        print("   - Kiểm tra debug ảnh để xem detect có chính xác không")
        print("   - Sử dụng 2 ảnh kết quả cho mục đích khác")
        print("   - Chỉnh sửa code để phù hợp với format bảng khác")
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        print("\n🔧 Có thể khắc phục:")
        print("   - Kiểm tra chất lượng ảnh input")
        print("   - Đảm bảo ảnh có đường kẻ rõ ràng")
        print("   - Thử với ảnh có độ phân giải cao hơn")

def custom_split_example():
    """
    Ví dụ sử dụng với custom input/output paths
    """
    print("\n🛠️ CUSTOM EXAMPLE")
    print("=" * 30)
    
    # Custom paths
    input_path = "my_table.png"      # Đường dẫn ảnh của bạn
    output_dir = "my_results"        # Thư mục lưu kết quả
    
    if os.path.exists(input_path):
        try:
            splitter = TableSplitter(input_path, output_dir)
            table1, table2 = splitter.split_table()
            print(f"✅ Success: {table1}, {table2}")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print(f"ℹ️ File không tồn tại: {input_path}")
        print("   Đây chỉ là ví dụ code")

if __name__ == "__main__":
    # Chạy demo
    demo_example()
    
    # Uncomment để test custom
    # custom_split_example()
    
    print("\n" + "="*50)
    print("🚀 Code hoàn thành! Sẵn sàng sử dụng!")
    print("="*50) 