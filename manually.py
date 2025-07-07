import cv2
import sys
import time 

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

    def read(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Error: Could not read frame.")
            return None
        return frame

    def save_Good(self):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{save_dir_good}/good_crab_{timestamp}.jpg"
        ret, frame = self.cap.read()
        if ret:
            cv2.imwrite(filename, frame)
            print(f"Saved good crab image to {filename}")
        else:
            print("Error: Could not read frame for saving.")
    
    def save_Bad(self):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{save_dir_bad}/bad_crab_{timestamp}.jpg"
        ret, frame = self.cap.read()
        if ret:
            cv2.imwrite(filename, frame)
            print(f"Saved bad crab image to {filename}")
        else:
            print("Error: Could not read frame for saving.")


if __name__ == "__main__":

    vs= Video(RTSP_URL)
    try:
        while True:
            frame = vs.read()

            if frame is None:
                print("Error: No frame to display.")
                break

            cv2.imshow("video",frame)
            cv2.waitKey(1)
            
            if cv2.waitKey(1) & 0xFF == ord('g'):
                vs.save_Good()
            if cv2.waitKey(1) & 0xFF == ord('b'):
                vs.save_Bad()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break



    finally:
        # 正确的位置：在循环结束后清理资源
        cv2.destroyAllWindows()
        vs.cap.release()  # 确保释放摄像头资源

  
