"""
Face Analyzer 测试
"""
import pytest
import numpy as np
import cv2
from face_detection_sdk import FaceAnalyzer, DetectionResult, FaceMetrics


class TestFaceAnalyzer:
    """FaceAnalyzer 测试类"""
    
    def test_initialization(self):
        """测试初始化"""
        analyzer = FaceAnalyzer()
        assert analyzer is not None
        assert analyzer.face_detection is not None
        assert analyzer.face_mesh is not None
        analyzer.release()
    
    def test_initialization_with_mask_model(self):
        """测试带口罩模型的初始化"""
        # 注意：这里需要实际的模型文件才能测试
        analyzer = FaceAnalyzer(mask_model_path=None)  # 暂时不提供模型
        assert analyzer is not None
        analyzer.release()
    
    def test_analyze_empty_frame(self):
        """测试空帧分析"""
        analyzer = FaceAnalyzer()
        empty_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        results = analyzer.analyze_frame(empty_frame)
        assert isinstance(results, list)
        assert len(results) == 0
        analyzer.release()
    
    def test_analyze_frame_with_face(self):
        """测试包含人脸的帧分析"""
        analyzer = FaceAnalyzer()
        
        # 创建一个简单的测试图像（这里只是示例，实际需要真实的人脸图像）
        test_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        results = analyzer.analyze_frame(test_frame)
        
        assert isinstance(results, list)
        # 注意：随机图像可能不会检测到人脸，所以结果可能为空
        analyzer.release()


class TestFaceMetrics:
    """FaceMetrics 测试类"""
    
    def test_face_metrics_creation(self):
        """测试FaceMetrics创建"""
        metrics = FaceMetrics(
            sharpness=50.0,
            brightness=127.0,
            contrast=75.0,
            has_mask=False,
            motion_blur=10.0
        )
        
        assert metrics.sharpness == 50.0
        assert metrics.brightness == 127.0
        assert metrics.contrast == 75.0
        assert metrics.has_mask is False
        assert metrics.motion_blur == 10.0
    
    def test_face_metrics_to_dict(self):
        """测试FaceMetrics转字典"""
        metrics = FaceMetrics(
            sharpness=50.0,
            brightness=127.0,
            contrast=75.0,
            has_mask=True,
            motion_blur=10.0
        )
        
        metrics_dict = metrics.to_dict()
        assert isinstance(metrics_dict, dict)
        assert metrics_dict['sharpness'] == 50.0
        assert metrics_dict['has_mask'] is True


class TestDetectionResult:
    """DetectionResult 测试类"""
    
    def test_detection_result_creation(self):
        """测试DetectionResult创建"""
        from face_detection_sdk import PoseEstimate
        
        pose = PoseEstimate(yaw=0.0, pitch=0.0, roll=0.0)
        metrics = FaceMetrics(
            sharpness=50.0,
            brightness=127.0,
            contrast=75.0,
            has_mask=False,
            motion_blur=10.0
        )
        
        result = DetectionResult(
            bbox=(100, 100, 200, 200),
            pose=pose,
            metrics=metrics,
            is_stable=True,
            distance=50.0
        )
        
        assert result.bbox == (100, 100, 200, 200)
        assert result.is_stable is True
        assert result.distance == 50.0
        assert result.pose == pose
        assert result.metrics == metrics
    
    def test_detection_result_to_dict(self):
        """测试DetectionResult转字典"""
        from face_detection_sdk import PoseEstimate
        
        pose = PoseEstimate(yaw=10.0, pitch=5.0, roll=2.0)
        metrics = FaceMetrics(
            sharpness=50.0,
            brightness=127.0,
            contrast=75.0,
            has_mask=True,
            motion_blur=10.0
        )
        
        result = DetectionResult(
            bbox=(100, 100, 200, 200),
            pose=pose,
            metrics=metrics,
            is_stable=True,
            distance=50.0
        )
        
        result_dict = result.to_dict()
        assert isinstance(result_dict, dict)
        assert result_dict['bbox'] == (100, 100, 200, 200)
        assert result_dict['is_stable'] is True
        assert result_dict['distance'] == 50.0
        assert 'pose' in result_dict
        assert 'metrics' in result_dict


if __name__ == "__main__":
    pytest.main([__file__]) 