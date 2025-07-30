#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trích xuất bảng và rows - Sử dụng Local Package detect-row
========================================================

Script sử dụng package detect-row từ source code local
Không sử dụng pip package do pip package bị lỗi thiếu BaseRowExtractor

Lưu ý: Mặc dù có import detect_row, nhưng Python ưu tiên local code
Sử dụng: python extract_table_local_package.py
"""

import os
import sys
import cv2
import numpy as np
import json
import re
from datetime import datetime
from typing import List, Tuple, Dict, Any
import matplotlib.pyplot as plt
import pytesseract

# FORCE sử dụng local code thay vì pip package
# Thêm thư mục hiện tại vào đầu sys.path để ưu tiên local code
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

print(f"🔧 Forced local import path: {current_dir}")
print(f"📍 sys.path[0]: {sys.path[0]}")

# Import package detect-row từ LOCAL CODE
try:
    from detect_row import AdvancedTableExtractor, AdvancedRowExtractorMain, TesseractRowExtractor
    print(f"✅ Imported detect-row package from LOCAL CODE successfully")
    print(f"📍 Note: Using local source code, not pip package (pip package has BaseRowExtractor issue)")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Đảm bảo thư mục detect_row/ tồn tại với đầy đủ source code")
    print(f"🔍 Current directory: {current_dir}")
    print(f"🔍 detect_row path exists: {os.path.exists(os.path.join(current_dir, 'detect_row'))}")
    exit(1)

def ensure_dir(path: str):
    """Tạo thư mục nếu chưa có"""
    os.makedirs(path, exist_ok=True)
    print(f"📁 Created directory: {path}")

def extract_rows_from_table(table_image_path: str, table_name: str, output_base: str) -> Dict[str, Any]:
    """
    Trích xuất rows từ một bảng sử dụng detect-row package
    
    Args:
        table_image_path: Đường dẫn ảnh bảng
        table_name: Tên bảng
        output_base: Thư mục output
    
    Returns:
        Dict: Thông tin kết quả trích xuất
    """
    print(f"\n--- Xử lý {table_name} ---")
    
    # Đọc ảnh bảng
    table_image = cv2.imread(table_image_path)
    if table_image is None:
        print(f"❌ Không thể đọc {table_image_path}")
        return {"error": "Cannot read image"}
    
    # Sử dụng AdvancedRowExtractorMain để trích xuất rows
    print("🔍 Sử dụng AdvancedRowExtractorMain...")
    row_extractor = AdvancedRowExtractorMain()
    
    try:
        # Trích xuất rows
        rows_result = row_extractor.extract_rows_from_table(table_image, table_name)
        
        print(f"🔍 Kết quả trích xuất: {type(rows_result)}")
        
        # Xử lý kết quả dựa trên cấu trúc thực tế
        rows = []
        if isinstance(rows_result, dict):
            if 'rows' in rows_result:
                rows = rows_result['rows']
            elif 'extracted_rows' in rows_result:
                rows = rows_result['extracted_rows']
            else:
                # Nếu không có key cụ thể, thử lấy tất cả values là list
                for key, value in rows_result.items():
                    if isinstance(value, list) and len(value) > 0:
                        rows = value
                        break
        elif isinstance(rows_result, list):
            rows = rows_result
        
        if not rows:
            print("⚠️ Không trích xuất được rows")
            print(f"🔍 Cấu trúc kết quả: {rows_result}")
            return {"error": "No rows extracted", "debug_info": str(rows_result)}
        
        print(f"✅ Trích xuất được {len(rows)} rows")
        
        # Lưu từng row
        saved_files = []
        rows_dir = os.path.join(output_base, "rows")
        
        for i, row_data in enumerate(rows):
            row_image = None
            
            # Xử lý các cấu trúc dữ liệu khác nhau
            if isinstance(row_data, dict):
                if 'image' in row_data:
                    row_image = row_data['image']
                elif 'row_image' in row_data:
                    row_image = row_data['row_image']
                else:
                    # Tìm key chứa image data
                    for key, value in row_data.items():
                        if isinstance(value, np.ndarray) and len(value.shape) >= 2:
                            row_image = value
                            break
            elif isinstance(row_data, np.ndarray):
                row_image = row_data
            
            if row_image is not None:
                filename = f"{table_name}_row_{i:02d}.jpg"
                filepath = os.path.join(rows_dir, filename)
                
                cv2.imwrite(filepath, row_image)
                saved_files.append(filepath)
                print(f"💾 Đã lưu: {filename}")
            else:
                print(f"⚠️ Row {i}: Không tìm thấy image data")
        
        # OCR cho từng row
        print("🔤 Thực hiện OCR cột đầu tiên (STT) cho các rows...")
        ocr_results = []
        
        for i, row_data in enumerate(rows):
            row_image = None
            bbox = []
            
            # Xử lý các cấu trúc dữ liệu khác nhau
            if isinstance(row_data, dict):
                if 'image' in row_data:
                    row_image = row_data['image']
                elif 'row_image' in row_data:
                    row_image = row_data['row_image']
                else:
                    # Tìm key chứa image data
                    for key, value in row_data.items():
                        if isinstance(value, np.ndarray) and len(value.shape) >= 2:
                            row_image = value
                            break
                
                bbox = row_data.get('bbox', row_data.get('coordinates', []))
            elif isinstance(row_data, np.ndarray):
                row_image = row_data
            
            if row_image is not None:
                try:
                    # Phát hiện đường gạch dọc để cắt cột đầu tiên chính xác
                    height, width = row_image.shape[:2]
                    
                    # Chuyển sang grayscale nếu cần
                    if len(row_image.shape) == 3:
                        gray = cv2.cvtColor(row_image, cv2.COLOR_BGR2GRAY)
                    else:
                        gray = row_image.copy()
                    
                    # Phát hiện đường thẳng dọc bằng HoughLinesP
                    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
                    
                    # Tìm đường thẳng dọc
                    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=int(height*0.3), 
                                          minLineLength=int(height*0.5), maxLineGap=10)
                    
                    vertical_lines = []
                    if lines is not None:
                        for line in lines:
                            x1, y1, x2, y2 = line[0]
                            # Kiểm tra đường thẳng dọc (góc gần 90 độ)
                            if abs(x2 - x1) < 10:  # Đường gần như thẳng đứng
                                vertical_lines.append((x1 + x2) // 2)  # Lấy tọa độ x trung bình
                    
                    # Tìm đường gạch dọc đầu tiên (gần nhất với bên trái)
                    if vertical_lines:
                        vertical_lines.sort()
                        # Lọc các đường quá gần bên trái (có thể là viền bảng)
                        valid_lines = [x for x in vertical_lines if x > width * 0.05]
                        
                        if valid_lines:
                            first_column_width = valid_lines[0]
                            print(f"🔍 Phát hiện đường gạch dọc tại x={first_column_width}px")
                        else:
                            # Fallback: sử dụng 20% nếu không tìm thấy đường gạch dọc hợp lệ
                            first_column_width = int(width * 0.2)
                            print(f"⚠️ Không tìm thấy đường gạch dọc, sử dụng 20% chiều rộng: {first_column_width}px")
                    else:
                        # Fallback: sử dụng 20% nếu không phát hiện được đường gạch dọc
                        first_column_width = int(width * 0.2)
                        print(f"⚠️ Không phát hiện đường gạch dọc, sử dụng 20% chiều rộng: {first_column_width}px")
                    
                    # Cắt cột đầu tiên
                    first_column = row_image[:, :first_column_width]
                    
                    # Lưu cột đầu tiên để debug
                    first_col_filename = f"{table_name}_row_{i:02d}_stt.jpg"
                    first_col_path = os.path.join(output_base, "rows", first_col_filename)
                    cv2.imwrite(first_col_path, first_column)
                    
                    # OCR cột đầu tiên bằng pytesseract trực tiếp
                    import pytesseract
                    
                    # Cấu hình OCR cho số
                    custom_config = r'--oem 3 --psm 8 -c tessedit_char_whitelist=0123456789'
                    stt_text = pytesseract.image_to_string(first_column, config=custom_config).strip()
                    
                    # Lọc chỉ lấy số
                    import re
                    stt_numbers = re.findall(r'\d+', stt_text)
                    stt = stt_numbers[0] if stt_numbers else ""
                    
                    row_ocr = {
                        "row_index": i,
                        "filename": f"{table_name}_row_{i:02d}.jpg",
                        "first_column_file": first_col_filename,
                        "stt": stt,
                        "raw_ocr_text": stt_text,
                        "bbox": bbox,
                        "first_column_width": first_column_width
                    }
                    ocr_results.append(row_ocr)
                    
                    if stt:
                        print(f"📝 Row {i}: STT = {stt}")
                    else:
                        print(f"⚠️ Row {i}: Không phát hiện STT (raw: '{stt_text}')")
                        
                except Exception as ocr_error:
                    print(f"⚠️ Lỗi OCR row {i}: {ocr_error}")
                    row_ocr = {
                        "row_index": i,
                        "filename": f"{table_name}_row_{i:02d}.jpg",
                        "first_column_file": "",
                        "stt": "",
                        "raw_ocr_text": "",
                        "bbox": bbox,
                        "error": str(ocr_error)
                    }
                    ocr_results.append(row_ocr)
        
        # Lưu kết quả OCR
        ocr_file = os.path.join(output_base, "ocr", f"{table_name}_ocr.json")
        with open(ocr_file, 'w', encoding='utf-8') as f:
            json.dump(ocr_results, f, indent=2, ensure_ascii=False)
        
        return {
            "table_name": table_name,
            "total_rows": len(rows),
            "saved_files": saved_files,
            "ocr_results": ocr_results,
            "success": True
        }
        
    except Exception as e:
        print(f"❌ Lỗi khi trích xuất rows: {e}")
        return {"error": str(e)}

def create_summary_visualization(all_results: List[Dict], output_path: str):
    """
    Tạo visualization tổng hợp
    
    Args:
        all_results: Danh sách kết quả từ tất cả bảng
        output_path: Đường dẫn lưu visualization
    """
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Biểu đồ số rows theo bảng
    table_names = []
    row_counts = []
    
    for result in all_results:
        if result.get('success'):
            table_names.append(result['table_name'])
            row_counts.append(result['total_rows'])
    
    if table_names:
        axes[0].bar(table_names, row_counts, alpha=0.7, color='skyblue')
        axes[0].set_title('Số Rows theo Bảng')
        axes[0].set_xlabel('Bảng')
        axes[0].set_ylabel('Số Rows')
        axes[0].grid(True, alpha=0.3)
        
        # Thêm số liệu trên cột
        for i, count in enumerate(row_counts):
            axes[0].text(i, count + 0.5, str(count), ha='center', fontweight='bold')
    
    # Biểu đồ tổng hợp
    total_tables = len([r for r in all_results if r.get('success')])
    total_rows = sum(r.get('total_rows', 0) for r in all_results if r.get('success'))
    
    categories = ['Bảng', 'Rows']
    values = [total_tables, total_rows]
    colors = ['lightcoral', 'lightgreen']
    
    axes[1].bar(categories, values, color=colors, alpha=0.7)
    axes[1].set_title('Tổng Hợp Kết Quả')
    axes[1].set_ylabel('Số Lượng')
    axes[1].grid(True, alpha=0.3)
    
    # Thêm số liệu trên cột
    for i, value in enumerate(values):
        axes[1].text(i, value + max(values) * 0.02, str(value), ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"📊 Đã lưu visualization tổng hợp: {output_path}")

def main():
    """Hàm chính"""
    image_path = "image0524.png"
    output_base = "pip_package_extraction_output"
    
    print(f"🚀 TRÍCH XUẤT BẢNG SỬ DỤNG LOCAL PACKAGE DETECT-ROW")
    print(f"📸 Ảnh đầu vào: {image_path}")
    print(f"📁 Thư mục đầu ra: {output_base}")
    print(f"⏰ Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📦 Package: detect-row (từ LOCAL CODE)")
    
    if not os.path.exists(image_path):
        print(f"❌ Không tìm thấy ảnh: {image_path}")
        return
    
    # Tạo thư mục output
    ensure_dir(output_base)
    ensure_dir(f"{output_base}/tables")
    ensure_dir(f"{output_base}/rows")
    ensure_dir(f"{output_base}/ocr")
    ensure_dir(f"{output_base}/analysis")
    
    # Bước 1: Trích xuất bảng bằng AdvancedTableExtractor
    print(f"\n{'='*60}")
    print("BƯỚC 1: TRÍCH XUẤT BẢNG BẰNG ADVANCEDTABLEEXTRACTOR")
    print(f"{'='*60}")
    
    table_extractor = AdvancedTableExtractor(
        input_dir=os.path.dirname(image_path),
        output_dir=f"{output_base}/tables"
    )
    
    # Trích xuất bảng
    result = table_extractor.process_image(image_path, margin=5, check_text=True)
    
    # Tìm các bảng đã trích xuất
    table_files = []
    tables_dir = f"{output_base}/tables"
    
    if os.path.exists(tables_dir):
        table_files = [f for f in os.listdir(tables_dir) if f.endswith('.jpg')]
        table_files.sort()
    
    if not table_files:
        print("❌ Không trích xuất được bảng nào!")
        return
    
    print(f"✅ Trích xuất được {len(table_files)} bảng")
    
    # Bước 2: Trích xuất rows cho từng bảng
    print(f"\n{'='*60}")
    print("BƯỚC 2: TRÍCH XUẤT ROWS BẰNG ADVANCEDROWEXTRACTORMAIN")
    print(f"{'='*60}")
    
    all_results = []
    
    for table_file in table_files:
        table_path = os.path.join(tables_dir, table_file)
        table_name = os.path.splitext(table_file)[0]
        
        # Trích xuất rows từ bảng
        result = extract_rows_from_table(table_path, table_name, output_base)
        all_results.append(result)
    
    # Bước 3: Tạo báo cáo tổng hợp
    print(f"\n{'='*60}")
    print("BƯỚC 3: BÁO CÁO TỔNG HỢP")
    print(f"{'='*60}")
    
    successful_results = [r for r in all_results if r.get('success')]
    total_tables = len(successful_results)
    total_rows = sum(r.get('total_rows', 0) for r in successful_results)
    
    # Tạo visualization
    viz_path = os.path.join(output_base, "analysis", "summary_visualization.png")
    create_summary_visualization(all_results, viz_path)
    
    # Lưu báo cáo JSON
    summary = {
        "timestamp": datetime.now().isoformat(),
        "method": "Local Package detect-row",
        "package_version": "detect-row from LOCAL CODE",
        "total_tables": total_tables,
        "total_rows_extracted": total_rows,
        "results": all_results
    }
    
    summary_file = os.path.join(output_base, "pip_package_summary.json")
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    # Báo cáo text
    report_file = os.path.join(output_base, "local_package_report.txt")
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("BÁO CÁO TRÍCH XUẤT BẢNG - LOCAL PACKAGE DETECT-ROW\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Package: detect-row (từ LOCAL CODE)\n")
        f.write(f"Tổng số bảng: {total_tables}\n")
        f.write(f"Tổng số rows: {total_rows}\n\n")
        
        f.write("CHI TIẾT:\n")
        f.write("-" * 30 + "\n")
        for result in successful_results:
            f.write(f"\nBảng: {result['table_name']}\n")
            f.write(f"  Rows trích xuất: {result['total_rows']}\n")
            f.write(f"  Files lưu: {len(result['saved_files'])}\n")
            
            # OCR results
            ocr_results = result.get('ocr_results', [])
            stt_rows = [r for r in ocr_results if r.get('stt', '').strip()]
            f.write(f"  Rows có STT: {len(stt_rows)}\n")
    
    # Tổng kết
    print(f"🎉 HOÀN THÀNH TRÍCH XUẤT SỬ DỤNG PACKAGE DETECT-ROW!")
    print(f"✅ Đã xử lý: {total_tables} bảng")
    print(f"✅ Đã trích xuất: {total_rows} rows")
    print(f"📦 Sử dụng: detect-row package từ PyPI")
    print(f"📁 Kết quả lưu tại: {output_base}/")
    print(f"  📊 Bảng: {output_base}/tables/")
    print(f"  📋 Rows: {output_base}/rows/")
    print(f"  🔤 OCR: {output_base}/ocr/")
    print(f"  📈 Phân tích: {output_base}/analysis/")
    
    # Hiển thị danh sách rows
    rows_dir = f"{output_base}/rows"
    if os.path.exists(rows_dir):
        row_files = sorted([f for f in os.listdir(rows_dir) if f.endswith('.jpg')])
        if row_files:
            print(f"\n📋 {len(row_files)} rows đã trích xuất:")
            for row_file in row_files[:10]:  # Hiển thị 10 file đầu
                print(f"  - {row_file}")
            if len(row_files) > 10:
                print(f"  ... và {len(row_files) - 10} files khác")
    
    # Hiển thị một số kết quả OCR STT
    print(f"\n🔤 MỘT SỐ KẾT QUẢ OCR STT:")
    for result in successful_results[:2]:  # Hiển thị 2 bảng đầu
        ocr_results = result.get('ocr_results', [])
        stt_rows = [r for r in ocr_results if r.get('stt', '').strip()][:5]  # 5 rows đầu có STT
        
        if stt_rows:
            print(f"\n📋 {result['table_name']}:")
            for row in stt_rows:
                stt = row['stt']
                raw_text = row.get('raw_ocr_text', '')
                print(f"  Row {row['row_index']}: STT = {stt} (raw: '{raw_text}')")
        else:
            print(f"\n📋 {result['table_name']}: Chưa phát hiện STT nào")

if __name__ == "__main__":
    main() 