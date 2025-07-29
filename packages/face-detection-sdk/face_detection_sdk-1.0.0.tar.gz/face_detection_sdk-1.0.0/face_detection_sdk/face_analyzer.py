"""
面部检测和分析器
"""
import cv2
import numpy as np
import mediapipe as mp
from ultralytics import YOLO
from collections import deque
from typing import Optional, List, Tuple
import warnings

from .models import DetectionResult, FaceMetrics, PoseEstimate
from .utils import ImageProcessor, ScoreCalculator, PoseEstimator

# 忽略MediaPipe的特定警告
warnings.filterwarnings("ignore", category=UserWarning)


class FaceAnalyzer:
    """面部检测和分析器"""
    
    def __init__(self, 
                 mask_model_path: Optional[str] = None,
                 min_detection_confidence: float = 0.7,
                 min_tracking_confidence: float = 0.7,
                 stable_frames_threshold: int = 3,
                 motion_blur_threshold: float = 100):
        """
        初始化面部分析器
        
        Args:
            mask_model_path: 口罩检测模型路径
            min_detection_confidence: 最小检测置信度
            min_tracking_confidence: 最小跟踪置信度
            stable_frames_threshold: 稳定帧数阈值
            motion_blur_threshold: 运动模糊阈值
        """
        # 初始化MediaPipe模型
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_face_mesh = mp.solutions.face_mesh
        
        # 创建人脸检测器实例
        self.face_detection = self.mp_face_detection.FaceDetection(
            min_detection_confidence=min_detection_confidence,
            model_selection=1
        )
        
        # 创建面部网格检测器实例
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        
        # 加载YOLO口罩检测模型
        if mask_model_path:
            self.mask_model = YOLO(mask_model_path)
        else:
            self.mask_model = None
        
        # 参数设置
        self.stable_frames_threshold = stable_frames_threshold
        self.motion_blur_threshold = motion_blur_threshold
        
        # 初始化状态
        self.face_history = deque(maxlen=5)
        self.prev_gray = None
        
    def analyze_frame(self, frame: np.ndarray) -> List[DetectionResult]:
        """
        分析单帧图像
        
        Args:
            frame: 输入图像帧
            
        Returns:
            检测结果列表
        """
        results = []
        
        # 运动模糊检测
        current_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        motion_blur = ImageProcessor.detect_motion_blur(current_gray, self.prev_gray)
        self.prev_gray = current_gray
        
        # 预处理帧
        processed_frame = ImageProcessor.darken_background(frame)
        rgb_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
        
        # 人脸检测
        face_results = self.face_detection.process(rgb_frame)
        
        if face_results.detections:
            for detection in face_results.detections:
                bbox = detection.location_data.relative_bounding_box
                h, w = frame.shape[:2]
                x1 = int(bbox.xmin * w)
                y1 = int(bbox.ymin * h)
                x2 = int((bbox.xmin + bbox.width) * w)
                y2 = int((bbox.ymin + bbox.height) * h)
                x1, y1 = max(0, x1), max(0, y1)
                x2, y2 = min(w, x2), min(h, y2)
                
                if (x2 - x1) < 50 or (y2 - y1) < 50:
                    continue
                
                # 检查稳定性
                current_bbox = (x1, y1, x2, y2)
                self.face_history.append(current_bbox)
                is_stable = self._is_face_stable(current_bbox)
                
                # 提取人脸区域
                face_roi = processed_frame[y1:y2, x1:x2]
                if face_roi.size == 0:
                    continue
                
                # 增强人脸亮度
                enhanced_face = ImageProcessor.enhance_face_brightness(face_roi)
                processed_frame[y1:y2, x1:x2] = enhanced_face
                
                # 面部网格检测
                mesh_results = self.face_mesh.process(rgb_frame)
                if mesh_results.multi_face_landmarks:
                    landmarks = []
                    for landmark in mesh_results.multi_face_landmarks[0].landmark:
                        landmarks.append((int(landmark.x * w), int(landmark.y * h)))
                    
                    # 姿态估计
                    yaw, pitch, roll = PoseEstimator.estimate_pose(landmarks, frame.shape)
                    pose = PoseEstimate(yaw=yaw, pitch=pitch, roll=roll)
                    
                    # 距离估计
                    distance = PoseEstimator.estimate_distance(landmarks, frame.shape[1])
                    
                    # 分析面部指标
                    metrics = self._analyze_face_metrics(frame, face_roi, motion_blur)
                    
                    # 创建检测结果
                    result = DetectionResult(
                        bbox=current_bbox,
                        pose=pose,
                        metrics=metrics,
                        is_stable=is_stable,
                        distance=distance,
                        landmarks=landmarks
                    )
                    
                    results.append(result)
        
        return results
    
    def _is_face_stable(self, current_bbox: Tuple[int, int, int, int]) -> bool:
        """判断人脸是否稳定"""
        if len(self.face_history) < self.stable_frames_threshold:
            return False
        
        movements = []
        for prev_bbox in self.face_history:
            dx = abs(current_bbox[0] - prev_bbox[0]) / current_bbox[2]
            dy = abs(current_bbox[1] - prev_bbox[1]) / current_bbox[3]
            movements.append(dx + dy)
        
        return np.mean(movements) < 0.1
    
    def _analyze_face_metrics(self, frame: np.ndarray, face_roi: np.ndarray, 
                            motion_blur: float) -> FaceMetrics:
        """分析面部指标"""
        # 计算清晰度
        sharpness = ImageProcessor.calculate_sharpness(face_roi)
        
        # 计算亮度
        gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
        brightness = float(np.mean(gray))
        
        # 计算对比度
        contrast, _ = ScoreCalculator.contrast_score(gray)
        
        # 口罩检测
        has_mask = False
        if self.mask_model:
            try:
                mask_results = self.mask_model.predict(face_roi, imgsz=160, conf=0.6, verbose=False)
                has_mask = any(box.cls == 0 for box in mask_results[0].boxes) if mask_results[0].boxes else False
            except:
                has_mask = False
        
        return FaceMetrics(
            sharpness=sharpness,
            brightness=brightness,
            contrast=contrast,
            has_mask=has_mask,
            motion_blur=motion_blur
        )
    
    def get_quality_scores(self, metrics: FaceMetrics) -> dict:
        """获取质量评分"""
        return {
            'sharpness_score': ScoreCalculator.sharpness_score(metrics.sharpness),
            'brightness_score': ScoreCalculator.brightness_score(metrics.brightness),
            'contrast_score': metrics.contrast
        }
    
    def release(self):
        """释放资源"""
        self.face_detection.close()
        self.face_mesh.close() 