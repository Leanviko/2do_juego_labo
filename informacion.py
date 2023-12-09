import pygame
from assets import *


def dibujar_texto(pantalla, texto, fuente, texto_color, x, y):
    img = fuente.render(texto, True, texto_color)
    pantalla.blit(img, (x, y))
