"""
Face Detection SDK Setup
"""
from setuptools import setup, find_packages
import os

# 读取README文件
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

# 读取requirements文件
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="face-detection-sdk",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="一个基于MediaPipe和YOLO的面部检测和分析SDK",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/face-detection-sdk",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
    },
    include_package_data=True,
    package_data={
        "face_detection_sdk": ["*.pt", "*.pkl", "*.json"],
    },
    keywords="face detection, computer vision, mediapipe, yolo, pose estimation",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/face-detection-sdk/issues",
        "Source": "https://github.com/yourusername/face-detection-sdk",
        "Documentation": "https://github.com/yourusername/face-detection-sdk/blob/main/README.md",
    },
) 