import cv2
import numpy as np
from PIL import Image
import os
from scipy import signal
from scipy.ndimage import gaussian_filter1d
from typing import Tuple, List, Optional

class AutoTableSplitter:
    def __init__(self, input_path: str):
        """
        Khởi tạo AutoTableSplitter
        
        Args:
            input_path (str): Đường dẫn đến file ảnh bảng
        """
        self.input_path = input_path
        self.img = None
        self.gray = None
        self.height = 0
        self.width = 0
        
    def load_image(self) -> None:
        """Tải và chuẩn bị ảnh"""
        self.img = cv2.imread(self.input_path)
        if self.img is None:
            raise ValueError(f"Không thể đọc ảnh từ {self.input_path}")
        
        self.height, self.width = self.img.shape[:2]
        self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        print(f"📐 Kích thước ảnh: {self.width} x {self.height}")
        
    def preprocess_image(self) -> np.ndarray:
        """
        Tiền xử lý ảnh để tăng độ chính xác
        
        Returns:
            np.ndarray: Ảnh nhị phân đã được xử lý
        """
        # Làm mịn để giảm noise
        blurred = cv2.GaussianBlur(self.gray, (3, 3), 0)
        
        # Tăng độ tương phản
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(blurred)
        
        # Threshold adaptive để xử lý ánh sáng không đều
        binary = cv2.adaptiveThreshold(enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                     cv2.THRESH_BINARY_INV, 15, 2)
        
        return binary
    
    def detect_vertical_lines_hough(self, binary: np.ndarray) -> List[int]:
        """
        Phát hiện đường thẳng dọc bằng Hough Transform
        
        Args:
            binary (np.ndarray): Ảnh nhị phân
            
        Returns:
            List[int]: Danh sách vị trí x của các đường thẳng dọc
        """
        # Phát hiện edges
        edges = cv2.Canny(binary, 50, 150, apertureSize=3)
        
        # Hough Line Transform - chỉ tìm đường thẳng dọc
        lines = cv2.HoughLines(edges, 1, np.pi/180, threshold=int(self.height*0.3))
        
        vertical_lines = []
        if lines is not None:
            for rho, theta in lines[:, 0]:
                # Chỉ lấy đường thẳng gần dọc (theta gần 0 hoặc π)
                if abs(theta) < 0.1 or abs(theta - np.pi) < 0.1:
                    x = int(rho / np.cos(theta)) if abs(np.cos(theta)) > 0.01 else None
                    if x is not None and 10 < x < self.width - 10:
                        vertical_lines.append(x)
        
        return sorted(list(set(vertical_lines)))
    
    def analyze_vertical_projection(self, binary: np.ndarray) -> Tuple[List[int], np.ndarray]:
        """
        Phân tích projection dọc với nhiều kỹ thuật
        
        Args:
            binary (np.ndarray): Ảnh nhị phân
            
        Returns:
            Tuple[List[int], np.ndarray]: (danh sách vị trí peaks, projection smoothed)
        """
        # Tính projection cơ bản
        projection = np.sum(binary, axis=0)
        
        # Làm mịn bằng Gaussian filter
        smoothed = gaussian_filter1d(projection, sigma=2)
        
        # Tìm peaks với scipy
        # Tính dynamic threshold
        median_val = np.median(smoothed)
        mad = np.median(np.abs(smoothed - median_val))  # Median Absolute Deviation
        threshold = median_val + 2 * mad
        
        # Tìm peaks
        peaks, properties = signal.find_peaks(smoothed, 
                                            height=threshold,
                                            distance=max(20, self.width//20),
                                            prominence=mad)
        
        return peaks.tolist(), smoothed
    
    def detect_morphological_lines(self, binary: np.ndarray) -> List[int]:
        """
        Phát hiện đường kẻ bằng morphological operations
        
        Args:
            binary (np.ndarray): Ảnh nhị phân
            
        Returns:
            List[int]: Danh sách vị trí x của các đường kẻ dọc
        """
        # Tạo kernel dọc để phát hiện đường kẻ dọc
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, self.height//10))
        
        # Morphological operations
        vertical_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, vertical_kernel)
        
        # Tìm contours của đường kẻ dọc
        contours, _ = cv2.findContours(vertical_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        line_positions = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            # Điều kiện: đường kẻ dọc (cao, hẹp)
            if h > self.height * 0.5 and w <= 10:
                line_positions.append(x + w//2)
        
        return sorted(line_positions)
    
    def find_text_regions(self, binary: np.ndarray) -> List[int]:
        """
        Tìm vùng text để xác định cột
        
        Args:
            binary (np.ndarray): Ảnh nhị phân
            
        Returns:
            List[int]: Danh sách vị trí gaps giữa các vùng text
        """
        # Tạo kernel ngang để nhóm text
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (self.width//50, 1))
        
        # Dilate để nhóm text thành blocks
        dilated = cv2.dilate(binary, horizontal_kernel, iterations=2)
        
        # Tìm contours của text blocks
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        text_regions = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w > 30 and h > 10:  # Filter noise
                text_regions.append((x, x + w))
        
        # Nhóm text regions thành columns
        text_regions.sort()
        
        # Tìm gaps giữa các text regions
        gaps = []
        if len(text_regions) > 1:
            for i in range(len(text_regions) - 1):
                gap_start = text_regions[i][1]
                gap_end = text_regions[i + 1][0]
                if gap_end - gap_start > 10:  # Significant gap
                    gaps.append((gap_start + gap_end) // 2)
        
        return gaps
    
    def combine_detections(self, hough_lines: List[int], projection_peaks: List[int], 
                          morph_lines: List[int], text_gaps: List[int]) -> List[int]:
        """
        Kết hợp kết quả từ các phương pháp khác nhau
        
        Args:
            hough_lines: Kết quả từ Hough Transform
            projection_peaks: Kết quả từ vertical projection
            morph_lines: Kết quả từ morphological operations
            text_gaps: Kết quả từ text region analysis
            
        Returns:
            List[int]: Danh sách vị trí cột đã được cluster
        """
        print(f"🔍 Hough lines: {hough_lines}")
        print(f"🔍 Projection peaks: {projection_peaks}")
        print(f"🔍 Morphological lines: {morph_lines}")
        print(f"🔍 Text gaps: {text_gaps}")
        
        # Tổng hợp tất cả candidates
        all_candidates = []
        
        # Thêm với trọng số khác nhau
        for line in hough_lines:
            all_candidates.extend([line] * 3)  # Trọng số cao
        
        for peak in projection_peaks:
            all_candidates.extend([peak] * 2)  # Trọng số trung bình
            
        for line in morph_lines:
            all_candidates.extend([line] * 2)  # Trọng số trung bình
            
        for gap in text_gaps:
            all_candidates.append(gap)  # Trọng số thấp
        
        if not all_candidates:
            return self.fallback_column_detection()
        
        # Cluster các candidates gần nhau
        all_candidates.sort()
        clusters = []
        current_cluster = [all_candidates[0]]
        
        for candidate in all_candidates[1:]:
            if candidate - current_cluster[-1] <= 15:  # Trong cùng cluster
                current_cluster.append(candidate)
            else:
                # Tính trung bình có trọng số của cluster
                cluster_center = int(np.mean(current_cluster))
                clusters.append(cluster_center)
                current_cluster = [candidate]
        
        # Thêm cluster cuối
        if current_cluster:
            cluster_center = int(np.mean(current_cluster))
            clusters.append(cluster_center)
        
        # Lọc các cluster ở biên
        clusters = [c for c in clusters if 20 < c < self.width - 20]
        
        return sorted(clusters)
    
    def fallback_column_detection(self) -> List[int]:
        """
        Phương pháp dự phòng - trả về lỗi khi không detect được
        
        Raises:
            RuntimeError: Khi không thể phát hiện cấu trúc bảng
        """
        raise RuntimeError(
            "❌ Không thể phát hiện cấu trúc bảng tự động!\n"
            "🔍 Các nguyên nhân có thể:\n"
            "   - Ảnh không rõ nét hoặc bị mờ\n"
            "   - Đường kẻ bảng không rõ ràng\n"
            "   - Định dạng bảng không chuẩn\n"
            "   - Độ tương phản thấp\n"
            "💡 Gợi ý khắc phục:\n"
            "   - Chụp lại ảnh với độ phân giải cao hơn\n"
            "   - Đảm bảo ảnh có đường kẻ rõ ràng\n"
            "   - Tăng độ tương phản của ảnh\n"
            "   - Kiểm tra định dạng bảng có đúng 4 cột không"
        )
    
    def refine_column_positions(self, candidates: List[int]) -> List[int]:
        """
        Tinh chỉnh vị trí cột để có 3 cột chính xác
        
        Args:
            candidates: Danh sách các vị trí cột candidate
            
        Returns:
            List[int]: Danh sách 3 vị trí cột cuối cùng
            
        Raises:
            RuntimeError: Khi không đủ cột để tạo bảng 4 cột
        """
        if len(candidates) == 0:
            raise RuntimeError(
                "❌ Không phát hiện được bất kỳ cột nào!\n"
                "🔍 Vui lòng kiểm tra:\n"
                "   - Ảnh có đường kẻ dọc rõ ràng không?\n"
                "   - Chất lượng ảnh có đủ tốt không?\n"
                "   - Bảng có đúng định dạng 4 cột không?"
            )
        
        if len(candidates) == 1:
            raise RuntimeError(
                "❌ Chỉ phát hiện được 1 cột!\n"
                f"🔍 Vị trí phát hiện: {candidates[0]}\n"
                "💡 Cần ít nhất 2 đường kẻ để tạo 3 cột.\n"
                "   Vui lòng kiểm tra lại ảnh bảng."
            )
        
        if len(candidates) == 2:
            raise RuntimeError(
                "❌ Chỉ phát hiện được 2 cột!\n"
                f"🔍 Vị trí phát hiện: {candidates}\n"
                "💡 Cần ít nhất 3 đường kẻ để tạo 4 cột bảng.\n"
                "   Vui lòng kiểm tra lại chất lượng ảnh."
            )
        
        if len(candidates) == 3:
            return candidates
        else:
            # Nếu có nhiều hơn 3, chọn 3 vị trí tối ưu
            print(f"🔍 Phát hiện {len(candidates)} cột, đang chọn 3 vị trí tối ưu...")
            
            # Ưu tiên chọn những vị trí tạo ra 4 phần cân đối
            best_score = float('inf')
            best_positions = candidates[:3]
            
            # Thử tất cả tổ hợp 3 vị trí
            from itertools import combinations
            for combo in combinations(candidates, 3):
                combo = sorted(combo)
                
                # Tính độ cân đối của 4 phần
                sections = [
                    combo[0],                    # Phần 1
                    combo[1] - combo[0],         # Phần 2  
                    combo[2] - combo[1],         # Phần 3
                    self.width - combo[2]        # Phần 4
                ]
                
                # Tính coefficient of variation (CV)
                mean_section = np.mean(sections)
                std_section = np.std(sections)
                cv = std_section / mean_section if mean_section > 0 else float('inf')
                
                if cv < best_score:
                    best_score = cv
                    best_positions = combo
            
            print(f"🎯 Chọn vị trí tối ưu: {best_positions} (CV: {best_score:.3f})")
            return list(best_positions)
    
    def visualize_detection(self, column_positions: List[int], save_path: str = "debug_detection.png") -> None:
        """
        Vẽ ảnh debug để kiểm tra kết quả
        
        Args:
            column_positions: Danh sách vị trí cột
            save_path: Đường dẫn lưu ảnh debug
        """
        debug_img = self.img.copy()
        
        # Vẽ các đường cột
        for i, pos in enumerate(column_positions):
            color = [(0, 255, 0), (255, 0, 0), (0, 0, 255)][i % 3]
            cv2.line(debug_img, (pos, 0), (pos, self.height), color, 3)
            cv2.putText(debug_img, f"Col {i+1}: {pos}", 
                       (pos + 5, 30 + i*25), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.7, color, 2)
        
        # Hiển thị 4 phần được tạo
        sections = [column_positions[0], 
                   column_positions[1] - column_positions[0],
                   column_positions[2] - column_positions[1], 
                   self.width - column_positions[2]]
        
        cv2.putText(debug_img, f"Sections: {sections}", 
                   (10, self.height - 20), cv2.FONT_HERSHEY_SIMPLEX, 
                   0.6, (255, 255, 255), 2)
        
        cv2.imwrite(save_path, debug_img)
        print(f"💾 Đã lưu ảnh debug: {save_path}")
    
    def split_table(self, output_dir: str = "output") -> Tuple[str, str, List[int], np.ndarray, np.ndarray]:
        """
        Thực hiện tách bảng tự động
        
        Args:
            output_dir (str): Thư mục lưu kết quả. Mặc định là "output"
            
        Returns:
            Tuple[str, str, List[int], np.ndarray, np.ndarray]: 
                - Đường dẫn ảnh 1 (STT + Họ và Tên + Đồng ý)
                - Đường dẫn ảnh 2 (STT + Họ và Tên + Không đồng ý) 
                - Danh sách vị trí cột phát hiện được
                - Ảnh 1 dưới dạng numpy array (BGR)
                - Ảnh 2 dưới dạng numpy array (BGR)
        """
        # Tải và xử lý ảnh
        self.load_image()
        binary = self.preprocess_image()
        
        # Áp dụng các phương pháp detection
        hough_lines = self.detect_vertical_lines_hough(binary)
        projection_peaks, _ = self.analyze_vertical_projection(binary)
        morph_lines = self.detect_morphological_lines(binary)
        text_gaps = self.find_text_regions(binary)
        
        # Kết hợp kết quả
        candidates = self.combine_detections(hough_lines, projection_peaks, 
                                           morph_lines, text_gaps)
        
        # Tinh chỉnh để có đúng 3 vị trí cột
        column_positions = self.refine_column_positions(candidates)
        
        print(f"✅ Vị trí cột cuối cùng: {column_positions}")
        
        # Visualize kết quả
        debug_path = os.path.join(output_dir, "debug_detection.png")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        self.visualize_detection(column_positions, debug_path)
        
        # Chuyển đổi sang PIL để xử lý
        img_rgb = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img_rgb)
        
        # Tạo ảnh 1: STT + Họ và Tên + Đồng ý (3 cột đầu)
        img1_pil = pil_img.crop((0, 0, column_positions[2], self.height))
        
        # Tạo ảnh 2: STT + Họ và Tên + Không đồng ý
        # Ghép cột 1,2 với cột 4
        img2_left = pil_img.crop((0, 0, column_positions[1], self.height))  # STT + Họ và Tên
        img2_right = pil_img.crop((column_positions[2], 0, self.width, self.height))  # Không đồng ý
        
        # Ghép hai phần
        img2_width = column_positions[1] + (self.width - column_positions[2])
        img2_pil = Image.new('RGB', (img2_width, self.height), 'white')
        img2_pil.paste(img2_left, (0, 0))
        img2_pil.paste(img2_right, (column_positions[1], 0))
        
        # Lưu kết quả
        output1_path = os.path.join(output_dir, "table_dong_y.png")
        output2_path = os.path.join(output_dir, "table_khong_dong_y.png")
        
        img1_pil.save(output1_path, quality=95, optimize=True)
        img2_pil.save(output2_path, quality=95, optimize=True)
        
        # Chuyển đổi sang numpy arrays (BGR format cho OpenCV)
        img1_numpy = cv2.cvtColor(np.array(img1_pil), cv2.COLOR_RGB2BGR)
        img2_numpy = cv2.cvtColor(np.array(img2_pil), cv2.COLOR_RGB2BGR)
        
        print(f"✅ Đã tạo ảnh 1 (STT + Họ và Tên + Đồng ý): {output1_path}")
        print(f"✅ Đã tạo ảnh 2 (STT + Họ và Tên + Không đồng ý): {output2_path}")
        print(f"📊 Kích thước ảnh 1: {img1_numpy.shape}")
        print(f"📊 Kích thước ảnh 2: {img2_numpy.shape}")
        
        return output1_path, output2_path, column_positions, img1_numpy, img2_numpy

def main():
    """Hàm chính để demo"""
    print("🚀 Auto Table Splitter - Phiên bản chuẩn hóa")
    print("=" * 60)
    
    # Đường dẫn ảnh input
    input_path = "table_01_cropped.jpg"  # Thay đổi tên file theo ảnh của bạn
    
    if not os.path.exists(input_path):
        print(f"❌ Không tìm thấy file: {input_path}")
        print("💡 Vui lòng đặt file ảnh bảng vào thư mục")
        return
    
    try:
        # Khởi tạo và chạy
        splitter = AutoTableSplitter(input_path)
        
        # Gọi hàm split_table với thư mục output tùy chỉnh
        output1_path, output2_path, positions, img1_np, img2_np = splitter.split_table("my_output")
        
        print("\n🎉 Hoàn thành!")
        print(f"📊 Vị trí cột phát hiện: {positions}")
        print(f"📁 Ảnh 1: {output1_path}")
        print(f"📁 Ảnh 2: {output2_path}")
        print(f"🔍 Ảnh debug: my_output/debug_detection.png")
        print(f"📊 Shape ảnh 1 (numpy): {img1_np.shape}")
        print(f"📊 Shape ảnh 2 (numpy): {img2_np.shape}")
        
        # Ví dụ sử dụng numpy arrays
        print(f"🎯 Có thể sử dụng img1_np và img2_np cho xử lý tiếp theo...")
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()