import pygame 

ANCHO_PANTALLA = 800
ALTO_PANTALLA = int(ANCHO_PANTALLA *0.8)

pantalla = pygame.display.set_mode((ANCHO_PANTALLA,ALTO_PANTALLA))
pygame.display.set_caption('2do juego')

x = 200
y = 200
img = pygame.image.load('img/jugador/parado/0.png')
rect = img.get_rect()
rect.center = (x, y)


corriendo = True
while corriendo:

    
    pantalla.blit(img, rect)


    for evento in pygame.event.get():
        
        if evento.type == pygame.QUIT:
            corriendo = False
    
    pygame.display.update()