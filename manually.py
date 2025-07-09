import cv2
import sys
import time 
from threading import Thread
import os

# from your_design_ui import Ui_MainWindow
# --- 配置 ---
# RTSP_URL = "192.168.1.102" 
save_dir_bad = "saved_bad_crabs" 
save_dir_good = "saved_good_crabs"  

class Video:
    def __init__(self, rtsp_url):
        self.rtsp_url = rtsp_url
        # self.cap = cv2.VideoCapture(f"rtsp://{self.rtsp_url}")
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Could not open video stream.")
            sys.exit(1)

    def read_img(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Error: Could not read frame.")
            return None
        
        self.current_frame = frame

        return frame
    
    def show(self):
        while True:
            frame = self.read_img()

            if frame is None:
                break
            cv2.imshow("Video Stream", frame)
            key = cv2.waitKey(1) & 0xFF
            if  key == ord('q'):
                break
            elif key  == ord('g'):
                self.save_Good()
            elif key  == ord('b'):
                self.save_Bad()

        cv2.destroyAllWindows()
        self.cap.release()

    def save_Good(self):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{save_dir_good}/good_crab_{timestamp}.jpg"

        if self.current_frame is not None:
            cv2.imwrite(filename, self.current_frame)
            print(f"Saved good crab image to {filename}")
        else:
            print("Error: Could not read frame for saving.")
    
    def save_Bad(self):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{save_dir_bad}/bad_crab_{timestamp}.jpg"
        
        if self.current_frame is not None:
            cv2.imwrite(filename, self.current_frame)
            print(f"Saved bad crab image to {filename}")
        else:
            print("Error: Could not read frame for saving.")


if __name__ == "__main__":

    os.makedirs(save_dir_bad, exist_ok=True)
    os.makedirs(save_dir_good, exist_ok=True)

    # vs= Video(RTSP_URL)
    vs= Video(0)


    thread_show_img = Thread(target=vs.show) #这里写vs.show()会立即执行，而不是传递函数引用,所以要用 `target=vs.show` 而不是 `target=vs.show()`
    # 这里的 args=(1, 1) 是多余的，因为 show 方法不需要参数
    thread_show_img.start()
    thread_show_img.join()

