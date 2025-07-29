"""
Face Detection SDK 演示脚本
"""
import cv2
import argparse
from .face_analyzer import FaceAnalyzer


def main():
    """主演示函数"""
    parser = argparse.ArgumentParser(description='Face Detection SDK Demo')
    parser.add_argument('--camera', type=int, default=0, help='摄像头索引')
    parser.add_argument('--mask-model', type=str, help='口罩检测模型路径')
    parser.add_argument('--confidence', type=float, default=0.7, help='检测置信度')
    parser.add_argument('--image', type=str, help='处理单张图像')
    
    args = parser.parse_args()
    
    # 初始化分析器
    analyzer = FaceAnalyzer(
        mask_model_path=args.mask_model,
        min_detection_confidence=args.confidence
    )
    
    try:
        if args.image:
            # 处理单张图像
            process_single_image(analyzer, args.image)
        else:
            # 实时摄像头处理
            process_camera(analyzer, args.camera)
    finally:
        analyzer.release()


def process_single_image(analyzer: FaceAnalyzer, image_path: str):
    """处理单张图像"""
    print(f"处理图像: {image_path}")
    
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"无法读取图像: {image_path}")
        return
    
    results = analyzer.analyze_frame(frame)
    
    if not results:
        print("未检测到人脸")
        return
    
    # 显示结果
    for i, result in enumerate(results):
        print(f"\n=== 人脸 {i+1} ===")
        print(f"边界框: {result.bbox}")
        print(f"姿态: Yaw={result.pose.yaw:.1f}°, Pitch={result.pose.pitch:.1f}°, Roll={result.pose.roll:.1f}°")
        print(f"口罩: {'是' if result.metrics.has_mask else '否'}")
        print(f"稳定性: {'稳定' if result.is_stable else '不稳定'}")
        print(f"距离: {result.distance}cm")
        
        # 获取质量评分
        scores = analyzer.get_quality_scores(result.metrics)
        print(f"质量评分:")
        print(f"  清晰度: {scores['sharpness_score']}/100")
        print(f"  亮度: {scores['brightness_score']}/100")
        print(f"  对比度: {scores['contrast_score']}/100")
        
        # 绘制边界框和信息
        x1, y1, x2, y2 = result.bbox
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        # 显示口罩信息
        mask_text = f"Mask: {'Yes' if result.metrics.has_mask else 'No'}"
        cv2.putText(frame, mask_text, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # 显示姿态信息
        pose_text = f"Y:{result.pose.yaw:.1f} P:{result.pose.pitch:.1f} R:{result.pose.roll:.1f}"
        cv2.putText(frame, pose_text, (x1, y2+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # 显示距离信息
        if result.distance:
            distance_text = f"Distance: {result.distance}cm"
            cv2.putText(frame, distance_text, (x1, y2+40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    # 显示图像
    cv2.imshow("Face Detection Result", frame)
    print("\n按任意键关闭窗口...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def process_camera(analyzer: FaceAnalyzer, camera_index: int):
    """处理摄像头实时流"""
    print(f"启动摄像头 {camera_index}...")
    
    cap = cv2.VideoCapture(camera_index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    if not cap.isOpened():
        print(f"无法打开摄像头 {camera_index}")
        return
    
    print("按 'q' 退出，按 's' 保存当前帧")
    
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print("无法读取摄像头帧")
            break
        
        # 分析帧
        results = analyzer.analyze_frame(frame)
        
        # 显示结果
        for result in results:
            x1, y1, x2, y2 = result.bbox
            
            # 根据状态选择颜色
            color = (0, 255, 0) if result.is_stable else (0, 0, 255)
            
            # 绘制边界框
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            
            # 显示标签
            label = f"{'Mask' if result.metrics.has_mask else 'No Mask'}{' (Stable)' if result.is_stable else ''}"
            cv2.putText(frame, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            
            # 显示姿态信息
            pose_text = f"Y:{result.pose.yaw:.1f} P:{result.pose.pitch:.1f} R:{result.pose.roll:.1f}"
            cv2.putText(frame, pose_text, (x1, y2+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # 显示距离信息
            if result.distance:
                distance_text = f"D:{result.distance}cm"
                cv2.putText(frame, distance_text, (x1, y2+40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # 显示FPS
        fps = cap.get(cv2.CAP_PROP_FPS)
        cv2.putText(frame, f'FPS: {fps:.1f}', (10, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # 每5帧打印一次详细信息
        if frame_count % 5 == 0 and results:
            print(f"\n=== 帧 {frame_count} ===")
            for i, result in enumerate(results):
                print(f"人脸 {i+1}: 稳定={result.is_stable}, 口罩={result.metrics.has_mask}, 距离={result.distance}cm")
        
        cv2.imshow("Face Detection Demo", frame)
        frame_count += 1
        
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break
        elif key & 0xFF == ord('s'):
            # 保存当前帧
            import os
            from datetime import datetime
            save_dir = "saved_frames"
            os.makedirs(save_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join(save_dir, f"frame_{timestamp}.jpg")
            cv2.imwrite(save_path, frame)
            print(f"帧已保存至: {save_path}")
    
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main() 