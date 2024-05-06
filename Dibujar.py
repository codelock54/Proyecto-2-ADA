import cv2
import numpy as np
import random
class DibujadorImagen:
    def __init__(self, imagen_path):
        self.imagen = cv2.imread(imagen_path)
        self.elementos_pintados = []
        self.punto_inicial = None
        self.color = (255, 0, 0)  # Color azul por defecto

        cv2.namedWindow('imagen')
        cv2.setMouseCallback('imagen', self.dibujar)

    def dibujar(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.punto_inicial = (x, y)
        elif event == cv2.EVENT_MOUSEMOVE and self.punto_inicial is not None:
            cv2.line(self.imagen, self.punto_inicial, (x, y), self.color, 1)
            self.punto_inicial = (x, y)
            self.elementos_pintados.append(('linea', self.punto_inicial, (x, y), self.color))
        elif event == cv2.EVENT_LBUTTONUP:
            punto_final = (x, y)
            cv2.line(self.imagen, self.punto_inicial, punto_final, self.color, 1)
            self.elementos_pintados.append(('linea', self.punto_inicial, punto_final, self.color))
            self.punto_inicial = None

    def dibujar_sobre_imagen(self, imagen, color):
        imagen_dibujada = imagen.copy()
        for elemento in self.elementos_pintados:
            tipo, inicio, fin, color = elemento
            cv2.line(imagen_dibujada, inicio, fin, color, 1)
        return imagen_dibujada

    def guardar_imagen(self, filename):
        cv2.imwrite(filename, self.imagen)

    def guardar_elementos_pintados(self, filename):
        with open(filename, 'w') as f:
            for elemento in self.elementos_pintados:
                f.write(str(elemento) + '\n')
    
    def cambiar_color_aleatorio(self, index):
        if index == 0:
            self.color = (0, 0, 0)         # Negro
        elif index == 1:
            self.color = (0, 255, 0)       # Verde
        elif index == 2:
            self.color = (0, 0, 255)       # Azul
        elif index == 3:
            self.color = (255, 0, 0)       # Rojo
        elif index == 4:
            self.color = (0, 255, 255)     # Amarillo (Azul y Verde)



