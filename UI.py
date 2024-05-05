import cv2
from datetime import datetime
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import *
import datetime
import os


class MainWindow(QMainWindow):
    def __init__(self):
        """Initializer"""
        super().__init__()
        self.setWindowTitle("Cámara en PyQt6")

        self.widget = QWidget()
        self.setCentralWidget(self.widget)

        # Main Layout
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)

        Camera_Layout = QHBoxLayout()

        # Original image
        self.original_label = QLabel()
        self.original_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        Camera_Layout.addWidget(self.original_label)

        # Filter image 
        self.filter_label = QLabel()
        self.filter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        Camera_Layout.addWidget(self.filter_label)

        # Add camera Layout
        self.layout.addLayout(Camera_Layout)

        # Open webcam 
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(10)

        self.photo_timer = QTimer(self)
       
    
        Button_Layout = QHBoxLayout()

        #Timer 
        self.combo_box_timer = QComboBox()
        self.combo_box_timer.addItem("0 seg")
        self.combo_box_timer.addItem("3 seg")
        self.combo_box_timer.addItem("5 seg")
        self.combo_box_timer.addItem("10 seg")
        Button_Layout.addWidget(self.combo_box_timer)

        #Filter combo
        self.filter_combo = QComboBox()
        self.filter_combo.addItem("Original")
        self.filter_combo.addItem("Complement")
        self.filter_combo.addItem("Binary")
        Button_Layout.addWidget(self.filter_combo)

        # Photo Button 
        self.photo_button = QPushButton("Take Photo")
        self.photo_button.clicked.connect(self.take_photo)
        Button_Layout.addWidget(self.photo_button)

        # Close Button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.confirmQuit)
        Button_Layout.addWidget(close_button)

        self.layout.addLayout(Button_Layout)

    def update_frame(self):
        """ """
        ret, frame = self.cap.read()
        if ret:

            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)

            pixmap = QPixmap.fromImage(qt_image)
            self.original_label.setPixmap(pixmap)
            self.original_label.setScaledContents(True)
            self.current_frame = frame
            self.update_filter()
            

    def confirmQuit(self):
        """Confirm Quit Dialog"""
        reply = QMessageBox.question(
            self,
            "Confirm",
            "Are you sure?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.close()



    def take_photo(self):
        """Initialize timer """
        timer_index = self.combo_box_timer.currentIndex()
        if timer_index == 0: # 0 seg
            self.start_photo_timer(0)
        elif timer_index == 1: # 3 seg
            self.start_photo_timer(3)
            
        elif timer_index == 2: # 5 seg
            self.start_photo_timer(5)

        elif timer_index == 3: # 10 seg
            self.start_photo_timer(10)


    def start_photo_timer(self, seconds):
        """Run timer and call capture photo method"""
        self.photo_timer.start(seconds * 1000)
        self.photo_timer.timeout.connect(self.capture_photo)

    def capture_photo(self):
        """ Capture photos and store it """
        try:
            if hasattr(self, "current_frame"):

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
                cv2.imwrite(os.path.join(galery_path, file_name), self.current_frame)
                print("Photo saved")
                self.photo_timer.stop()

        except Exception as e:
            print(f"Error to take the photo: {e}")
            self.photo_timer.stop()



    def update_filter(self):
            """Camera filters """
            filter_index = self.filter_combo.currentIndex()
            # Original
            if filter_index == 0: 
                self.display_frame = self.current_frame
                
            # Complemento
            elif filter_index == 1: 
                self.display_frame = cv2.bitwise_not(self.current_frame)

            # Binarización
            elif filter_index == 2: 
                gray_frame = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2GRAY)
                _, self.display_frame = cv2.threshold(gray_frame, 128, 255, cv2.THRESH_BINARY)
                self.display_frame = cv2.cvtColor(self.display_frame, cv2.COLOR_GRAY2BGR)

            self.display_frame = cv2.cvtColor(self.display_frame, cv2.COLOR_BGR2RGB)
            h, w, ch = self.display_frame.shape
            bytes_per_line = ch * w
            qt_image = QImage(self.display_frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.filter_label.setPixmap(pixmap)
            self.filter_label.setScaledContents(True)

    
    def closeEvent(self, event):
        self.cap.release()
        event.accept()