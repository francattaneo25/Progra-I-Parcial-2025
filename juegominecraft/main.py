import pygame
import sys
from jugador import seleccionar_usuario

def dibujar_boton(pantalla, texto, rect, fuente, imagen_boton, mouse_pos):

    boton_img = pygame.transform.scale(imagen_boton, (rect.width, rect.height))

    if rect.collidepoint(mouse_pos):
        boton_img.set_alpha(255)
    else:
        boton_img.set_alpha(180)

    pantalla.blit(boton_img, rect.topleft)

    texto_render = fuente.render(texto, True, (255, 255, 255))
    texto_rect = texto_render.get_rect(center=rect.center)
    pantalla.blit(texto_render, texto_rect)


def main():
    pygame.init()
    pygame.mixer.init()
    ancho, alto = 800, 600
    pantalla = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Minecraft Construction Tool")
    fuente = pygame.font.SysFont("Minecraft", 20)

    boton_jugar = pygame.Rect(ancho // 2 - 150, 350, 300, 60)
    boton_opciones = pygame.Rect(ancho // 2 - 150, 430, 300, 60)
    boton_salir = pygame.Rect(ancho // 2 - 150, 510, 300, 60)


    fondo = pygame.image.load("fondojuegominecraft.png")
    fondo = pygame.transform.scale(fondo, (800, 600))

    imagen_boton = pygame.image.load("boton.png").convert_alpha()

    pygame.mixer.music.load("MINECRAFT MENU MUSIC.mp3")
    pygame.mixer.music.play(-1)

    titulo = pygame.image.load("Minecraft-Logo-2013.png")
    titulo = pygame.transform.scale(titulo, (610, 350))
    rect_titulo = titulo.get_rect()
    rect_titulo.centerx = ancho // 2
    rect_titulo.top = 20

    reloj = pygame.time.Clock()

    slots_usuarios = ["", "", ""]

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar.collidepoint(mouse_pos):
                    nombre_usuario = seleccionar_usuario(slots_usuarios)
                    print(f"Usuario seleccionado: {nombre_usuario}")
                elif boton_opciones.collidepoint(mouse_pos):
                    print("Opciones...")
                elif boton_salir.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pantalla.blit(fondo, [0, 0])
        pantalla.blit(titulo, rect_titulo)

        dibujar_boton(pantalla, "JUGAR", boton_jugar, fuente, imagen_boton, mouse_pos)
        dibujar_boton(pantalla, "OPCIONES", boton_opciones, fuente, imagen_boton, mouse_pos)
        dibujar_boton(pantalla, "SALIR", boton_salir, fuente, imagen_boton, mouse_pos)

        pygame.display.flip()
        reloj.tick(60)  # 60 FPS

if __name__ == "__main__":
    main()








