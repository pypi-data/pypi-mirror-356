# 📚 HƯỚNG DẪN SỬ DỤNG HOÀN CHỈNH - HỆ THỐNG TRÍCH XUẤT BẢNG

> **Phiên bản**: 2.0  
> **Ngày cập nhật**: 2025-06-18  
> **Tác giả**: AI Assistant

---

## 🎯 TỔNG QUAN HỆ THỐNG

Hệ thống trích xuất bảng này cung cấp giải pháp toàn diện để:
- ✅ **Phát hiện và tách bảng** từ ảnh tài liệu
- ✅ **Trích xuất hàng (rows)** với độ chính xác cao  
- ✅ **Trích xuất cột (columns)** linh hoạt
- ✅ **Merge cột theo nhu cầu** tùy chỉnh
- ✅ **Hỗ trợ GPU** để tăng tốc xử lý
- ✅ **Quản lý bộ nhớ** hiệu quả
- ✅ **Debug và troubleshooting** chi tiết

---

## 🏗️ CẤU TRÚC HỆ THỐNG

```
detectrow1806/
├── 📦 Core Package
│   ├── detect_row/
│   │   ├── __init__.py                    # API chính
│   │   ├── base.py                        # Base classes
│   │   ├── advanced_table_extractor.py    # Trích xuất bảng
│   │   ├── advanced_row_extractor.py      # Trích xuất hàng
│   │   ├── advanced_column_extractor.py   # Trích xuất cột
│   │   ├── gpu_support.py                 # Hỗ trợ GPU
│   │   └── tesseract_ocr_extractor.py     # OCR support
│   
├── 🚀 Main Scripts
│   ├── extract_tables_and_columns.py     # Script chính (All-in-one)
│   ├── extract_tables_final.py           # Chỉ tách bảng
│   ├── extract_columns_demo.py           # Demo trích xuất cột
│   └── column_groups_helper.py           # Trợ giúp cấu hình merge
│   
├── 🔧 Utilities
│   ├── test_gpu_support.py               # Test GPU
│   ├── show_results_summary.py           # Hiển thị kết quả
│   └── check_versions.py                 # Kiểm tra phiên bản
│   
└── 📁 Directories
    ├── input/                            # Ảnh đầu vào
    ├── output/                           # Kết quả
    ├── debug/                            # Debug files
    └── configs/                          # Cấu hình merge
```

---

## 🚀 QUICK START - BẮT ĐẦU NHANH

### 1. **Cài đặt Dependencies**
```bash
# Cài đặt packages cơ bản
pip install -r requirements.txt

# Cài đặt GPU support (tùy chọn)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### 2. **Test GPU Support**
```bash
python test_gpu_support.py
```

### 3. **Trích xuất bảng cơ bản**
```bash
# Đặt ảnh vào thư mục input/
cp your_image.png input/

# Chạy trích xuất (sử dụng cấu hình mặc định)
python extract_tables_and_columns.py your_image.png
```

### 4. **Xem kết quả**
```bash
# Kết quả trong output/tables_and_columns/
ls output/tables_and_columns/tables/      # Các bảng đã tách
ls output/tables_and_columns/columns/     # Các cột đã trích xuất
```

---

## 📋 CHI TIẾT CÁC TÍNH NĂNG

### 🔍 **1. TRÍCH XUẤT BẢNG (Table Extraction)**

#### Script chuyên dụng:
```bash
# Chỉ tách bảng với thuật toán tối ưu
python extract_tables_final.py
```

#### Tích hợp trong workflow:
```bash
# Tách bảng + trích xuất cột
python extract_tables_and_columns.py image.png
```

#### Thuật toán sử dụng:
- **Adaptive Threshold**: Tự động điều chỉnh ngưỡng
- **Morphological Operations**: Phát hiện cấu trúc bảng
- **Contour Analysis**: Lọc và validate bảng
- **Overlap Removal**: Loại bỏ trùng lặp thông minh

#### Kết quả:
```
output/tables_and_columns/tables/
├── image_table_0.jpg    # Bảng 1 (thường là bảng chính)
├── image_table_1.jpg    # Bảng 2 
└── image_table_2.jpg    # Bảng 3 (nếu có)
```

### 📏 **2. TRÍCH XUẤT HÀNG (Row Extraction)**

#### API sử dụng:
```python
from detect_row import AdvancedRowExtractor

