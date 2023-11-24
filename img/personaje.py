import pygame

class Personaje(pygame.sprite.Sprite):
    def __init__(self,x,y,scale):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load('img/jugador/parado/0.png')
        self.img = pygame.transform.scale_by(self.img, scale)
        self.rect = self.img.get_rect()
        self.rect.center = (x, y)