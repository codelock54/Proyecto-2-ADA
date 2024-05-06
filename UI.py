import cv2
from datetime import datetime
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import *
import datetime
import os
from camera import Camera
from functools import partial


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

        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        self.camera_tab = QWidget()
        self.Fotos_tab = QWidget()
        self.Videos_tab = QWidget()

        self.tab_widget.addTab(self.camera_tab, "Cámara")
        self.tab_widget.addTab(self.Fotos_tab, "Fotos")
        self.tab_widget.addTab(self.Videos_tab, "Videos")

        self.camera_tab_layout = QVBoxLayout()
        self.camera_tab.setLayout(self.camera_tab_layout)
        
        
        Camera_Layout = QHBoxLayout()
        self.camera_tab_layout.addLayout(Camera_Layout)

        # Original image
        self.original_label = QLabel()
        self.original_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        Camera_Layout.addWidget(self.original_label)

        #Filter combo
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Original", "Complement","Binary"])

        # Filter image 
        self.filter_label = QLabel()
        self.filter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        Camera_Layout.addWidget(self.filter_label)
        # self.filtercamera = Camera(self.filter_label, self.filter_combo)


        self.camera = Camera(self.original_label, self.filter_label,self.filter_combo)

  

        # Add camera Layout
        self.layout.addLayout(Camera_Layout)

        # self.photo_timer = QTimer(self)
    
        Button_Layout = QHBoxLayout()

        # Cameras combo 
        self.camera_combo = QComboBox()
        self.camera_combo.setWindowTitle("Cámaras")
        # self.fill_camera_combo()
        # self.camera_combo.currentIndexChanged.connect(self.change_camera)
        Button_Layout.addWidget(self.camera_combo)


        #Timer 
        self.combo_box_timer = QComboBox()
        self.combo_box_timer.addItems(["0 seg","3 seg", "5 seg", "10 seg"])
        Button_Layout.addWidget(self.combo_box_timer)

        
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
        timer_index = self.combo_box_timer.currentIndex()
        if timer_index == 0:
            self.camera.take_photo()
        elif timer_index in (1, 2, 3):
            self.camera.start_photo_timer(timer_index * 3)


 