extractor = AdvancedRowExtractor(
    input_dir="input",
    output_dir="output/rows",
    debug_dir="debug/rows"
)

# Trích xuất hàng từ bảng
rows = extractor.extract_rows_from_table(table_image, "table_name")
```

#### Tham số quan trọng:
- `min_row_height`: Chiều cao tối thiểu của hàng (default: 20px)
- `row_overlap_threshold`: Ngưỡng overlap giữa các hàng (default: 0.3)
- `noise_reduction`: Giảm nhiễu (default: True)

### 📊 **3. TRÍCH XUẤT CỘT (Column Extraction)**

#### Cách sử dụng cơ bản:
```bash
# Trích xuất cột với cấu hình mặc định
python extract_tables_and_columns.py image.png
```

#### Tùy chỉnh nhóm cột:
```bash
# Định nghĩa nhóm cột tùy chỉnh
python extract_tables_and_columns.py image.png \
  --column-groups "header:1;content:2,3;footer:4"
```

#### Chế độ tương tác:
```bash
# Thiết lập nhóm cột tương tác
python extract_tables_and_columns.py --interactive
```

#### Không merge (chỉ cột riêng):
```bash
# Chỉ tách cột riêng biệt
python extract_tables_and_columns.py image.png --no-merge
```

### 🔗 **4. MERGE CỘT (Column Merging)**

#### Sử dụng Column Groups Helper:
```bash
# Chạy trợ giúp tạo cấu hình
python column_groups_helper.py
```

#### Templates có sẵn:
1. **basic**: Merge cơ bản (1+2, 3, 4)
2. **enhanced**: Có thêm merge mở rộng (1+2+3, 1+2+4)
3. **comprehensive**: Đầy đủ các combination
4. **document_structure**: Phù hợp tài liệu Việt Nam
5. **custom_pairs**: Các cặp tùy chỉnh

#### Format định nghĩa nhóm:
```bash
# Format: group_name:col1,col2,col3;another_group:col4
--column-groups "cols_1_2:1,2;col_3:3;cols_1_2_3:1,2,3"
```

#### Ví dụ thực tế:
```bash
# Merge theo ngữ cảnh tài liệu
python extract_tables_and_columns.py image.png \
  --column-groups "stt:1;ho_ten:2;dong_y:3;khong_dong_y:4;thong_tin:1,2;ket_qua:3,4"
```

### ⚙️ **5. THIẾT LẬP THÔNG SỐ (Parameters Setup)**

#### Thông số bảng (Table Parameters):
```python
# Trong script hoặc API
table_extractor = AdvancedTableExtractor(
    input_dir="input",
    output_dir="output/tables", 
    debug_dir="debug/tables",
    # Thông số tùy chỉnh
    min_table_area_ratio=0.003,    # 0.3% diện tích ảnh
    max_table_area_ratio=0.25,     # 25% diện tích ảnh
    min_aspect_ratio=1.0,          # Tỷ lệ khung hình tối thiểu
    max_aspect_ratio=15.0          # Tỷ lệ khung hình tối đa
)
```

#### Thông số cột (Column Parameters):
```python
column_extractor = AdvancedColumnExtractor(
    input_dir="input",
    output_dir="output/columns",
    debug_dir="debug/columns",
    min_column_width=20,           # Độ rộng cột tối thiểu
    column_overlap_threshold=0.3,  # Ngưỡng overlap
    vertical_line_threshold=0.4    # Ngưỡng đường kẻ dọc
)
```

#### Thông số hàng (Row Parameters):
```python
row_extractor = AdvancedRowExtractor(
    input_dir="input", 
    output_dir="output/rows",
    debug_dir="debug/rows",
    min_row_height=20,             # Chiều cao hàng tối thiểu
    horizontal_line_threshold=0.4, # Ngưỡng đường kẻ ngang
    row_spacing_threshold=5        # Khoảng cách giữa các hàng
)
```

### 🐛 **6. DEBUG VÀ TROUBLESHOOTING**

#### Bật chế độ debug:
```bash
# Script tự động tạo debug files trong debug/
python extract_tables_and_columns.py image.png
```

#### Cấu trúc debug:
```
debug/tables_and_columns/
├── tables/
│   ├── final_binary.jpg          # Ảnh binary sau xử lý
│   ├── final_structure.jpg       # Cấu trúc bảng phát hiện
│   ├── final_result.jpg          # Kết quả cuối cùng với bounding boxes
│   └── all_contours.jpg          # Tất cả contours
└── columns/
    └── table_name/
        ├── column_detection.jpg   # Phát hiện cột
        ├── vertical_lines.jpg     # Đường kẻ dọc
        └── histogram.jpg          # Histogram projection
