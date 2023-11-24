import pygame

class Personaje(pygame.sprite.Sprite):
    def __init__(self, tipo, x, y,scale, velocidad):
        pygame.sprite.Sprite.__init__(self)
        self.tipo = tipo
        self.velocidad = velocidad
        self.direccion = 1
        self.flip = False
        self.img = pygame.image.load(f'img/{tipo}/parado/0.png')
        self.img = pygame.transform.scale_by(self.img, scale)
        self.rect = self.img.get_rect()
        self.rect.center = (x, y)

    def movimiento(self, mov_izquierda, mov_derecha):
        dx = 0
        dy = 0
        if mov_izquierda:
            dx = -self.velocidad
            self.flip = True
            self.direccion = -1
        if mov_derecha:
            dx += self.velocidad
            self.flip = False
            self.direccion = 1

        self.rect.x += dx
        self.rect.y += dy

    def dibujado(self,pantalla):
        
        pantalla.blit(pygame.transform.flip(self.img, self.flip, False), self.rect)