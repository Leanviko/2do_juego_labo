import pygame
import json

with open("variables.json","r") as var:
    variables = json.load(var)

ROJO = variables["ROJO"]
VERDE = variables["VERDE"]

class BarraSalud():
    def __init__(self, x, y, salud, salud_max):
        self.x = x
        self.y = y
        self.salud = salud
        self.salud_max = salud_max

    def dibujar(self, pantalla, salud):
        #actualizar con nueva salud
        self.salud = salud
        proporcion = self.salud/self.salud_max

        pygame.draw.rect(pantalla, ROJO, (self.x, self.y, 150, 20))
        pygame.draw.rect(pantalla, VERDE, (self.x, self.y, 150*proporcion, 20))
        pygame.draw.rect(pantalla, (0,0,0), (self.x, self.y, 150, 20),3)
