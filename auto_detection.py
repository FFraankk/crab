import cv2
from ultralytics import YOLO

# --- 1. 定义你的自定义模型路径和类别名称 ---
# 请将 'path/to/your/yolov11_custom_model.pt' 替换为你实际的模型文件路径
MODEL_PATH = 'best.pt'

# 请确保这里的类别名称和顺序与你模型训练时定义的保持一致
# 例如，如果你的模型在训练时将 'Mark' 定义为类别0，'Empty' 定义为类别1
CLASS_NAMES = ["Mark", "Empty"] # 根据你的模型实际类别调整，注意大小写

# --- 2. 加载YOLOv11自定义模型 ---
try:
    model = YOLO(MODEL_PATH)
    print(f"成功加载模型: {MODEL_PATH}")
except Exception as e:
    print(f"加载模型失败: {e}")
    print("请检查模型路径是否正确，以及模型文件是否完整。")
    exit() # 如果模型加载失败，则退出程序

# --- 3. 定义处理检测结果的函数 ---
def process_detections(results, class_names):
    """
    根据YOLO模型的检测结果，打印相应的状态信息。
    """
    detected_labels = []
    # results[0] 通常包含单张图像的检测结果
    if results and results[0].boxes:
        for box in results[0].boxes:
            # 确保置信度高于某个阈值（例如0.5），以减少误报
            if box.conf > 0.5: # 增加一个置信度阈值判断，提高识别准确性
                class_id = int(box.cls)
                if class_id < len(class_names):
                    detected_labels.append(class_names[class_id])

    # 注意：这里将 "marked" 和 "empty" 改为 "Mark" 和 "Empty"，与 CLASS_NAMES 中的定义一致
    mark_count = detected_labels.count("Mark")
    empty_count = detected_labels.count("Empty")
    total_relevant_detections = mark_count + empty_count

    if mark_count > 0 and empty_count == 0:
        print("marked") # 输出仍然保持小写，符合你的需求
    elif empty_count > 0 and mark_count == 0:
        print("empty") # 输出仍然保持小写
    elif total_relevant_detections > 1:
        # 识别到多个 'Mark' 或 'Empty'，或两者兼有
        print("请拿走一个")
    elif total_relevant_detections == 0 and len(detected_labels) == 0:
        # 没有检测到 'Mark' 或 'Empty'，也没有检测到其他任何东西
        # 你的需求是“什么都不要管”，所以这里留空
        pass
    else:
        # 识别到其他类别的物体（如果你的模型训练了除了Mark和Empty以外的类别）
        # 并且这些其他物体不影响Mark和Empty的判断逻辑时，也符合“什么都不要管”
        pass


# --- 4. 示例：从视频文件实时检测 ---
# 更改为你的视频文件路径
cap = cv2.VideoCapture("test_source/output_video.avi")

if not cap.isOpened():
    print("无法打开视频文件，请检查文件路径是否正确或文件是否损坏。")
    exit()

print("\n--- 开始从视频文件检测，按 'q' 键退出 ---")

while True:
    ret, frame = cap.read()
    if not ret:
        print("视频播放结束或无法接收帧，正在退出...")
        break

    # 对每一帧运行YOLO推理
    # conf=0.25 是一个默认的置信度阈值，你可以根据需要调整
    # iou=0.7 也是一个默认的IoU阈值，用于非极大值抑制（NMS）
    results = model(frame, conf=0.25, iou=0.7, verbose=False) # verbose=False 可以减少控制台输出

    # 处理检测结果并打印信息
    process_detections(results, CLASS_NAMES)

    # 可选：在窗口中显示带有检测框的帧（如果需要可视化）
    annotated_frame = results[0].plot() # 这会返回一个带有检测框和标签的帧
    cv2.imshow("YOLOv11 Detection", annotated_frame)

    # 按 'q' 键退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# --- 5. 清理资源 ---
cap.release()
cv2.destroyAllWindows()
print("检测结束。")