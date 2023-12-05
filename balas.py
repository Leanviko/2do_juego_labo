import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,direccion):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.bala_imagen = pygame.image.load('img/iconos/bala.img').convert_alpha()
        self.rect = self.bala_imagen.get_rect()
        self.rect.center = (x, y)
        self.direccion = direccion

        