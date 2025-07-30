"""
Test GPU Support cho detect_row package
Kiểm tra khả năng sử dụng GPU và so sánh hiệu suất
"""

import cv2
import numpy as np
import time
import sys
import os

# Thêm thư mục detect_row vào path
sys.path.append(os.path.join(os.path.dirname(__file__), 'detect_row'))

try:
    from detect_row.gpu_support import check_gpu_requirements, GPUSupport
except ImportError:
    print("Không thể import GPU support module")
    sys.exit(1)

def test_opencv_gpu():
    """Kiểm tra OpenCV có hỗ trợ CUDA không"""
    print("🔍 Kiểm tra OpenCV CUDA Support:")
    
    # Kiểm tra OpenCV version
    print(f"   OpenCV version: {cv2.__version__}")
    
    # Kiểm tra CUDA support
    if hasattr(cv2, 'cuda'):
        print("   ✅ OpenCV có CUDA module")
        try:
            device_count = cv2.cuda.getCudaEnabledDeviceCount()
            print(f"   📊 Số GPU devices: {device_count}")
            
            if device_count > 0:
                print(f"   🎯 Current GPU device: {cv2.cuda.getDevice()}")
                # In thông tin GPU
                try:
                    print("   📋 GPU Info:")
                    device_info = cv2.cuda.DeviceInfo()
                    print(f"      Name: {device_info.name()}")
                    print(f"      Memory: {device_info.totalMemory() / (1024**3):.1f} GB")
                    print(f"      Compute Capability: {device_info.majorVersion()}.{device_info.minorVersion()}")
                except:
                    print("      Không thể lấy thông tin chi tiết GPU")
            else:
                print("   ❌ Không có GPU device nào hỗ trợ CUDA")
                
        except Exception as e:
            print(f"   ❌ Lỗi khi kiểm tra CUDA devices: {e}")
    else:
        print("   ❌ OpenCV không có CUDA module")
        print("   💡 Cần cài đặt opencv-python với CUDA support")

