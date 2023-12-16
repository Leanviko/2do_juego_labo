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


def funcion_menu_pausa(pantalla, img, x, y, pos_x,pos_y, estados):

    img = img.convert_alpha()
    img_rect = img.get_rect()
    img_rect.center = (x, y)
    

    #cerrar
    if (pos_x > 473 and pos_x<526) and (pos_y > 157 and pos_y<212):
        print("hola2")    
        if pygame.mouse.get_pressed()[0]:
            estados["pausa_juego"] = False

    #cerrar juego
    if (pos_x > 283 and pos_x<358) and (pos_y > 239 and pos_y<294):
        print("cerrar juego")
        if pygame.mouse.get_pressed()[0]:
            #estados["pausa_juego"] = False
            estados["menu_pausa_principal"] = False
            estados["iniciar_juego"] = False
    
    #configuracion
    if (pos_x > 370 and pos_x< 422) and (pos_y > 239 and pos_y<294):
        #print("configuracion")
        if pygame.mouse.get_pressed()[0]:
            estados["configuracion_pantalla"] = True
            estados["menu_pausa_principal"] = False
    
    #nivel
    if (pos_x > 448 and pos_x< 500) and (pos_y > 239 and pos_y<294):
        print("nivel")
        if pygame.mouse.get_pressed()[0]:
            estados["seleccion_nivel_pantalla"] = True
            estados["menu_pausa_principal"] = False 

    #ranking
    if (pos_x > 370 and pos_x< 422) and (pos_y > 327 and pos_y<378):
        print("ranking")
        if pygame.mouse.get_pressed()[0]:
            estados["ranking_pantalla"] = True
            

    pantalla.blit(img, img_rect)


    
def menu_configuracion(pantalla, img, x, y, pos_x,pos_y, estados,grados_img_lista,volumenes,sonidos):
    img = img.convert_alpha()
    img_rect = img.get_rect()
    img_rect.center = (x, y)

    #cerrar
    if (pos_x > 473 and pos_x<526) and (pos_y > 157 and pos_y<212):
        if pygame.mouse.get_pressed()[0]:
            estados["pausa_juego"] = False
            estados["configuracion_pantalla"] = False
    
    #volumen musica
    if (pos_x > 470 and pos_x< 505) and (pos_y > 286 and pos_y<327):
        if pygame.mouse.get_pressed()[0] and volumenes["presionado"] == False:
            volumenes["volumen_musica"]  += 1
            if volumenes["volumen_musica"]  > 7:
                volumenes["volumen_musica"]  = 7
            volumenes["presionado"] = True
            sonidos["disparo"].play()
    
    if (pos_x > 293 and pos_x< 331) and (pos_y > 286 and pos_y<327):
        if pygame.mouse.get_pressed()[0] and volumenes["presionado"] == False:
            volumenes["volumen_musica"]  -= 1
            if volumenes["volumen_musica"]  < 0:
                volumenes["volumen_musica"]  = 0
            volumenes["presionado"] = True
            sonidos["disparo"].play()
        
    if not(pygame.mouse.get_pressed()[0]):
        volumenes["presionado"] = False

    volumen = volumenes["volumen_musica"]

    if volumen == 0:
        grados = grados_img_lista[0]
    elif volumen == 1:
        grados = grados_img_lista[1]
    elif volumen == 2:
        grados = grados_img_lista[2]
    elif volumen == 3:
        grados = grados_img_lista[3]
    elif volumen == 4:
        grados = grados_img_lista[4]
    elif volumen == 5:
        grados = grados_img_lista[5]
    elif volumen == 6:
        grados = grados_img_lista[6]
    elif volumen == 7:
        grados = grados_img_lista[7]
    

    grados_img = grados.convert_alpha()
    img_grados_rect = grados_img.get_rect()
    img_grados_rect.topleft = (336,293)

    #volumen sonidos
    if (pos_x > 470 and pos_x< 505) and (pos_y > 357 and pos_y< 400):
        if pygame.mouse.get_pressed()[0] and volumenes["presionado"] == False:
            volumenes["volumen_sonido"]  += 1
            if volumenes["volumen_sonido"]  > 7:
                volumenes["volumen_sonido"]  = 7
            volumenes["presionado"] = True
            #sonidos["disparo"].play()

    if (pos_x > 293 and pos_x< 331) and (pos_y > 357 and pos_y< 400):
        if pygame.mouse.get_pressed()[0] and volumenes["presionado"] == False:
            volumenes["volumen_sonido"]  -= 1
            if volumenes["volumen_sonido"]  < 0:
                volumenes["volumen_sonido"]  = 0
            volumenes["presionado"] = True
            #sonidos["disparo"].play()
        
    if not(pygame.mouse.get_pressed()[0]):
        volumenes["presionado"] = False

    volumen_sonido = volumenes["volumen_sonido"]

    if volumen_sonido == 0:
        grados_sonido = grados_img_lista[0]
    elif volumen_sonido == 1:
        grados_sonido = grados_img_lista[1]
    elif volumen_sonido == 2:
        grados_sonido = grados_img_lista[2]
    elif volumen_sonido == 3:
        grados_sonido = grados_img_lista[3]
    elif volumen_sonido == 4:
        grados_sonido = grados_img_lista[4]
    elif volumen_sonido == 5:
        grados_sonido = grados_img_lista[5]
    elif volumen_sonido == 6:
        grados_sonido = grados_img_lista[6]
    elif volumen_sonido == 7:
        grados_sonido = grados_img_lista[7]
    

    grados_sonido_img = grados_sonido.convert_alpha()
    img_grados_sonido_rect = grados_sonido_img.get_rect()
    img_grados_sonido_rect.topleft = (336,364)

    pantalla.blit(img, img_rect)
    pantalla.blit(grados_img, img_grados_rect)
    pantalla.blit(grados_sonido_img, img_grados_sonido_rect)



