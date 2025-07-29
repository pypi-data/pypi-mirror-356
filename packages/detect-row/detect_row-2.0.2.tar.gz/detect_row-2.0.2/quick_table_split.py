#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QUICK TABLE SPLIT - Version đơn giản
====================================

Input:  1 bảng 4 cột (STT | Họ tên | Đồng ý | Không đồng ý)
Output: 2 bảng 3 cột:
  - Bảng A: STT + Họ tên + Đồng ý     (cột 1+2+3)
  - Bảng B: STT + Họ tên + Không đồng ý (cột 1+2+4)

Usage:
    python quick_table_split.py input.jpg
"""

import cv2
import numpy as np
from PIL import Image
import sys
import os

def quick_split(input_path: str, output_dir: str = "output") -> tuple:
    """
    Split bảng nhanh - version đơn giản
    
    Args:
        input_path: Đường dẫn ảnh input
        output_dir: Thư mục output
        
    Returns:
        tuple: (path_table_A, path_table_B)
    """
    print(f"🔄 Processing: {input_path}")
    
    # Tạo output dir
    os.makedirs(output_dir, exist_ok=True)
    
    # Load ảnh
    img = cv2.imread(input_path)
    if img is None:
        raise ValueError(f"Cannot read image: {input_path}")
    
    height, width = img.shape[:2]
    print(f"📐 Size: {width} x {height}")
    
    # Convert to grayscale và detect edges
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Simple vertical projection để tìm cột
    # Sum theo chiều dọc
    projection = np.sum(gray, axis=0)
    
    # Tìm vị trí có ít pixel nhất (đường kẻ hoặc khoảng trống)
    # Smooth projection
    from scipy.ndimage import gaussian_filter1d
    smoothed = gaussian_filter1d(projection, sigma=3)
    
    # Tìm minima (valleys) - có thể là đường phân cách
    from scipy.signal import find_peaks
    
    # Invert để tìm valleys
    inverted = -smoothed
    peaks, _ = find_peaks(inverted, distance=width//10, prominence=np.std(inverted)*0.5)
    
    # Convert back to original scale
    valley_positions = peaks.tolist()
    
    print(f"🔍 Found {len(valley_positions)} potential separators: {valley_positions}")
    
    # Nếu không tìm được, dùng equal division
    if len(valley_positions) < 3:
        print("⚠️ Using equal division fallback")
        valley_positions = [width//4, width//2, 3*width//4]
    
    # Chọn 3 vị trí gần equal nhất
    if len(valley_positions) > 3:
        # Chọn 3 vị trí cân đối nhất
        from itertools import combinations
        best_positions = valley_positions[:3]
        best_score = float('inf')
        
        for combo in combinations(valley_positions, 3):
            combo = sorted(combo)
            sections = [combo[0], combo[1]-combo[0], combo[2]-combo[1], width-combo[2]]
            cv = np.std(sections) / np.mean(sections)
            if cv < best_score:
                best_score = cv
                best_positions = combo
        
        valley_positions = list(best_positions)
    
    # Sort positions
    valley_positions = sorted(valley_positions[:3])
    
    print(f"✅ Final separators: {valley_positions}")
    
    # Convert to PIL cho easy cropping
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_rgb)
    
    # Tạo Table A: Cột 1 + 2 + 3
    table_a = pil_img.crop((0, 0, valley_positions[2], height))
    
    # Tạo Table B: Cột 1 + 2 + 4 (ghép)
    left_part = pil_img.crop((0, 0, valley_positions[1], height))        # Cột 1+2
    right_part = pil_img.crop((valley_positions[2], 0, width, height))   # Cột 4
    
    # Ghép Table B
    table_b_width = valley_positions[1] + (width - valley_positions[2])
    table_b = Image.new('RGB', (table_b_width, height), 'white')
    table_b.paste(left_part, (0, 0))
    table_b.paste(right_part, (valley_positions[1], 0))
    
    # Save results
    table_a_path = os.path.join(output_dir, "table_A_cols_123.jpg")
    table_b_path = os.path.join(output_dir, "table_B_cols_124.jpg")
    
    table_a.save(table_a_path, quality=95)
    table_b.save(table_b_path, quality=95)
    
    print(f"💾 Table A (1+2+3): {table_a_path} - Size: {table_a.size}")
    print(f"💾 Table B (1+2+4): {table_b_path} - Size: {table_b.size}")
    
    # Tạo debug image
    debug_img = img.copy()
    for i, pos in enumerate(valley_positions):
        cv2.line(debug_img, (pos, 0), (pos, height), (0, 255, 0), 2)
        cv2.putText(debug_img, f"Sep{i+1}", (pos+5, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    debug_path = os.path.join(output_dir, "debug_splits.jpg")
    cv2.imwrite(debug_path, debug_img)
    print(f"🔍 Debug: {debug_path}")
    
    return table_a_path, table_b_path

def main():
    """Main function"""
    print("🚀 QUICK TABLE SPLITTER")
    print("=" * 40)
    
    # Check arguments
    if len(sys.argv) < 2:
        print("Usage: python quick_table_split.py <input_image>")
        print("\nExample:")
        print("  python quick_table_split.py table.jpg")
        print("  python quick_table_split.py my_table.png")
        
        # Try default file
        default_files = ["table_input.jpg", "table.jpg", "image.png"]
        for f in default_files:
            if os.path.exists(f):
                print(f"\n✅ Found: {f}, using as input...")
                input_file = f
                break
        else:
            print(f"\n❌ No input file provided and no default files found.")
            return
    else:
        input_file = sys.argv[1]
    
    # Check input exists
    if not os.path.exists(input_file):
        print(f"❌ File not found: {input_file}")
        return
    
    try:
        # Process
        table_a, table_b = quick_split(input_file)
        
        print("\n🎉 SUCCESS!")
        print("=" * 40)
        print(f"📊 Input: {input_file}")
        print(f"📄 Table A (STT + Họ tên + Đồng ý): {table_a}")
        print(f"📄 Table B (STT + Họ tên + Không đồng ý): {table_b}")
        print("🔍 Check debug_splits.jpg to verify column detection")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 