"""
GPU Support Module cho detect_row package
Cung cấp các chức năng xử lý ảnh được tăng tốc bằng GPU
"""

import cv2
import numpy as np
import logging
from typing import Optional, Tuple, List
import os

logger = logging.getLogger(__name__)

class GPUSupport:
    """Lớp hỗ trợ GPU cho xử lý ảnh"""
    
    def __init__(self):
        self.gpu_available = self._check_gpu_support()
        self.gpu_device = None
        if self.gpu_available:
            self._initialize_gpu()
    
    def _check_gpu_support(self) -> bool:
        """Kiểm tra xem OpenCV có hỗ trợ CUDA không"""
        try:
            # Kiểm tra OpenCV có build với CUDA không
            if not hasattr(cv2, 'cuda'):
                logger.warning("OpenCV không được build với CUDA support")
                return False
            
            # Kiểm tra có GPU device không
            device_count = cv2.cuda.getCudaEnabledDeviceCount()
            if device_count == 0:
                logger.warning("Không tìm thấy GPU device hỗ trợ CUDA")
                return False
            
            logger.info(f"Tìm thấy {device_count} GPU device(s) hỗ trợ CUDA")
            return True
            
        except Exception as e:
            logger.warning(f"Lỗi khi kiểm tra GPU support: {e}")
            return False
    
    def _initialize_gpu(self):
        """Khởi tạo GPU device"""
        try:
            # Lấy thông tin GPU
            device_info = cv2.cuda.printCudaDeviceInfo(0)
            logger.info("GPU được khởi tạo thành công")
            
            # Tạo CUDA stream
            self.stream = cv2.cuda_Stream()
            
        except Exception as e:
            logger.error(f"Lỗi khi khởi tạo GPU: {e}")
            self.gpu_available = False
    
    def is_gpu_available(self) -> bool:
        """Kiểm tra GPU có khả dụng không"""
        return self.gpu_available
    
    def get_gpu_info(self) -> dict:
        """Lấy thông tin GPU"""
        if not self.gpu_available:
            return {"gpu_available": False}
        
        try:
            device_count = cv2.cuda.getCudaEnabledDeviceCount()
            device_info = {
                "gpu_available": True,
                "device_count": device_count,
                "current_device": cv2.cuda.getDevice()
            }
            return device_info
        except Exception as e:
            logger.error(f"Lỗi khi lấy thông tin GPU: {e}")
            return {"gpu_available": False, "error": str(e)}


