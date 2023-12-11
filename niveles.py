import pygame
import csv
from assets import *


def cargar_niveles(FILAS,COLUMNAS,nivel):
    data_niveles = []

    for fila in range(FILAS):
        f = [-1]* COLUMNAS #llenamos por defecto con -1
        data_niveles.append(f)
    #carga del archivo de nivel
    with open(f'nivel{nivel}_data.csv', newline='') as csvfile:
        lectura = csv.reader(csvfile, delimiter=',')
        for x, fila in enumerate(lectura):
            for y, bloque in enumerate(fila):
                data_niveles[x][y] = int(bloque) #el numero del archivo se asigna a la posicion de la lista del juego

    print(data_niveles)


class Mundo():
    def __init__(self):
        self.lista_obstaculos = []

    def procesamiento_datos(self, datos):
        for y, fila in enumerate(datos):
            for x, bloque in enumerate(fila):
                if bloque >= 0:
                    img = bloques_img_lista[bloque]
                    img_rect = img.get_rect()
                    img_rect.x = x*BLOQUE_TAMANIO
                    img_rect.y = x*BLOQUE_TAMANIO
                    tile_data = (img, img_rect)
