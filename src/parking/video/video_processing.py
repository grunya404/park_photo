import math
import os

import cv2

from config import settings


class VideoProcessing:

    def __init__(self, stream_url, camera_id):
        """
        инициализация класс получения изображения с камер
        :param stream_url:  rtsp://user:12312345678@0.0.0.0:554
        :param picture_path:
        :return: void
        """

        self.frame_rate = None
        self.capture = None
        self.picture_path = settings.SCREENSHOT_ROOT
        self.camera_id = camera_id
        self.stream_url = stream_url

    async def get_screenshot(self) -> str:
        self.capture = cv2.VideoCapture(self.stream_url)
        self.frame_rate = self.capture.get(5)  # frame rate
        filename = ""
        try:
            while self.capture.isOpened():
                frame_id = self.capture.get(1)
                ret, frame = self.capture.read()
                if (ret != True):
                    break
                if (frame_id % math.floor(self.frame_rate) == 0):
                    filename = self.picture_path + "/image_" + str(self.camera_id) + ".jpg"
                    if os.path.exists(filename):
                        os.remove(filename)
                    cv2.imwrite(filename, frame)
                self.capture.release()
            cv2.destroyAllWindows()

        except Exception:
            Exception("Filed get screenshot")

        path, file = os.path.split(filename)
        url = f"{settings.SCREENSHOT_URL}{file}"
        return url
