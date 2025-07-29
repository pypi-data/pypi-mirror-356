"""
工具函数模块
"""
import cv2
import numpy as np
from typing import Tuple, Optional
from .models import FaceMetrics


class ImageProcessor:
    """图像处理工具类"""
    
    @staticmethod
    def calculate_sharpness(image: np.ndarray) -> float:
        """计算图像清晰度"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.Laplacian(gray, cv2.CV_64F).var()
    
    @staticmethod
    def detect_motion_blur(current_gray: np.ndarray, prev_gray: Optional[np.ndarray]) -> float:
        """检测运动模糊"""
        if prev_gray is None:
            return 0.0
        try:
            flow = cv2.calcOpticalFlowFarneback(
                prev_gray, current_gray,
                None, 0.5, 3, 15, 3, 5, 1.2, 0
            )
            magnitude = np.sqrt(flow[..., 0] ** 2 + flow[..., 1] ** 2)
            return float(np.mean(magnitude))
        except:
            return 0.0
    
    @staticmethod
    def enhance_face_brightness(face_roi: np.ndarray, gamma: float = 1.5, 
                              clahe_enabled: bool = True) -> np.ndarray:
        """增强人脸亮度"""
        lab = cv2.cvtColor(face_roi, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)

        if clahe_enabled:
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
            l = clahe.apply(l)

        l_gamma = np.power(l / 255.0, 1.0 / gamma) * 255
        l_gamma = np.clip(l_gamma, 0, 255).astype(np.uint8)
        enhanced_lab = cv2.merge((l_gamma, a, b))
        return cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
    
    @staticmethod
    def darken_background(frame: np.ndarray, factor: float = 0.7) -> np.ndarray:
        """使背景变暗"""
        blurred = cv2.GaussianBlur(frame, (0, 0), 3)
        frame = cv2.addWeighted(frame, 0.7, blurred, 0.3, 0)
        return np.clip(frame.astype(np.float32) * factor, 0, 255).astype(np.uint8)


class ScoreCalculator:
    """评分计算器"""
    
    @staticmethod
    def sharpness_score(sharpness_value: float) -> float:
        """清晰度评分（基于拉普拉斯梯度）"""
        score = min(100, max(0, sharpness_value / 10))
        return round(score, 2)
    
    @staticmethod
    def brightness_score(brightness_value: float) -> float:
        """亮度评分（基于灰度图像的亮度值）"""
        if brightness_value < 30:
            score = 0
        elif brightness_value > 220:
            score = 0
        else:
            score = 100 - abs(brightness_value - 127.5) / 127.5 * 100
        return round(max(0, score), 2)
    
    @staticmethod
    def contrast_score(gray_image: np.ndarray) -> Tuple[float, float]:
        """对比度评分（基于灰度图像的标准差）"""
        std = np.std(gray_image)
        if std < 20:
            score = 0
        elif std > 100:
            score = 100
        else:
            score = (std - 20) / 80 * 100
        return round(max(0, min(100, score))), round(std, 2)


class PoseEstimator:
    """姿态估计器"""
    
    @staticmethod
    def estimate_pose(landmarks: list, frame_shape: Tuple[int, int]) -> Tuple[float, float, float]:
        """估计头部姿态"""
        try:
            image_points = np.array([
                landmarks[4], landmarks[152], landmarks[133],
                landmarks[362], landmarks[61], landmarks[291]
            ], dtype="double")

            model_points = np.array([
                (0.0, 0.0, 0.0), (0.0, -330.0, -65.0),
                (-165.0, 170.0, -135.0), (165.0, 170.0, -135.0),
                (-150.0, -150.0, -125.0), (150.0, -150.0, -125.0)
            ])

            focal_length = frame_shape[1]
            center = (frame_shape[1] / 2, frame_shape[0] / 2)
            camera_matrix = np.array([
                [focal_length, 0, center[0]],
                [0, focal_length, center[1]],
                [0, 0, 1]
            ], dtype="double")

            dist_coeffs = np.zeros((4, 1))
            _, rotation_vector, _ = cv2.solvePnP(
                model_points, image_points,
                camera_matrix, dist_coeffs,
                flags=cv2.SOLVEPNP_ITERATIVE
            )

            from scipy.spatial.transform import Rotation
            r = Rotation.from_rotvec(rotation_vector.reshape(3))
            yaw, pitch, roll = r.as_euler('yxz', degrees=True)
            return float(yaw), float(pitch), float(roll)
        except:
            return 0.0, 0.0, 0.0
    
    @staticmethod
    def estimate_distance(landmarks: list, frame_width: int, 
                         avg_pupil_distance_mm: float = 63) -> Optional[float]:
        """单目测距（基于瞳距）"""
        try:
            # 获取左右眼中心点
            left_eye = landmarks[133]  # 左眼中心
            right_eye = landmarks[362]  # 右眼中心

            # 计算像素距离
            pixel_distance = np.sqrt((right_eye[0] - left_eye[0]) ** 2 + 
                                   (right_eye[1] - left_eye[1]) ** 2)

            # 估算焦距（假设标准距离为50cm时的瞳距像素）
            focal_length = (pixel_distance * 500) / avg_pupil_distance_mm

            # 计算当前距离（mm）
            distance_mm = (avg_pupil_distance_mm * focal_length) / pixel_distance
            distance_cm = distance_mm / 10

            return round(distance_cm, 1)
        except:
            return None 