```

#### Phân tích debug files:

1. **final_binary.jpg**: Kiểm tra chất lượng threshold
   - Nếu quá nhiễu → Tăng threshold
   - Nếu thiếu chi tiết → Giảm threshold

2. **final_structure.jpg**: Xem cấu trúc bảng
   - Đường kẻ không rõ → Tăng kernel size
   - Quá nhiều đường kẻ → Giảm kernel size

3. **vertical_lines.jpg**: Kiểm tra phát hiện cột
   - Thiếu cột → Giảm `vertical_line_threshold`
   - Quá nhiều cột → Tăng `vertical_line_threshold`

#### Troubleshooting thường gặp:

**❌ Không phát hiện được bảng:**
```python
# Giảm ngưỡng diện tích
min_table_area_ratio = 0.001  # Thay vì 0.003
```

**❌ Phát hiện sai cột:**
```python
# Điều chỉnh thông số cột
min_column_width = 10         # Giảm độ rộng tối thiểu
vertical_line_threshold = 0.3 # Giảm ngưỡng
```

**❌ Chất lượng ảnh kém:**
```python
# Tăng cường xử lý ảnh
binary = cv2.medianBlur(binary, 3)  # Giảm nhiễu
binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, larger_kernel)
```

### 📤 **7. OUTPUT VÀ KẾT QUẢ**

#### Cấu trúc output hoàn chỉnh:
```
output/tables_and_columns/
├── 📁 tables/                    # Các bảng đã tách
│   ├── image_table_0.jpg
│   ├── image_table_1.jpg
│   └── image_table_2.jpg
│
└── 📁 columns/                   # Cột từ từng bảng
    ├── image_table_0/
    │   ├── 📁 individual_columns/    # Cột riêng biệt
    │   │   ├── image_table_0_column_01.jpg
    │   │   ├── image_table_0_column_02.jpg
    │   │   ├── image_table_0_column_03.jpg
    │   │   └── image_table_0_column_04.jpg
    │   │
    │   └── 📁 merged_columns/        # Cột đã merge
    │       ├── image_table_0_columns_1_2_cols_1_2.jpg
    │       ├── image_table_0_columns_3_col_3.jpg
    │       ├── image_table_0_columns_4_col_4.jpg
    │       ├── image_table_0_columns_1_2_3_cols_1_2_3.jpg
    │       └── image_table_0_columns_1_2_4_cols_1_2_4.jpg
    │
    ├── image_table_1/              # Tương tự cho bảng 2
    └── image_table_2/              # Tương tự cho bảng 3
```

#### Thống kê kết quả:
```bash
# Xem tóm tắt kết quả
python show_results_summary.py
```

---

## 🚀 HỖ TRỢ GPU VÀ QUẢN LÝ BỘ NHỚ

### 🎮 **GPU Support**

#### Kiểm tra GPU:
```bash
# Test GPU availability
python test_gpu_support.py
```

#### Kích hoạt GPU:
```python
from detect_row.gpu_support import GPUManager

# Khởi tạo GPU manager
gpu_manager = GPUManager()

if gpu_manager.is_gpu_available():
    print("✅ GPU có sẵn")
    print(f"🎮 GPU: {gpu_manager.get_gpu_info()}")
    
    # Sử dụng GPU cho xử lý
    device = gpu_manager.get_device()
    # Chuyển tensor lên GPU: tensor.to(device)
