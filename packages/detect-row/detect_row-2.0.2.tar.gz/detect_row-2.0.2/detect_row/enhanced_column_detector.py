#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced Column Detector - Học từ approach của user
===================================================

Kết hợp 4 phương pháp parallel detection như trong main16vip.py
với flexibility của DetectRow 2.0

Author: AI Assistant (inspired by user's main16vip.py)
"""

import cv2
import numpy as np
from PIL import Image
import os
from scipy import signal
from scipy.ndimage import gaussian_filter1d
from typing import Tuple, List, Optional, Dict
from itertools import combinations
import logging

class EnhancedColumnDetector:
    """
    Enhanced Column Detector kết hợp 4 phương pháp parallel
    như trong main16vip.py nhưng flexible cho nhiều use case
    """
    
    def __init__(self, 
                 target_columns: int = 4,
                 debug: bool = False,
                 logger: Optional[logging.Logger] = None):
        """
        Khởi tạo Enhanced Column Detector
        
        Args:
            target_columns: Số cột mục tiêu (default 4 như user)
            debug: Enable debug mode
            logger: Logger instance
        """
        self.target_columns = target_columns
        self.target_separators = target_columns - 1  # n cột cần n-1 separator
        self.debug = debug
        self.logger = logger or logging.getLogger(__name__)
        
        # Weights cho từng phương pháp (học từ user)
        self.method_weights = {
            'hough': 3,      # Tin cậy nhất
            'projection': 2,  # Trung bình
            'morphology': 2,  # Trung bình  
            'text_gaps': 1   # Thấp nhất
        }
        
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Tiền xử lý ảnh - học từ user nhưng cải tiến
        
        Args:
            image: Input image (BGR hoặc Grayscale)
            
        Returns:
            Binary image đã được enhanced
        """
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
            
        height, width = gray.shape
        
        # Adaptive preprocessing based on image size
        blur_kernel = max(3, min(7, width // 200))  # Dynamic kernel size
        
        # Làm mịn để giảm noise
        blurred = cv2.GaussianBlur(gray, (blur_kernel, blur_kernel), 0)
        
        # Tăng độ tương phản - adaptive CLAHE
        clip_limit = 2.0 if width > 1000 else 3.0
        tile_size = max(8, width // 100)
        clahe = cv2.createCLAHE(clipLimit=clip_limit, 
                               tileGridSize=(tile_size, tile_size))
        enhanced = clahe.apply(blurred)
        
        # Adaptive threshold
        block_size = max(15, min(31, width // 50))
        if block_size % 2 == 0:
            block_size += 1
            
        binary = cv2.adaptiveThreshold(enhanced, 255, 
                                     cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY_INV, 
                                     block_size, 2)
        
        if self.debug:
            self.logger.debug(f"Preprocessing: blur_kernel={blur_kernel}, "
                            f"clip_limit={clip_limit}, block_size={block_size}")
        
        return binary
    
    def detect_vertical_lines_hough(self, binary: np.ndarray) -> List[int]:
        """
        Phát hiện đường thẳng dọc bằng Hough Transform
        Học từ user nhưng adaptive threshold
        """
        height, width = binary.shape
        
        # Phát hiện edges với adaptive parameters
        low_threshold = 50
        high_threshold = 150
        if width > 2000:  # High resolution image
            low_threshold = 30
            high_threshold = 100
            
        edges = cv2.Canny(binary, low_threshold, high_threshold, apertureSize=3)
        
        # Adaptive Hough threshold
        hough_threshold = max(int(height * 0.2), 50)
        
        lines = cv2.HoughLines(edges, 1, np.pi/180, threshold=hough_threshold)
        
        vertical_lines = []
        if lines is not None:
            for rho, theta in lines[:, 0]:
                # Chỉ lấy đường thẳng gần dọc - relaxed tolerance
                angle_tolerance = 0.15  # ~8.6 degrees
                if abs(theta) < angle_tolerance or abs(theta - np.pi) < angle_tolerance:
                    x = int(rho / np.cos(theta)) if abs(np.cos(theta)) > 0.01 else None
                    if x is not None and 10 < x < width - 10:
                        vertical_lines.append(x)
        
        return sorted(list(set(vertical_lines)))
    
    def analyze_vertical_projection(self, binary: np.ndarray) -> Tuple[List[int], np.ndarray]:
        """
        Phân tích projection dọc - cải tiến từ user
        """
        height, width = binary.shape
        
        # Tính projection
        projection = np.sum(binary, axis=0)
        
        # Adaptive smoothing
        sigma = max(1, width // 500)
        smoothed = gaussian_filter1d(projection, sigma=sigma)
        
        # Dynamic threshold calculation
        median_val = np.median(smoothed)
        mad = np.median(np.abs(smoothed - median_val))
        
        # Adaptive threshold multiplier
        multiplier = 1.5 if width > 1500 else 2.0
        threshold = median_val + multiplier * mad
        
        # Adaptive peak detection
        min_distance = max(15, width // 30)  # Minimum distance between peaks
        
        peaks, properties = signal.find_peaks(smoothed,
                                            height=threshold,
                                            distance=min_distance,
                                            prominence=mad * 0.5)
        
        if self.debug:
            self.logger.debug(f"Projection: threshold={threshold:.1f}, "
                            f"distance={min_distance}, peaks={len(peaks)}")
        
        return peaks.tolist(), smoothed
    
    def detect_morphological_lines(self, binary: np.ndarray) -> List[int]:
        """
        Phát hiện đường kẻ bằng morphological operations
        Học từ user với adaptive kernel
        """
        height, width = binary.shape
        
        # Adaptive kernel size
        kernel_height = max(height // 15, 10)
        kernel_width = 1
        
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, 
                                                  (kernel_width, kernel_height))
        
        # Morphological operations
        vertical_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, vertical_kernel)
        
        # Tìm contours
        contours, _ = cv2.findContours(vertical_lines, cv2.RETR_EXTERNAL, 
                                     cv2.CHAIN_APPROX_SIMPLE)
        
        line_positions = []
        min_height = height * 0.3  # Adaptive minimum height
        max_width = max(10, width // 100)  # Adaptive maximum width
        
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            # Điều kiện: đường kẻ dọc (cao, hẹp)
            if h > min_height and w <= max_width:
                line_positions.append(x + w // 2)
        
        return sorted(line_positions)
    
    def find_text_regions(self, binary: np.ndarray) -> List[int]:
        """
        Tìm vùng text để xác định cột - cải tiến từ user
        """
        height, width = binary.shape
        
        # Adaptive kernel cho text grouping
        horizontal_kernel_width = max(width // 30, 10)
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, 
                                                    (horizontal_kernel_width, 1))
        
        # Dilate để nhóm text thành blocks
        dilated = cv2.dilate(binary, horizontal_kernel, iterations=2)
        
        # Tìm contours của text blocks
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, 
                                     cv2.CHAIN_APPROX_SIMPLE)
        
        text_regions = []
        min_width = max(20, width // 50)
        min_height = 5
        
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w > min_width and h > min_height:
                text_regions.append((x, x + w))
        
        # Sort và tìm gaps
        text_regions.sort()
        gaps = []
        
        if len(text_regions) > 1:
            for i in range(len(text_regions) - 1):
                gap_start = text_regions[i][1]
                gap_end = text_regions[i + 1][0]
                gap_size = gap_end - gap_start
                
                # Adaptive gap threshold
                min_gap = max(5, width // 100)
                if gap_size > min_gap:
                    gaps.append((gap_start + gap_end) // 2)
        
        return gaps
    
    def combine_detections_weighted(self, 
                                  hough_lines: List[int],
                                  projection_peaks: List[int], 
                                  morph_lines: List[int],
                                  text_gaps: List[int]) -> List[int]:
        """
        Kết hợp kết quả với weighted approach của user
        """
        if self.debug:
            self.logger.debug(f"Detection results:")
            self.logger.debug(f"  Hough lines: {hough_lines}")
            self.logger.debug(f"  Projection peaks: {projection_peaks}")
            self.logger.debug(f"  Morphological lines: {morph_lines}")
            self.logger.debug(f"  Text gaps: {text_gaps}")
        
        # Tổng hợp với trọng số
        all_candidates = []
        
        # Weighted contribution
        for line in hough_lines:
            all_candidates.extend([line] * self.method_weights['hough'])
            
        for peak in projection_peaks:
            all_candidates.extend([peak] * self.method_weights['projection'])
            
        for line in morph_lines:
            all_candidates.extend([line] * self.method_weights['morphology'])
            
        for gap in text_gaps:
            all_candidates.extend([gap] * self.method_weights['text_gaps'])
        
        if not all_candidates:
            return []
        
        # Clustering với adaptive threshold
        all_candidates.sort()
        clusters = []
        current_cluster = [all_candidates[0]]
        
        # Adaptive cluster threshold
        cluster_threshold = max(10, len(all_candidates) // 20)
        
        for candidate in all_candidates[1:]:
            if candidate - current_cluster[-1] <= cluster_threshold:
                current_cluster.append(candidate)
            else:
                # Weighted average của cluster
                cluster_center = int(np.mean(current_cluster))
                clusters.append(cluster_center)
                current_cluster = [candidate]
        
        # Thêm cluster cuối
        if current_cluster:
            cluster_center = int(np.mean(current_cluster))
            clusters.append(cluster_center)
        
        return sorted(clusters)
    
    def optimize_positions(self, candidates: List[int], width: int) -> List[int]:
        """
        Tối ưu hóa vị trí dựa trên CV optimization của user
        Nhưng flexible cho số cột khác nhau
        """
        if len(candidates) < self.target_separators:
            return candidates
        
        if len(candidates) == self.target_separators:
            return candidates
        
        # Chọn optimal combination
        best_score = float('inf')
        best_positions = candidates[:self.target_separators]
        
        for combo in combinations(candidates, self.target_separators):
            combo = sorted(combo)
            
            # Tính độ cân đối của các sections
            sections = []
            
            # First section
            sections.append(combo[0])
            
            # Middle sections
            for i in range(1, len(combo)):
                sections.append(combo[i] - combo[i-1])
            
            # Last section
            sections.append(width - combo[-1])
            
            # Coefficient of variation
            mean_section = np.mean(sections)
            std_section = np.std(sections)
            cv = std_section / mean_section if mean_section > 0 else float('inf')
            
            if cv < best_score:
                best_score = cv
                best_positions = combo
        
        if self.debug:
            self.logger.debug(f"Optimized positions: {best_positions} (CV: {best_score:.3f})")
        
        return list(best_positions)
    
    def detect_columns(self, image: np.ndarray) -> Tuple[List[int], Dict]:
        """
        Main detection method - kết hợp tất cả approaches
        
        Returns:
            Tuple[List[int], Dict]: (column_positions, debug_info)
        """
        height, width = image.shape[:2]
        
        # Preprocess
        binary = self.preprocess_image(image)
        
        # Apply all 4 methods
        hough_lines = self.detect_vertical_lines_hough(binary)
        projection_peaks, projection_smoothed = self.analyze_vertical_projection(binary)
        morph_lines = self.detect_morphological_lines(binary)
        text_gaps = self.find_text_regions(binary)
        
        # Combine with weights
        candidates = self.combine_detections_weighted(hough_lines, projection_peaks,
                                                    morph_lines, text_gaps)
        
        # Optimize positions
        final_positions = self.optimize_positions(candidates, width)
        
        # Debug info
        debug_info = {
            'hough_lines': hough_lines,
            'projection_peaks': projection_peaks,
            'projection_smoothed': projection_smoothed,
            'morph_lines': morph_lines,
            'text_gaps': text_gaps,
            'candidates': candidates,
            'final_positions': final_positions,
            'binary': binary
        }
        
        return final_positions, debug_info
    
    def visualize_detection(self, image: np.ndarray, 
                          debug_info: Dict, 
                          save_path: str) -> None:
        """
        Tạo visualization như user nhưng comprehensive hơn
        """
        debug_img = image.copy()
        height, width = image.shape[:2]
        
        # Vẽ kết quả từ từng method với màu khác nhau
        colors = {
            'hough': (0, 255, 0),      # Green
            'projection': (255, 0, 0),  # Blue  
            'morph': (0, 0, 255),      # Red
            'text': (255, 255, 0),     # Cyan
            'final': (255, 0, 255)     # Magenta
        }
        
        y_offset = 30
        
        # Draw method results
        for method, positions in [
            ('hough', debug_info['hough_lines']),
            ('projection', debug_info['projection_peaks']),
            ('morph', debug_info['morph_lines']),
            ('text', debug_info['text_gaps'])
        ]:
            color = colors[method]
            for pos in positions:
                cv2.line(debug_img, (pos, 0), (pos, height), color, 1)
            
            # Label
            cv2.putText(debug_img, f"{method}: {len(positions)}", 
                       (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX,
                       0.5, color, 1)
            y_offset += 20
        
        # Draw final positions
        for i, pos in enumerate(debug_info['final_positions']):
            color = colors['final']
            cv2.line(debug_img, (pos, 0), (pos, height), color, 3)
            cv2.putText(debug_img, f"Col {i+1}: {pos}",
                       (pos + 5, 50 + i*25), cv2.FONT_HERSHEY_SIMPLEX,
                       0.6, color, 2)
        
        # Stats
        final_pos = debug_info['final_positions']
        if final_pos:
            sections = [final_pos[0]]
            for i in range(1, len(final_pos)):
                sections.append(final_pos[i] - final_pos[i-1])
            sections.append(width - final_pos[-1])
            
            cv2.putText(debug_img, f"Sections: {sections}",
                       (10, height - 40), cv2.FONT_HERSHEY_SIMPLEX,
                       0.5, (255, 255, 255), 1)
            
            mean_section = np.mean(sections)
            cv_score = np.std(sections) / mean_section if mean_section > 0 else 0
            cv2.putText(debug_img, f"CV Score: {cv_score:.3f}",
                       (10, height - 20), cv2.FONT_HERSHEY_SIMPLEX,
                       0.5, (255, 255, 255), 1)
        
        cv2.imwrite(save_path, debug_img)
        
        if self.debug:
            self.logger.debug(f"Debug visualization saved: {save_path}")

# Integration với DetectRow
def enhance_column_detection():
    """
    Function để integrate enhanced detector vào DetectRow
    """
    detector = EnhancedColumnDetector(target_columns=4, debug=True)
    return detector

if __name__ == "__main__":
    # Test
    detector = EnhancedColumnDetector(target_columns=4, debug=True)
    print("✅ Enhanced Column Detector ready!")
    print(f"🎯 Target columns: {detector.target_columns}")
    print(f"🔍 Method weights: {detector.method_weights}") 