def benchmark_cpu_vs_gpu():
    """So sánh hiệu suất CPU vs GPU"""
    print("\n⚡ Benchmark CPU vs GPU:")
    
    # Tạo ảnh test lớn
    height, width = 2000, 2000
    test_image = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
    
    # Test CPU
    print("   🖥️  CPU Processing...")
    start_time = time.time()
    for i in range(10):
        gray_cpu = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
        blurred_cpu = cv2.GaussianBlur(gray_cpu, (15, 15), 0)
        _, thresh_cpu = cv2.threshold(blurred_cpu, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cpu_time = time.time() - start_time
    print(f"      CPU time: {cpu_time:.3f}s")
    
    # Test GPU (nếu có)
    gpu_support = GPUSupport()
    if gpu_support.is_gpu_available():
        print("   🎮 GPU Processing...")
        try:
            # Upload ảnh lên GPU
            gpu_image = cv2.cuda_GpuMat()
            gpu_image.upload(test_image)
            
            start_time = time.time()
            for i in range(10):
                # Convert to grayscale trên GPU
                gpu_gray = cv2.cuda.cvtColor(gpu_image, cv2.COLOR_BGR2GRAY)
                # Gaussian blur trên GPU
                gpu_blurred = cv2.cuda.GaussianBlur(gpu_gray, (15, 15), 0)
                # Threshold trên GPU
                _, gpu_thresh = cv2.cuda.threshold(gpu_blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                # Download về CPU (để công bằng)
                result_gpu = gpu_thresh.download()
            
            gpu_time = time.time() - start_time
            print(f"      GPU time: {gpu_time:.3f}s")
            
            # Tính speedup
            speedup = cpu_time / gpu_time
            print(f"   📈 GPU Speedup: {speedup:.2f}x")
            
        except Exception as e:
            print(f"   ❌ Lỗi GPU processing: {e}")
    else:
        print("   ❌ GPU không khả dụng để benchmark")

def test_detect_row_with_gpu():
    """Test detect_row package với GPU support"""
    print("\n🔬 Test detect_row package với GPU:")
    
    # Kiểm tra xem có ảnh test không
    image_path = "image0524.png"
    if not os.path.exists(image_path):
        print(f"   ❌ Không tìm thấy ảnh test: {image_path}")
        return
    
    # Load ảnh
    image = cv2.imread(image_path)
    if image is None:
        print(f"   ❌ Không thể load ảnh: {image_path}")
        return
    
    print(f"   📷 Loaded image: {image.shape}")
    
    # Test với CPU
    print("   🖥️  Processing với CPU...")
    start_time = time.time()
    gray_cpu = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_cpu = cv2.threshold(gray_cpu, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Morphological operations
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    morph_cpu = cv2.morphologyEx(binary_cpu, cv2.MORPH_CLOSE, kernel, iterations=2)
    cpu_time = time.time() - start_time
    print(f"      CPU processing time: {cpu_time:.3f}s")
    
    # Test với GPU (nếu có)
    gpu_support = GPUSupport()
    if gpu_support.is_gpu_available():
        print("   🎮 Processing với GPU...")
        try:
            start_time = time.time()
            
            # Upload lên GPU
            gpu_image = cv2.cuda_GpuMat()
            gpu_image.upload(image)
            
            # Convert to grayscale trên GPU
            gpu_gray = cv2.cuda.cvtColor(gpu_image, cv2.COLOR_BGR2GRAY)
            
            # Threshold trên GPU
            _, gpu_binary = cv2.cuda.threshold(gpu_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            
            # Morphological operations trên GPU
            gpu_morph = cv2.cuda.morphologyEx(gpu_binary, cv2.MORPH_CLOSE, kernel, iterations=2)
            
            # Download kết quả
            result_gpu = gpu_morph.download()
            
            gpu_time = time.time() - start_time
            print(f"      GPU processing time: {gpu_time:.3f}s")
            
            # So sánh kết quả
            diff = cv2.absdiff(morph_cpu, result_gpu)
            max_diff = np.max(diff)
            print(f"      Max difference CPU vs GPU: {max_diff}")
            
            if max_diff < 5:  # Threshold nhỏ cho phép sai số rounding
                print("      ✅ Kết quả CPU và GPU tương đương")
            else:
                print("      ⚠️  Có sự khác biệt giữa CPU và GPU")
            
            # Tính speedup
            if gpu_time > 0:
                speedup = cpu_time / gpu_time
                print(f"   📈 GPU Speedup: {speedup:.2f}x")
                
        except Exception as e:
            print(f"   ❌ Lỗi GPU processing: {e}")
    else:
        print("   ❌ GPU không khả dụng")

def main():
    print("🚀 Test GPU Support cho detect_row package")
    print("=" * 50)
    
    # Kiểm tra GPU requirements
    print("1️⃣ Kiểm tra GPU Requirements:")
    gpu_available = check_gpu_requirements()
    
    # Test OpenCV GPU
    print("\n2️⃣ Test OpenCV CUDA:")
    test_opencv_gpu()
    
    # Benchmark nếu có GPU
    if gpu_available:
        print("\n3️⃣ Benchmark Performance:")
        benchmark_cpu_vs_gpu()
        
        print("\n4️⃣ Test detect_row với GPU:")
        test_detect_row_with_gpu()
    else:
        print("\n💡 Hướng dẫn cài đặt GPU support:")
        print("   1. Cài NVIDIA GPU drivers mới nhất")
        print("   2. Cài CUDA Toolkit từ NVIDIA")
        print("   3. Gỡ opencv-python hiện tại:")
        print("      pip uninstall opencv-python opencv-contrib-python")
        print("   4. Cài opencv với CUDA support:")
        print("      pip install opencv-contrib-python")
        print("   5. Hoặc build OpenCV từ source với CUDA support")

if __name__ == "__main__":
    main() 