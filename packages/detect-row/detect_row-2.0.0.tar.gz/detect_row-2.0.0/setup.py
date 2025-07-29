from setuptools import setup, find_packages
import os

# Đọc README
def read_readme():
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            return f.read()
    except:
        return "Hệ thống trích xuất bảng, hàng, cột hoàn chỉnh với AI và GPU support"

# Đọc requirements
def read_requirements():
    try:
        with open("requirements.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    except:
        return [
            "numpy>=1.19.0",
            "opencv-python>=4.5.0", 
            "matplotlib>=3.4.0",
            "pytesseract>=0.3.8",
            "Pillow>=8.2.0",
            "scikit-image>=0.18.0",
            "scipy>=1.7.0",
            "psutil>=5.8.0",
        ]

setup(
    name="detect-row",
    version="2.0.0",
    packages=find_packages(),
    include_package_data=True,
    
    install_requires=read_requirements(),
    
    # Optional dependencies
    extras_require={
        'gpu': [
            'torch>=1.9.0',
            'torchvision>=0.10.0',
        ],
        'dev': [
            'pytest>=6.0.0',
            'black>=21.0.0',
            'flake8>=3.9.0',
        ],
        'full': [
            'torch>=1.9.0',
            'torchvision>=0.10.0',
            'pytest>=6.0.0',
            'black>=21.0.0',
            'flake8>=3.9.0',
        ]
    },
    
    # Entry points cho command line
    entry_points={
        'console_scripts': [
            # Core extractors
            'detect-row-basic=detect_row.basic_row_extractor:main',
            'detect-row-advanced=detect_row.advanced_row_extractor:main',
            'detect-row-ocr=detect_row.tesseract_ocr_extractor:main',
            'detect-row-table=detect_row.advanced_table_extractor:main',
            'detect-row-column=detect_row.advanced_column_extractor:main',
            
            # Main workflows
            'detect-row-extract=extract_tables_and_columns:main',
            'detect-row-workflow=run_complete_workflow:main',
            
            # Utilities
            'detect-row-check=system_check:main',
            'detect-row-demo=quick_demo:main',
            'detect-row-helper=column_groups_helper:main',
            'detect-row-gpu-test=test_gpu_support:main',
            'detect-row-summary=show_results_summary:main',
        ],
    },
    
    # Package data
    package_data={
        'detect_row': [
            'templates/*.json',
            'configs/*.json',
        ],
        '': [
            '*.md',
            '*.txt',
            '*.json',
            '*.sh',
        ]
    },
    
    # Metadata
    author="AI Assistant & Row Detection Team",
    author_email="detect.row.team@gmail.com",
    description="Hệ thống trích xuất bảng, hàng, cột hoàn chỉnh với AI và GPU support",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    keywords="computer vision, table extraction, row detection, column extraction, OCR, vietnamese, image processing, AI, GPU, machine learning",
    url="https://github.com/detectrow/detect-row",
    project_urls={
        "Bug Reports": "https://github.com/detectrow/detect-row/issues",
        "Source": "https://github.com/detectrow/detect-row",
        "Documentation": "https://github.com/detectrow/detect-row/blob/main/COMPLETE_USAGE_GUIDE.md",
        "Quick Guide": "https://github.com/detectrow/detect-row/blob/main/HUONG_DAN_NHANH.md",
        "Vietnamese Guide": "https://github.com/detectrow/detect-row/blob/main/HUONG_DAN_SU_DUNG.md",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Information Technology",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: GPU :: NVIDIA CUDA",
        "Natural Language :: Vietnamese",
        "Natural Language :: English",
    ],
    python_requires=">=3.8",
    zip_safe=False,
    
    # Additional metadata
    platforms=['any'],
    license='MIT',
)
