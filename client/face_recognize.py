import sys

import cv2
import face_recognition
import numpy as np
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QApplication


class FaceThread(QThread):
    """人脸识别子线程"""
    isOwner = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.timeout = 100  # 设定超时时间

    def run(self):
        video_capture = cv2.VideoCapture(0)

        # Load sample pictures and learn how to recognize them
        zyh_image = face_recognition.load_image_file("../images/zyh.jpg")
        zyh_face_encoding = face_recognition.face_encodings(zyh_image)[0]

        dy_image = face_recognition.load_image_file("../images/dy.jpg")
        dy_face_encoding = face_recognition.face_encodings(dy_image)[0]

        # Arrays of known face encodings and their names
        known_face_encodings = [zyh_face_encoding, dy_face_encoding]
        known_face_names = ["Yuhao Zhao", "Yun Day"]

        process_this_frame = True

        while self.timeout and video_capture.isOpened():
            self.timeout -= 1
            ret, frame = video_capture.read()
            if not ret:
                break

            if process_this_frame:
                # Face recognition logic
                recognition_result = self.process_frame(frame, known_face_encodings, known_face_names)
                if recognition_result == 1:
                    self.isOwner.emit(1)
                    break

            process_this_frame = not process_this_frame

        video_capture.release()
        cv2.destroyAllWindows()
        self.isOwner.emit(0)

    def process_frame(self, frame, known_face_encodings, known_face_names):
        """ Process a single frame for face recognition """
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, 0.45)
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                return 1  # Known face detected

        return 0  # No known faces detected


if __name__ == '__main__':
    app = QApplication(sys.argv)  # 创建 QApplication 实例
    face_thread = FaceThread()
    face_thread.isOwner.connect(lambda owner: print(f"Owner detected: {owner}"))
    face_thread.start()
    sys.exit(app.exec())  # 启动事件循环