else:
    print("❌ GPU không có sẵn, sử dụng CPU")
```

#### Tối ưu GPU:
```python
# Trong script xử lý
import torch

# Cấu hình GPU
if torch.cuda.is_available():
    torch.backends.cudnn.benchmark = True  # Tăng tốc convolution
    torch.cuda.empty_cache()               # Xóa cache
    
    # Batch processing trên GPU
    batch_size = 8 if torch.cuda.get_device_properties(0).total_memory > 8e9 else 4
```

### 🧠 **Quản lý bộ nhớ hiệu quả**

#### Memory Management Class:
```python
from detect_row.gpu_support import MemoryManager

memory_manager = MemoryManager()

# Theo dõi bộ nhớ
memory_manager.monitor_memory()

# Xử lý batch với giới hạn bộ nhớ
for batch in memory_manager.create_batches(images, max_memory_gb=4):
    # Xử lý batch
    results = process_batch(batch)
    
    # Giải phóng bộ nhớ
    memory_manager.cleanup()
```

#### Tối ưu bộ nhớ:
```python
import gc
import psutil

class MemoryOptimizer:
    def __init__(self, max_memory_percent=80):
        self.max_memory_percent = max_memory_percent
    
    def check_memory(self):
        """Kiểm tra sử dụng bộ nhớ"""
        memory = psutil.virtual_memory()
        return memory.percent
    
    def cleanup_if_needed(self):
        """Dọn dẹp bộ nhớ nếu cần"""
        if self.check_memory() > self.max_memory_percent:
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
    
    def process_with_memory_limit(self, images):
        """Xử lý với giới hạn bộ nhớ"""
        results = []
        for i, image in enumerate(images):
            # Xử lý ảnh
            result = self.process_image(image)
            results.append(result)
            
            # Dọn dẹp mỗi 10 ảnh
            if (i + 1) % 10 == 0:
                self.cleanup_if_needed()
        
        return results
```

#### Batch Processing thông minh:
```python
def smart_batch_processing(images, target_memory_gb=2):
    """Xử lý batch thông minh theo bộ nhớ có sẵn"""
    
    # Tính toán batch size tối ưu
    available_memory = psutil.virtual_memory().available / (1024**3)  # GB
    image_memory = estimate_image_memory(images[0]) if images else 0.1  # GB
    
    optimal_batch_size = min(
        len(images),
        max(1, int(target_memory_gb / image_memory))
    )
    
    print(f"🧠 Bộ nhớ khả dụng: {available_memory:.1f}GB")
    print(f"📊 Batch size tối ưu: {optimal_batch_size}")
    
    # Xử lý theo batch
    results = []
    for i in range(0, len(images), optimal_batch_size):
        batch = images[i:i + optimal_batch_size]
        batch_results = process_batch(batch)
        results.extend(batch_results)
        
        # Dọn dẹp sau mỗi batch
        gc.collect()
        
    return results
```

---

## 📊 WORKFLOW HOÀN CHỈNH

### 🔄 **Workflow tự động**

```bash
#!/bin/bash
# auto_extract.sh - Script tự động hoàn chỉnh

echo "🚀 Bắt đầu workflow trích xuất bảng tự động"

# 1. Kiểm tra GPU
echo "🎮 Kiểm tra GPU..."
python test_gpu_support.py

# 2. Kiểm tra ảnh đầu vào
echo "📁 Kiểm tra ảnh đầu vào..."
if [ ! -d "input" ] || [ -z "$(ls -A input/)" ]; then
    echo "❌ Không có ảnh trong thư mục input/"
    exit 1
fi

# 3. Dọn dẹp output cũ
echo "🧹 Dọn dẹp output cũ..."
rm -rf output/tables_and_columns/
rm -rf debug/tables_and_columns/

# 4. Trích xuất với cấu hình tối ưu
echo "⚙️ Trích xuất bảng và cột..."
python extract_tables_and_columns.py \
    --column-groups "stt:1;ho_ten:2;dong_y:3;khong_dong_y:4;info:1,2;result:3,4;full:1,2,3,4"