class GPUImageProcessor:
    """Lớp xử lý ảnh trên GPU"""
    
    def __init__(self):
        self.gpu_support = GPUSupport()
        self.stream = None
        if self.gpu_support.is_gpu_available():
            self.stream = cv2.cuda_Stream()
    
    def convert_to_gray_gpu(self, image: np.ndarray) -> np.ndarray:
        """Chuyển ảnh sang grayscale trên GPU"""
        if not self.gpu_support.is_gpu_available():
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        try:
            # Upload ảnh lên GPU
            gpu_image = cv2.cuda_GpuMat()
            gpu_image.upload(image)
            
            # Chuyển đổi màu trên GPU
            gpu_gray = cv2.cuda.cvtColor(gpu_image, cv2.COLOR_BGR2GRAY)
            
            # Download kết quả về CPU
            result = gpu_gray.download()
            return result
            
        except Exception as e:
            logger.warning(f"Lỗi GPU processing, fallback to CPU: {e}")
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    def threshold_gpu(self, image: np.ndarray, thresh_type: int = cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU) -> Tuple[float, np.ndarray]:
        """Threshold ảnh trên GPU"""
        if not self.gpu_support.is_gpu_available():
            return cv2.threshold(image, 0, 255, thresh_type)
        
        try:
            # Upload ảnh lên GPU
            gpu_image = cv2.cuda_GpuMat()
            gpu_image.upload(image)
            
            # Threshold trên GPU
            thresh_val, gpu_binary = cv2.cuda.threshold(gpu_image, 0, 255, thresh_type)
            
            # Download kết quả về CPU
            result = gpu_binary.download()
            return thresh_val, result
            
        except Exception as e:
            logger.warning(f"Lỗi GPU processing, fallback to CPU: {e}")
            return cv2.threshold(image, 0, 255, thresh_type)
    
    def morphology_gpu(self, image: np.ndarray, operation: int, kernel: np.ndarray, iterations: int = 1) -> np.ndarray:
        """Morphological operations trên GPU"""
        if not self.gpu_support.is_gpu_available():
            return cv2.morphologyEx(image, operation, kernel, iterations=iterations)
        
        try:
            # Upload ảnh và kernel lên GPU
            gpu_image = cv2.cuda_GpuMat()
            gpu_image.upload(image)
            
            # Morphological operations trên GPU
            gpu_result = cv2.cuda.morphologyEx(gpu_image, operation, kernel, iterations=iterations)
            
            # Download kết quả về CPU
            result = gpu_result.download()
            return result
            
        except Exception as e:
            logger.warning(f"Lỗi GPU processing, fallback to CPU: {e}")
            return cv2.morphologyEx(image, operation, kernel, iterations=iterations)
    
    def resize_gpu(self, image: np.ndarray, size: Tuple[int, int], interpolation: int = cv2.INTER_LINEAR) -> np.ndarray:
        """Resize ảnh trên GPU"""
        if not self.gpu_support.is_gpu_available():
            return cv2.resize(image, size, interpolation=interpolation)
        
        try:
            # Upload ảnh lên GPU
            gpu_image = cv2.cuda_GpuMat()
            gpu_image.upload(image)
            
            # Resize trên GPU
            gpu_result = cv2.cuda.resize(gpu_image, size, interpolation=interpolation)
            
            # Download kết quả về CPU
            result = gpu_result.download()
            return result
            
        except Exception as e:
            logger.warning(f"Lỗi GPU processing, fallback to CPU: {e}")
            return cv2.resize(image, size, interpolation=interpolation)
    
    def gaussian_blur_gpu(self, image: np.ndarray, ksize: Tuple[int, int], sigmaX: float) -> np.ndarray:
        """Gaussian blur trên GPU"""
        if not self.gpu_support.is_gpu_available():
            return cv2.GaussianBlur(image, ksize, sigmaX)
        
        try:
            # Upload ảnh lên GPU
            gpu_image = cv2.cuda_GpuMat()
            gpu_image.upload(image)
            
            # Gaussian blur trên GPU
            gpu_result = cv2.cuda.GaussianBlur(gpu_image, ksize, sigmaX)
            
            # Download kết quả về CPU
            result = gpu_result.download()
            return result
            
        except Exception as e:
            logger.warning(f"Lỗi GPU processing, fallback to CPU: {e}")
            return cv2.GaussianBlur(image, ksize, sigmaX)


def check_gpu_requirements():
    """Kiểm tra yêu cầu GPU và đưa ra hướng dẫn cài đặt"""
    gpu_support = GPUSupport()
    
    if gpu_support.is_gpu_available():
        info = gpu_support.get_gpu_info()
        print("✅ GPU Support: Available")
        print(f"   Device count: {info.get('device_count', 'N/A')}")
        print(f"   Current device: {info.get('current_device', 'N/A')}")
        return True
    else:
        print("❌ GPU Support: Not Available")
        print("\n🔧 Để sử dụng GPU, bạn cần:")
        print("1. Cài đặt NVIDIA GPU drivers")
        print("2. Cài đặt CUDA Toolkit")
        print("3. Cài đặt OpenCV với CUDA support:")
        print("   pip uninstall opencv-python")
        print("   pip install opencv-contrib-python")
        print("   # Hoặc build OpenCV từ source với CUDA support")
        print("\n📖 Hướng dẫn chi tiết:")
        print("   https://docs.opencv.org/4.x/d6/d15/tutorial_building_tegra_cuda.html")
        return False


if __name__ == "__main__":
    check_gpu_requirements() 