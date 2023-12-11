import pygame
import json
from assets import *

with open("variables.json","r") as var:
    variables = json.load(var)



class CajaItem(pygame.sprite.Sprite):
    def __init__(self, item_tipo, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_tipo = item_tipo
        self.image = item_cajas[item_tipo].convert_alpha()
        self.image = pygame.transform.scale_by(self.image,0.8)
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + BLOQUE_TAMANIO//2, y + (BLOQUE_TAMANIO - self.image.get_height()))
    
    def update(self,jugador):
        if pygame.sprite.collide_rect(self, jugador):
            if self.item_tipo == 'Salud':
                jugador.salud += 25
                if jugador.salud > jugador.salud_max:
                    jugador.salud = jugador.salud_max
                print(f'salud: {jugador.salud}')
            elif self.item_tipo == 'Municion':
                jugador.municion += 25
                print(f'municion: {jugador.municion}')
            elif self.item_tipo == 'Granada':
                jugador.granadas += 3
                print(f'granadas: {jugador.granadas}')
            self.kill()