# 5. Hiển thị kết quả
echo "📊 Hiển thị kết quả..."
python show_results_summary.py

echo "✅ Hoàn thành workflow!"
```

### 🎯 **Workflow cho production**

```python
class ProductionWorkflow:
    """Workflow production với error handling và logging"""
    
    def __init__(self, config):
        self.config = config
        self.logger = self.setup_logging()
        self.memory_manager = MemoryManager()
        self.gpu_manager = GPUManager()
    
    def run_full_pipeline(self, input_images):
        """Chạy pipeline hoàn chỉnh"""
        try:
            # 1. Validate input
            validated_images = self.validate_inputs(input_images)
            
            # 2. Setup environment
            self.setup_environment()
            
            # 3. Process images
            results = self.process_images_batch(validated_images)
            
            # 4. Post-process
            final_results = self.post_process_results(results)
            
            # 5. Generate report
            self.generate_report(final_results)
            
            return final_results
            
        except Exception as e:
            self.logger.error(f"Pipeline failed: {e}")
            raise
        finally:
            self.cleanup()
    
    def process_images_batch(self, images):
        """Xử lý ảnh theo batch với monitoring"""
        results = []
        total_images = len(images)
        
        for i, image_batch in enumerate(self.create_smart_batches(images)):
            self.logger.info(f"Processing batch {i+1}/{total_images}")
            
            # Monitor memory
            memory_usage = self.memory_manager.get_usage()
            if memory_usage > 80:
                self.memory_manager.force_cleanup()
            
            # Process batch
            batch_results = self.process_single_batch(image_batch)
            results.extend(batch_results)
            
            # Progress update
            processed = len(results)
            progress = (processed / total_images) * 100
            self.logger.info(f"Progress: {progress:.1f}% ({processed}/{total_images})")
        
        return results
```

---

## 🔧 ADVANCED CONFIGURATION

### ⚙️ **Config File hệ thống**

Tạo file `config.json`:
```json
{
    "table_extraction": {
        "adaptive_threshold": {
            "max_value": 255,
            "adaptive_method": "ADAPTIVE_THRESH_GAUSSIAN_C",
            "threshold_type": "THRESH_BINARY_INV",
            "block_size": 15,
            "c": 3
        },
        "morphology": {
            "kernel_ratio": 45,
            "iterations": 1
        },
        "filtering": {
            "min_area_ratio": 0.003,
            "max_area_ratio": 0.25,
            "min_aspect_ratio": 1.0,
            "max_aspect_ratio": 15.0
        }
    },
    "column_extraction": {
        "min_column_width": 20,
        "vertical_line_threshold": 0.4,
        "overlap_threshold": 0.3
    },
    "row_extraction": {
        "min_row_height": 20,
        "horizontal_line_threshold": 0.4,
        "spacing_threshold": 5
    },
    "performance": {
        "use_gpu": true,
        "batch_size": 8,
        "max_memory_gb": 4,
        "num_workers": 4
    },
    "output": {
        "save_debug": true,
        "save_individual_columns": true,
        "save_merged_columns": true,
        "image_quality": 95
    }
}
```

### 🎛️ **Sử dụng config file**:
```python
import json
from detect_row import AdvancedTableExtractor

# Load config
with open('config.json', 'r') as f:
    config = json.load(f)

# Initialize với config
extractor = AdvancedTableExtractor(
    config=config['table_extraction']
)
```

---

## 📈 PERFORMANCE OPTIMIZATION

### ⚡ **Speed Optimization**

1. **GPU Acceleration**:
```python
# Enable GPU
export CUDA_VISIBLE_DEVICES=0
python extract_tables_and_columns.py --use-gpu
```

2. **Multi-threading**:
```python
from concurrent.futures import ThreadPoolExecutor

def process_multiple_images(image_paths, num_workers=4):
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = []
        for image_path in image_paths:
            future = executor.submit(process_single_image, image_path)
            futures.append(future)
        
        results = []
        for future in futures:
            results.append(future.result())
    
    return results
```

3. **Memory Mapping**:
```python
import numpy as np

