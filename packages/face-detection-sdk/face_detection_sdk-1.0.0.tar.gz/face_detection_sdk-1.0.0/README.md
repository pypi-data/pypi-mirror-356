# Face Detection SDK

一个基于MediaPipe和YOLO的面部检测和分析SDK，提供面部检测、姿态估计、质量评估等功能。

## 功能特性

- 🎯 **面部检测**: 基于MediaPipe的高精度面部检测
- 📐 **姿态估计**: 实时头部姿态（偏航、俯仰、滚转）估计
- 🎭 **口罩检测**: 基于YOLO的口罩佩戴检测
- 📊 **质量评估**: 图像清晰度、亮度、对比度评分
- 📏 **距离估计**: 基于瞳距的单目测距
- 🔄 **稳定性检测**: 面部运动稳定性分析
- 🌟 **图像增强**: 自动人脸亮度增强和背景处理

## 安装

```bash
pip install face-detection-sdk
```

## 快速开始

### 基本使用

```python
import cv2
from face_detection_sdk import FaceAnalyzer

# 初始化分析器
analyzer = FaceAnalyzer(
    mask_model_path="path/to/your/mask_model.pt",  # 可选
    min_detection_confidence=0.7
)

# 读取图像
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # 分析帧
    results = analyzer.analyze_frame(frame)
    
    # 处理结果
    for result in results:
        print(f"检测到人脸: {result.bbox}")
        print(f"姿态: Yaw={result.pose.yaw:.1f}°, Pitch={result.pose.pitch:.1f}°, Roll={result.pose.roll:.1f}°")
        print(f"口罩: {'是' if result.metrics.has_mask else '否'}")
        print(f"稳定性: {'稳定' if result.is_stable else '不稳定'}")
        print(f"距离: {result.distance}cm")
        
        # 获取质量评分
        scores = analyzer.get_quality_scores(result.metrics)
        print(f"质量评分: 清晰度={scores['sharpness_score']}, 亮度={scores['brightness_score']}, 对比度={scores['contrast_score']}")
    
    # 显示结果
    cv2.imshow('Face Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
analyzer.release()
```

### 高级使用

```python
from face_detection_sdk import FaceAnalyzer, DetectionResult
import cv2
import numpy as np

# 自定义参数初始化
analyzer = FaceAnalyzer(
    mask_model_path="best.pt",
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8,
    stable_frames_threshold=5,
    motion_blur_threshold=80
)

def process_image(image_path: str):
    """处理单张图像"""
    frame = cv2.imread(image_path)
    results = analyzer.analyze_frame(frame)
    
    for result in results:
        # 绘制边界框
        x1, y1, x2, y2 = result.bbox
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        # 显示信息
        info = f"Mask: {'Yes' if result.metrics.has_mask else 'No'}"
        cv2.putText(frame, info, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # 显示姿态信息
        pose_info = f"Y:{result.pose.yaw:.1f} P:{result.pose.pitch:.1f} R:{result.pose.roll:.1f}"
        cv2.putText(frame, pose_info, (x1, y2+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    return frame, results

# 使用示例
image_path = "test_image.jpg"
processed_frame, detection_results = process_image(image_path)
cv2.imshow("Processed Image", processed_frame)
cv2.waitKey(0)
```

## API 文档

### FaceAnalyzer

主要的分析器类，提供面部检测和分析功能。

#### 初始化参数

- `mask_model_path` (str, optional): YOLO口罩检测模型路径
- `min_detection_confidence` (float): 最小检测置信度，默认0.7
- `min_tracking_confidence` (float): 最小跟踪置信度，默认0.7
- `stable_frames_threshold` (int): 稳定帧数阈值，默认3
- `motion_blur_threshold` (float): 运动模糊阈值，默认100

#### 主要方法

- `analyze_frame(frame)`: 分析单帧图像，返回检测结果列表
- `get_quality_scores(metrics)`: 获取质量评分
- `release()`: 释放资源

### DetectionResult

检测结果数据类，包含所有检测信息。

#### 属性

- `bbox`: 边界框坐标 (x1, y1, x2, y2)
- `pose`: 姿态估计结果 (PoseEstimate)
- `metrics`: 面部指标 (FaceMetrics)
- `is_stable`: 是否稳定
- `distance`: 估计距离 (cm)
- `landmarks`: 面部关键点列表

### FaceMetrics

面部指标数据类。

#### 属性

- `sharpness`: 清晰度值
- `brightness`: 亮度值
- `contrast`: 对比度值
- `has_mask`: 是否戴口罩
- `motion_blur`: 运动模糊值

## 依赖要求

- Python >= 3.7
- OpenCV >= 4.5.0
- NumPy >= 1.19.0
- MediaPipe >= 0.8.0
- Ultralytics >= 8.0.0
- SciPy >= 1.7.0
- Matplotlib >= 3.3.0

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 更新日志

### v1.0.0
- 初始版本发布
- 支持面部检测和姿态估计
- 支持口罩检测
- 支持图像质量评估
- 支持距离估计和稳定性检测 