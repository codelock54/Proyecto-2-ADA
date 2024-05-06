import cv2
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import *
import os 
import datetime
import pygame
class Camera:
    """Open and Manage the Camera"""
    def __init__(self, original_label, filter_label, filter_combo):
        self.original_label = original_label
        self.filter_label = filter_label
        self.filter_combo = filter_combo
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(10)

        self.photo_timer = QTimer()
        self.photo_timer.timeout.connect(self.take_photo)

    def update_frame(self):
        """Update frames y set up filters"""
        ret, frame = self.cap.read()
        if ret:
            # show original image
            self.display_image(frame, self.original_label)

            # Set filter selected 
            filter_index = self.filter_combo.currentIndex()
            if filter_index == 0:  # Original
                filtered_frame = frame.copy()
            elif filter_index == 1:  # Complement
                filtered_frame = cv2.bitwise_not(frame)
            elif filter_index == 2:  # Binary
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                _, binary_frame = cv2.threshold(gray_frame, 128, 255, cv2.THRESH_BINARY)
                filtered_frame = cv2.cvtColor(binary_frame, cv2.COLOR_GRAY2BGR)

            # show filter image
            self.display_image(filtered_frame, self.filter_label)

    def display_image(self, image, label):
        """Show Image in the display"""
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        label.setPixmap(pixmap)
        label.setScaledContents(True)


    def take_photo(self):
        """Take and Store photos"""
        try:
           

                # Determinar la ruta del escritorio
                desktop_path = os.path.join(os.path.expanduser("."),"./")
                # desktop_path = os.getcwdb()

                # # Crear la carpeta "Galery" si no existe
                galery_path = os.path.join(desktop_path, "Galery")
                # galery_path = "./Galery"

                if not os.path.exists(galery_path):
                    os.mkdir(galery_path)

                # Generar el nombre del archivo con la fecha y hora actual
                now = datetime.datetime.now()  
                date_time_str = now.strftime("%Y-%m-%d_%H-%M-%S")
                file_name = f"photo_{date_time_str}.jpg"

                # Guardar la imagen en la carpeta "Galery"
                ret, frame = self.cap.read()
                if ret:
                    cv2.imwrite(os.path.join(galery_path, file_name), frame)
                    print("Photo saved")
                    pygame.mixer.music.load("effects/camera-flash-204151.mp3")
                    pygame.mixer.music.play()
                    self.photo_timer.stop()

        except Exception as e:
            print(f"Error to take the photo: {e}")
    

    def start_photo_timer(self, seconds):
        """Set Timer to take photos"""
        self.photo_timer.start(seconds * 1000)

  
   