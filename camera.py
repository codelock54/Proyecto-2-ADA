import cv2
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QImage, QPixmap

import cv2
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QImage, QPixmap

class Camera:
    def __init__(self, original_label, filter_label, filter_combo):
        self.original_label = original_label
        self.filter_label = filter_label
        self.filter_combo = filter_combo
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(10)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Mostrar la imagen original en self.original_label
            self.display_image(frame, self.original_label)

            # Aplicar el filtro seleccionado a la imagen
            filter_index = self.filter_combo.currentIndex()
            if filter_index == 0:  # Original
                filtered_frame = frame.copy()
            elif filter_index == 1:  # Complement
                filtered_frame = cv2.bitwise_not(frame)
            elif filter_index == 2:  # Binary
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                _, binary_frame = cv2.threshold(gray_frame, 128, 255, cv2.THRESH_BINARY)
                filtered_frame = cv2.cvtColor(binary_frame, cv2.COLOR_GRAY2BGR)

            # Mostrar la imagen filtrada en self.filter_label
            self.display_image(filtered_frame, self.filter_label)

    def display_image(self, image, label):
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        label.setPixmap(pixmap)
        label.setScaledContents(True)
