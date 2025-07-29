"""
Face Detection SDK
一个基于MediaPipe和YOLO的面部检测和分析SDK
"""

from .face_analyzer import FaceAnalyzer
from .models import DetectionResult, FaceMetrics
from .utils import ImageProcessor

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

__all__ = [
    "FaceAnalyzer",
    "DetectionResult", 
    "FaceMetrics",
    "ImageProcessor"
] 