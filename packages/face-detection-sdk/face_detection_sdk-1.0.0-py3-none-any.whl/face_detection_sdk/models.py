"""
数据模型定义
"""
from dataclasses import dataclass
from typing import Optional, Tuple, List
import numpy as np


@dataclass
class FaceMetrics:
    """面部检测指标"""
    sharpness: float
    brightness: float
    contrast: float
    has_mask: bool
    motion_blur: float
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'sharpness': self.sharpness,
            'brightness': self.brightness,
            'contrast': self.contrast,
            'has_mask': self.has_mask,
            'motion_blur': self.motion_blur
        }


@dataclass
class PoseEstimate:
    """姿态估计结果"""
    yaw: float
    pitch: float
    roll: float
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'yaw': self.yaw,
            'pitch': self.pitch,
            'roll': self.roll
        }


@dataclass
class DetectionResult:
    """检测结果"""
    bbox: Tuple[int, int, int, int]  # (x1, y1, x2, y2)
    pose: PoseEstimate
    metrics: FaceMetrics
    is_stable: bool
    distance: Optional[float] = None
    landmarks: Optional[List[Tuple[int, int]]] = None
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'bbox': self.bbox,
            'pose': self.pose.to_dict(),
            'metrics': self.metrics.to_dict(),
            'is_stable': self.is_stable,
            'distance': self.distance,
            'landmarks': self.landmarks
        } 