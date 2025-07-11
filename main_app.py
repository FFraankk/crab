import cv2
import sys
import time
from threading import Thread
import os

from PyQt5 import QtWidgets, QtGui, QtCore
from manually_ui import Ui_MainWindow  # 假设你的UI文件生成为 your_design_ui.py

# --- 配置 ---
# RTSP_URL = "192.168.1.102" # 如果使用RTSP流，请取消注释并设置URL
save_dir_bad = "saved_bad_crabs"
save_dir_good = "saved_good_crabs"


class VideoProcessor(QtCore.QObject):
    # 声明一个信号，用于在有新帧可用时发出
    new_frame_signal = QtCore.pyqtSignal(QtGui.QImage)
    # 新增一个信号，用于通知摄像头打开状态
    camera_status_signal = QtCore.pyqtSignal(bool)

    def __init__(self, rtsp_url):
        super().__init__()
        self.rtsp_url = rtsp_url
        self.cap = cv2.VideoCapture(self.rtsp_url)
        self.running = False  # 初始设置为False，只有成功打开摄像头才设置为True
        self.current_frame = None

        if not self.cap.isOpened():
            print(f"VideoProcessor: 错误: 无法打开视频流 {rtsp_url}。")
            self.camera_status_signal.emit(False)  # 发出摄像头未打开信号
        else:
            print(f"VideoProcessor: 成功打开视频流 {rtsp_url}。")
            self.running = True  # 只有成功打开摄像头才允许运行
            self.camera_status_signal.emit(True)  # 发出摄像头已打开信号

    def process_frames(self):
        """在单独的线程中处理视频帧并发出信号"""
        print("VideoProcessor: process_frames 线程开始运行。")
        if not self.cap.isOpened():
            print("VideoProcessor: 视频流未打开，无法处理帧。线程退出。")
            self.running = False  # 确保running为False
            return

        # 确保在线程启动后立即尝试读取第一帧，以避免current_frame为None
        # 即使这里失败，循环也会继续尝试
        ret, frame = self.cap.read()
        if ret and frame is not None:
            self.current_frame = frame
            print("VideoProcessor: 成功读取第一帧。")
        else:
            print("VideoProcessor: 未能读取到第一帧。")


        while self.running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                print("VideoProcessor: 错误: 无法读取帧。视频流可能已中断。")
                self.running = False  # 如果读取帧失败，则停止运行
                break
            
            # 检查帧是否有效，防止读取到None帧
            if frame is None:
                # print("VideoProcessor: 读取到空帧，跳过此帧。") # 频繁打印会刷屏，暂时注释
                continue # 跳过当前循环，继续尝试读取下一帧
                
            self.current_frame = frame

            # 将OpenCV的BGR图像转换为Qt的RGB QImage
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)

            self.new_frame_signal.emit(qt_image)

            # 添加一个小的延迟，防止循环占用100%的CPU
            time.sleep(0.01)

        self.cap.release()
        print("VideoProcessor: 视频处理线程已停止。")

    def stop(self):
        """停止视频处理循环"""
        print("VideoProcessor: 收到停止请求。")
        self.running = False

    def save_Good(self):
        """保存当前帧为好螃蟹图片"""
        print(f"VideoProcessor: save_Good 被调用。current_frame is None: {self.current_frame is None}")
        if self.current_frame is not None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"{save_dir_good}/good_crab_{timestamp}.jpg"
            try:
                cv2.imwrite(filename, self.current_frame)
                print(f"已将好螃蟹图片保存到: {filename}")
            except Exception as e:
                print(f"保存好螃蟹图片时发生错误: {e}")
        else:
            print("错误: 没有可用于保存的帧。")

    def save_Bad(self):
        """保存当前帧为坏螃蟹图片"""
        print(f"VideoProcessor: save_Bad 被调用。current_frame is None: {self.current_frame is None}")
        if self.current_frame is not None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"{save_dir_bad}/bad_crab_{timestamp}.jpg"
            try:
                cv2.imwrite(filename, self.current_frame)
                print(f"已将坏螃蟹图片保存到: {e}")
            except Exception as e:
                print(f"保存坏螃蟹图片时发生错误: {e}")
        else:
            print("错误: 没有可用于保存的帧。")


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 创建保存目录（如果不存在）
        os.makedirs(save_dir_bad, exist_ok=True)
        os.makedirs(save_dir_good, exist_ok=True)

        # 初始化 VideoProcessor
        self.video_processor = VideoProcessor(0)  # 用于摄像头 (索引 0)

        # 连接摄像头状态信号
        self.video_processor.camera_status_signal.connect(self.handle_camera_status)

        # 为视频处理创建一个QThread，避免UI冻结
        self.video_thread = QtCore.QThread()
        self.video_processor.moveToThread(self.video_thread)

        # 连接信号和槽
        print("MainWindow: 尝试连接 new_frame_signal 到 update_video_feed。")
        self.video_processor.new_frame_signal.connect(self.update_video_feed)
        print("MainWindow: 尝试连接 video_thread.started 到 video_processor.process_frames。")
        self.video_thread.started.connect(self.video_processor.process_frames)

        # 连接按钮点击事件到相应的方法
        # 根据你提供的your_design_ui.py，按钮的objectName是 'quit', 'good', 'bad'
        print("MainWindow: 尝试连接 'quit' 按钮。")
        self.ui.quit.clicked.connect(self.quit_application)
        print("MainWindow: 尝试连接 'good' 按钮。")
        self.ui.good.clicked.connect(self._on_good_button_clicked) # 连接到包装方法
        print("MainWindow: 尝试连接 'bad' 按钮。")
        self.ui.bad.clicked.connect(self._on_bad_button_clicked)   # 连接到包装方法

        # 启动视频线程，只有当VideoProcessor报告摄像头成功打开时才启动
        if self.video_processor.running:
            self.video_thread.start()
            print("MainWindow: 摄像头已成功打开，视频处理线程已启动。")
        else:
            # 如果视频流未打开，则直接让线程退出或不启动
            self.video_thread.quit()
            print("MainWindow: 摄像头未成功打开，视频处理线程未启动。")

    @QtCore.pyqtSlot(bool)
    def handle_camera_status(self, is_opened):
        """处理摄像头打开状态的槽函数"""
        print(f"MainWindow: handle_camera_status 被调用，is_opened: {is_opened}")
        if not is_opened:
            QtWidgets.QMessageBox.critical(self, "错误", "无法打开视频流。请检查摄像头是否连接或RTSP地址是否正确。")
            # 禁用相关按钮，因为没有视频流可以操作
            self.ui.good.setEnabled(False)
            self.ui.bad.setEnabled(False)
            self.ui.quit.setEnabled(False) # 摄像头未打开时，退出按钮也应禁用
            print("MainWindow: 按钮已禁用。")
        else:
            # 确保在摄像头成功打开时启用按钮
            self.ui.good.setEnabled(True)
            self.ui.bad.setEnabled(True)
            self.ui.quit.setEnabled(True)
            print("MainWindow: 按钮已启用。")

    @QtCore.pyqtSlot(QtGui.QImage)
    def update_video_feed(self, image):
        """
        更新QLabel中的视频画面。
        将QImage缩放以适应QLabel的大小并保持长宽比。
        """
        # print("MainWindow: update_video_feed 被调用。") # 频繁打印会刷屏，暂时注释
        pixmap = QtGui.QPixmap.fromImage(image)
        # 获取QLabel的当前大小
        label_size = self.ui.video_feed_label.size()
        # 缩放图像以适应QLabel，保持长宽比，并进行平滑转换
        scaled_pixmap = pixmap.scaled(
            label_size,
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation
        )
        self.ui.video_feed_label.setPixmap(scaled_pixmap)

    def quit_application(self):
        """优雅地退出应用程序"""
        print("MainWindow: quit_application 被调用。")
        if self.video_processor:
            self.video_processor.stop()  # 停止视频处理循环
        if self.video_thread.isRunning():
            self.video_thread.quit()     # 请求线程退出
            self.video_thread.wait()     # 等待线程结束

        QtWidgets.QApplication.quit()  # 关闭PyQt应用程序

    # 新增包装方法，用于调试按钮点击
    def _on_good_button_clicked(self):
        print("MainWindow: 'good' 按钮被点击。")
        self.video_processor.save_Good()

    def _on_bad_button_clicked(self):
        print("MainWindow: 'bad' 按钮被点击。")
        self.video_processor.save_Bad()

    def closeEvent(self, event):
        """
        重写closeEvent，确保窗口关闭时正确清理资源。
        """
        print("MainWindow: closeEvent 被调用。")
        self.quit_application()
        event.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())