import pygame

class Boton():
    def __init__(self,x,y,imagen,scala):
        ancho = imagen.get_width()
        alto = imagen.get_height()
        self.image = pygame.transform.scale_by(imagen,scala)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.accionado = False

    def dibujo(self, superficie):
        accion = False

        pos =  pygame.mouse.get_pos()

        #chequear la posicion sobre el boton y el click
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.accionado == False:
                self.accionado = True
            
        if pygame.mouse.get_pressed()[0] == 0:
            self.accionado = False

        #dibujar boton
        superficie.blit(self.image, (self.rect.x,self.rect.y))

        return self.accionado