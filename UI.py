import cv2
from datetime import datetime
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap, QIcon
from PyQt6.QtWidgets import *
import datetime
import os
from camera import Camera
import pygame
from Dibujar import DibujadorImagen
from styles import Styles

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cámara en PyQt6")
        pygame.mixer.init()

        self.widget = QWidget()
        self.setCentralWidget(self.widget)

        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)

        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        self.camera_tab = QWidget()
        self.Fotos_tab = QWidget()
        self.Videos_tab = QWidget()

        # Tabs 
        self.tab_widget.addTab(self.camera_tab, "Cámara")
        self.tab_widget.addTab(self.Fotos_tab, "Fotos")
        self.tab_widget.addTab(self.Videos_tab, "Videos")

        self.camera_tab_layout = QVBoxLayout()
        self.camera_tab.setLayout(self.camera_tab_layout)

        camera_layout = QHBoxLayout()
        button_layout = QHBoxLayout()

        # original image
        self.original_label = QLabel()
        self.original_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        camera_layout.addWidget(self.original_label)

        # Filters
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Original", "Complement", "Binary"])
        button_layout.addWidget(self.filter_combo)

        #Filter Image
        self.filter_label = QLabel()
        self.filter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        camera_layout.addWidget(self.filter_label)

        self.camera = Camera(self.original_label, self.filter_label,self.filter_combo)
        self.camera_tab_layout.addLayout(camera_layout)

        

        # Cameras combo 
        self.camera_combo = QComboBox()
        self.camera_combo.setWindowTitle("Cámaras")
        self.camera_combo.addItems(["Cámara 1","Cámara 2", "Cámara 3" ])
        self.camera_combo.currentIndexChanged.connect(self.change_camera)
        button_layout.addWidget(self.camera_combo)

        # Timer Combo
        self.combo_box_timer = QComboBox()
        self.combo_box_timer.addItems(["0 sec", "3 sec", "5 sec", "10 sec"])
        button_layout.addWidget(self.combo_box_timer)

        

        self.camera_tab_layout.addLayout(button_layout)

        # Photo button 
        photo_icon_path = "icons/radio.png"
        self.photo_button = QPushButton(icon=QIcon(photo_icon_path))
        self.photo_button.clicked.connect(self.take_photo)
        button_layout.addWidget(self.photo_button)

        # Record Button
        record_icon_path = "icons/play-button.png"
        self.record_button = QPushButton(icon=QIcon(record_icon_path))
        self.record_button.clicked.connect(self.record_video)
        button_layout.addWidget(self.record_button)

        #Close Button
        close_icon_path = "icons/close.png"
        close_button = QPushButton(icon=QIcon(close_icon_path))
        close_button.setObjectName("closeButton")
        close_button.clicked.connect(self.confirmQuit)
        button_layout.addWidget(close_button)

        self.photos_tab_layout = QHBoxLayout()
        self.Fotos_tab.setLayout(self.photos_tab_layout)

        self.photos_list = QListWidget()
        self.photos_list.itemDoubleClicked.connect(self.show_selected_photo)
        self.photos_list.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)  # Ajuste de tamaño
        self.photos_tab_layout.addWidget(self.photos_list)
        
        #Update Button 
        update_icon_path = "icons/update.png"
        self.actualizar_button = QPushButton(icon=QIcon(update_icon_path))
        self.actualizar_button.clicked.connect(self.actualizar_widget_fotos)
        self.photos_tab_layout.addWidget(self.actualizar_button)

        self.photo_display_layout = QVBoxLayout()
        self.photos_tab_layout.addLayout(self.photo_display_layout)

        self.selected_photo_label = QLabel()
        self.selected_photo_label.setMinimumSize(400, 400)  
        self.selected_photo_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)  
        self.photo_display_layout.addWidget(self.selected_photo_label)

        button_layout = QHBoxLayout()

        #Dibujar Buttom 
        draw_icon_path = "icons/edit-button.png"
        self.edit_button = QPushButton(icon=QIcon(draw_icon_path))
        self.edit_button.clicked.connect(self.Dibujar_foto)
        self.edit_button.setEnabled(False)
        button_layout.addWidget(self.edit_button)

        #Delete Button 
        delete_icon_path = "icons/trash.png"
        self.delete_button = QPushButton(icon=QIcon(delete_icon_path))
        self.delete_button.clicked.connect(self.delete_photo)
        self.delete_button.setEnabled(False)
        button_layout.addWidget(self.delete_button)

        self.photo_display_layout.addLayout(button_layout)


        self.output_dir = os.path.join(os.getenv('HOME'), "Downloads")
        self.photo_files = []
        self.load_photos()

        Styles.apply_styles(self)
        pygame.mixer.init()
         # Asegúrate de que el nombre del archivo coincida con el tuyo

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
            self.photo_button.setEnabled(False)
            self.timer = QTimer()
            self.camera.start_photo_timer(timer_index * 3)
            self.timer.singleShot(timer_index * 3000, self.enable_photo_button) 

    def enable_photo_button(self):
        
        self.photo_button.setEnabled(True)

    def actualizar_widget_fotos(self):

        self.photos_list.clear()
    
        self.load_photos()
        self.show_photos()

    # Deberia ir en el Modulo camera.py
    def change_camera(self, index):
        self.timer.stop() # el timer a usar se declara en dicho modulo 
        self.cap.release()
        if index == 0:
            self.camera_index = 0
        elif index == 1:
            self.camera_index = 1
        else:
            self.camera_index = 2
        self.cap = cv2.VideoCapture(self.camera_index)
        self.timer.start()

    
    def record_video(self):
        # Código para grabar un video
        pass

    def show_photos(self):
        self.photos_list
        for file in self.photo_files:
            item = QListWidgetItem(file)
            self.photos_list.addItem(item)

    def show_selected_photo(self, item):
        file_name = item.text()
        file_path = os.path.join(self.output_dir, file_name)
        try:
            image = cv2.imread(file_path)
            if image is not None:
                qimage = QImage(image.data, image.shape[1], image.shape[0], QImage.Format.Format_BGR888)
                pixmap = QPixmap.fromImage(qimage)
                self.selected_photo_label.setPixmap(pixmap.scaledToWidth(800))
                self.edit_button.setEnabled(True)
                self.delete_button.setEnabled(True)
            else:
                QMessageBox.warning(self, "Error", f"No se pudo abrir la imagen: {file_path}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al abrir la imagen: {e}")


    def Dibujar_foto(self):
        selected_item = self.photos_list.currentItem()
        if selected_item is None:
            QMessageBox.warning(self, "Error", "Seleccione una foto para dibujar.")
            return

        file_name = selected_item.text()
        file_path = os.path.join(self.output_dir, file_name)

        dibujador = DibujadorImagen(file_path)

        button_layout = QHBoxLayout()

        color_combo = QComboBox()
        color_combo.addItems(["Negro", "Verde", "Azul", "Rojo", "Amarillo"]) 
        color_combo.currentIndexChanged.connect(dibujador.cambiar_color_aleatorio)

        guardar_elementos_button = QPushButton("Guardar elementos gráficos")
        guardar_elementos_button.clicked.connect(lambda: self.guardar_y_cargar_imagen(dibujador, file_name, 0))

        guardar_imagen_button = QPushButton("Guardar imagen editada")
        guardar_imagen_button.clicked.connect(lambda: self.guardar_y_cargar_imagen(dibujador, file_name, 1))

        button_layout.addWidget(color_combo)
        button_layout.addWidget(guardar_elementos_button)
        button_layout.addWidget(guardar_imagen_button)
        
        self.photo_display_layout.addLayout(button_layout)

        while True:
            cv2.imshow('imagen', dibujador.dibujar_sobre_imagen(dibujador.imagen, dibujador.color))
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or cv2.getWindowProperty('imagen', cv2.WND_PROP_VISIBLE) < 1:  
                break
            elif key == ord('e'):  
                break
                
        cv2.destroyAllWindows()

    def guardar_y_cargar_imagen(self, dibujador, file_name, index):
        try:
            if index == 0:
                # Construye la ruta del archivo de manera segura y compatible
                elements_path = os.path.join(self.output_dir, file_name + '_elementos_pintados.txt')
                dibujador.guardar_elementos_pintados(elements_path)
            elif index == 1:
                # Construye la ruta del archivo de manera segura y compatible
                edited_image_path = os.path.join(self.output_dir, file_name + '_imagen_editada.jpg')
                dibujador.guardar_imagen(edited_image_path)
                self.photo_files.append(edited_image_path)  # Asegúrate de que self.photo_files esté definido
        except Exception as e:
            print(f"Error al guardar o cargar la imagen: {e}")

    def delete_photo(self):
        selected_item = self.photos_list.currentItem()
        if selected_item is None:
            QMessageBox.warning(self, "Error", "Seleccione una foto para eliminar.")
            return
        reply = QMessageBox.question(
            self, "Confirmar", "¿Estás seguro de que deseas eliminar esta foto?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            file_name = selected_item.text()
            file_path = os.path.join(self.output_dir, file_name)
            os.remove(file_path)
            self.photos_list.takeItem(self.photos_list.row(selected_item))
            self.selected_photo_label.clear()
            self.edit_button.setEnabled(False)
            self.delete_button.setEnabled(False)

    def open_photo(self, item):
        try:
            file_name = item.text()
            file_path = os.path.join(self.output_dir, file_name)

            # Verifica si el archivo existe antes de intentar leerlo
            if not os.path.isfile(file_path):
                raise FileNotFoundError(f"No se encontró el archivo: {file_path}")

            image = cv2.imread(file_path)
            if image is None:
                raise IOError(f"No se pudo leer el archivo: {file_path}")

            cv2.imshow("Photo", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        except Exception as e:
            print(f"Error al abrir la foto: {e}")

    def open_video(self, item):
        file_name = item.text()
        file_path = os.path.join(self.output_dir, file_name)
        cap = cv2.VideoCapture(file_path)
        if not cap.isOpened():
            print("Error: No se pudo abrir el archivo de video.")
            return
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow("Video", frame)
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    def save_photos(self):
        # Construye la ruta del archivo de manera segura y compatible
        photos_list_path = os.path.join(self.output_dir, "photos_list.txt")

        with open(photos_list_path, "w") as file:
            for photo_file in self.photo_files:
                file.write(photo_file + "\n")

    def load_photos(self):
        # Construye la ruta del archivo de manera segura y compatible
        photos_list_path = os.path.join(self.output_dir, "photos_list.txt")

        if os.path.exists(photos_list_path):
            with open(photos_list_path, "r") as file:
                for line in file:
                    self.photo_files.append(line.strip())

   