def menu_niveles(pantalla, img, x, y, pos_x,pos_y, estados, estrellas_img_lista,estrellas,nivel):
    
    img = img.convert_alpha()
    ancho = img.get_width()
    alto = img.get_height()
    img = pygame.transform.scale(img,(ancho*1.5,alto))
    img_rect = img.get_rect()
    img_rect.center = (x, y)

    img_menu_est =[]
    for i in range(4):
        num_estrellas = estrellas[f"nivel_{i+1}"]
        img_estre = estrellas_img_lista[num_estrellas]

        img_menu_est.append(img_estre)

    estrellas_n1_img = img_menu_est[0].convert_alpha()
    estrellas_n1_rect = estrellas_n1_img.get_rect()
    estrellas_n1_rect.topleft = (299,248)

    estrellas_n2_img = img_menu_est[1].convert_alpha()
    estrellas_n2_rect = estrellas_n2_img.get_rect()
    estrellas_n2_rect.topleft = (422,248)

    estrellas_n3_img = img_menu_est[2].convert_alpha()
    estrellas_n3_rect = estrellas_n3_img.get_rect()
    estrellas_n3_rect.topleft = (299,330)

    estrellas_n4_img = img_menu_est[3].convert_alpha()
    estrellas_n4_rect = estrellas_n4_img.get_rect()
    estrellas_n4_rect.topleft = (422,330)
        

    #cerrar
    if (pos_x > 479 and pos_x<533) and (pos_y > 153 and pos_y<190):

        if pygame.mouse.get_pressed()[0]:
            estados["seleccion_nivel_pantalla"] = False
            estados["pausa_juego"] = False
            #estados["configuracion_pantalla"] = False

    #nivel 1
    if (pos_x > 297 and pos_x< 379) and (pos_y > 211 and pos_y<270):
        print("nivel 1")
        if pygame.mouse.get_pressed()[0] and estrellas["nivel_1"]>0 and estados["presionado"] == False:
            nivel = 1
            estados["pausa_juego"] = False
            estados["seleccion_nivel_pantalla"] = False
            

    #nivel 2
    if (pos_x > 423 and pos_x< 504) and (pos_y > 211 and pos_y<270):
        #print("nivel 2")
        if pygame.mouse.get_pressed()[0] and estrellas["nivel_2"]>0 and estados["presionado"] == False:
            nivel = 2
            estados["pausa_juego"] = False
            estados["seleccion_nivel_pantalla"] = False


    #nivel 3
    if (pos_x > 298 and pos_x< 380) and (pos_y > 295 and pos_y<354):

        print("nivel 3")
        if pygame.mouse.get_pressed()[0] and estrellas["nivel_3"]>0 and estados["presionado"] == False:
            nivel = 3
            estados["seleccion_nivel_pantalla"] = False
            estados["pausa_juego"] = False
 
    
    #nivel 4
    if (pos_x > 420 and pos_x< 503) and (pos_y > 295 and pos_y<354):

        print("nivel 4")
        if pygame.mouse.get_pressed()[0] and estrellas["nivel_4"]>0 and estados["presionado"] == False:

            nivel = 4
            estados["seleccion_nivel_pantalla"] = False
            estados["pausa_juego"] = False
            

    if not(pygame.mouse.get_pressed()[0]):
        estados["presionado"] = False

    pantalla.blit(img, img_rect)

    pantalla.blit(estrellas_n1_img, estrellas_n1_rect)
    pantalla.blit(estrellas_n2_img, estrellas_n2_rect)
    pantalla.blit(estrellas_n3_img, estrellas_n3_rect)
    pantalla.blit(estrellas_n4_img, estrellas_n4_rect)

    return nivel
    
#def menu_niveles():
    