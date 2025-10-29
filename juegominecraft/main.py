import pygame

pygame.init()


ANCHO = 960
ALTO = 540
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Fabricación en Minecraft")


fondo = pygame.image.load("fondo.png")
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))  # El fondo ocupa toda la pantalla

tablero = pygame.image.load("Tablero.png")

tablero = pygame.transform.scale(tablero, (330, 330))  # Podés ajustar los valores


x_tablero = 330
y_tablero = 120

ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    pantalla.blit(fondo, (0, 0))               
    pantalla.blit(tablero, (x_tablero, y_tablero))  

    pygame.display.update()

pygame.quit()