def load_image_memory_mapped(image_path):
    """Load ảnh với memory mapping để tiết kiệm RAM"""
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    
    # Convert to memory-mapped array
    temp_file = f"/tmp/temp_image_{os.getpid()}.dat"
    fp = np.memmap(temp_file, dtype=image.dtype, mode='w+', shape=image.shape)
    fp[:] = image[:]
    
    return fp
```

### 🎯 **Quality vs Speed Trade-offs**

```python
# Preset configurations
PRESETS = {
    "high_quality": {
        "adaptive_threshold_block_size": 15,
        "morphology_iterations": 2,
        "min_area_ratio": 0.001,
        "enable_noise_reduction": True
    },
    "balanced": {
        "adaptive_threshold_block_size": 11,
        "morphology_iterations": 1,
        "min_area_ratio": 0.003,
        "enable_noise_reduction": True
    },
    "fast": {
        "adaptive_threshold_block_size": 9,
        "morphology_iterations": 1,
        "min_area_ratio": 0.005,
        "enable_noise_reduction": False
    }
}
```

---

## 🏆 BEST PRACTICES

### ✅ **DOs (Nên làm)**

1. **Chuẩn bị ảnh đầu vào**:
   - ✅ Độ phân giải tối thiểu: 300 DPI
   - ✅ Format: PNG, JPG, TIFF
   - ✅ Contrast tốt giữa text và background

2. **Cấu hình hệ thống**:
   - ✅ Luôn test GPU trước khi chạy production
   - ✅ Monitor memory usage
   - ✅ Enable debug cho lần chạy đầu tiên

3. **Xử lý batch**:
   - ✅ Xử lý theo batch để tối ưu memory
   - ✅ Cleanup memory sau mỗi batch
   - ✅ Save intermediate results

### ❌ **DON'Ts (Không nên làm)**

1. **Tránh lỗi thường gặp**:
   - ❌ Không process ảnh quá lớn (>20MB) mà không resize
   - ❌ Không ignore memory warnings
   - ❌ Không skip validation input

2. **Performance**:
   - ❌ Không load tất cả ảnh vào memory cùng lúc
   - ❌ Không sử dụng thread quá nhiều (max = CPU cores)
   - ❌ Không disable debug trong production

---

## 🆘 TROUBLESHOOTING GUIDE

### 🐛 **Lỗi thường gặp**

#### **1. Memory Error**
```
Error: RuntimeError: CUDA out of memory
```
**Giải pháp**:
```bash
# Giảm batch size
python extract_tables_and_columns.py --batch-size 2

# Hoặc sử dụng CPU
python extract_tables_and_columns.py --no-gpu
```

#### **2. Không phát hiện được bảng**
```
Warning: Không phát hiện bảng hợp lệ
```
**Giải pháp**:
```python
# Điều chỉnh threshold trong code
min_table_area_ratio = 0.001  # Giảm ngưỡng
adaptive_threshold_block_size = 21  # Tăng block size
```

#### **3. Cột bị tách sai**
```
Warning: Số cột phát hiện không chính xác
```
**Giải pháp**:
```python
# Kiểm tra debug/columns/vertical_lines.jpg
# Điều chỉnh:
min_column_width = 10
vertical_line_threshold = 0.3
```

#### **4. Performance chậm**
**Chẩn đoán**:
```bash
# Check GPU
nvidia-smi

# Check CPU usage
htop

# Check memory
free -h
```

**Tối ưu**:
```bash
# Sử dụng GPU
python extract_tables_and_columns.py --use-gpu

# Tăng workers
python extract_tables_and_columns.py --workers 8

# Giảm chất lượng output
python extract_tables_and_columns.py --quality 80
```

---

## 📞 SUPPORT & COMMUNITY

### 🔗 **Resources**

- 📚 **Documentation**: `/docs/`
- 🐛 **Bug Reports**: `/issues/`
- 💡 **Feature Requests**: `/discussions/`
- 📧 **Email Support**: support@example.com

### 🤝 **Contributing**

1. Fork repository
2. Create feature branch
3. Add tests
4. Submit pull request

### 📄 **License**

MIT License - Free for commercial and personal use.

---

*Cập nhật lần cuối: 2025-06-18*  
*Phiên bản hướng dẫn: 2.0* 