import pygame
import sys
from jugador import seleccionar_usuario
from fabricacion import pantalla_fabricacion

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


    fondo = pygame.image.load("juegominecraft\\botones y fondos\\fondojuegominecraft.png")
    fondo = pygame.transform.scale(fondo, (800, 600))

    imagen_boton = pygame.image.load("juegominecraft/botones y fondos/boton.png").convert_alpha()

    pygame.mixer.music.load(r"juegominecraft\botones y fondos\\MINECRAFT MENU MUSIC.mp3")
    pygame.mixer.music.play(-1)

    titulo = pygame.image.load("juegominecraft\\botones y fondos\Minecraft-Logo-2013.png")
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
                    menu_jugar(pantalla, fuente, fondo)
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
        reloj.tick(60)

def menu_jugar(pantalla, fuente, fondo):
    """Submenú que aparece después de elegir usuario."""
    reloj = pygame.time.Clock()
    ancho, alto = pantalla.get_size()
    
    # Fondo
    fondo = pygame.image.load("juegominecraft/botones y fondos/Dirt_background_BE1.png").convert()
    fondo = pygame.transform.scale(fondo, (ancho, alto))

    # Imágenes de íconos
    img_fabricar = pygame.image.load("juegominecraft/botones y fondos/Crafting_Table_JE4_BE3.png").convert_alpha()
    img_mochila = pygame.image.load("juegominecraft/botones y fondos/mochila.jpg").convert_alpha()
    img_fabricar = pygame.transform.scale(img_fabricar, (120, 120))
    img_mochila = pygame.transform.scale(img_mochila, (120, 120))

    # Imagen de botón base y hover
    boton_base = pygame.image.load("juegominecraft/botones y fondos/boton chico.png").convert_alpha()
    boton_hover = boton_base.copy()
    boton_hover.set_alpha(255)
    boton_base.set_alpha(180)

    # Definir rectángulos
    rect_fabricar = pygame.Rect(ancho // 2 - 240, 340, 120, 60)
    rect_objetos = pygame.Rect(ancho // 2 + 120, 340, 120, 60)
    rect_volver = pygame.Rect(ancho // 2 - 80, 520, 100, 45)

    # Definir lista de botones (para evitar repetir if)
    botones = [
        {"nombre": "Fabricar", "rect": rect_fabricar},
        {"nombre": "Objetos", "rect": rect_objetos},
        {"nombre": "Volver", "rect": rect_volver}
    ]

    en_submenu = True
    while en_submenu:
        mouse_pos = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                for boton in botones:
                    if boton["rect"].collidepoint(mouse_pos):
                        if boton["nombre"] == "Fabricar":
                            print("Abriendo mesa de crafteo...")
                            pantalla_fabricacion(pantalla)
                        elif boton["nombre"] == "Objetos":
                            print("Abriendo mochila / inventario...")
                            from inventario import pantalla_inventario
                            pantalla_inventario(pantalla)
                        elif boton["nombre"] == "Volver":
                            en_submenu = False

        # Fondo
        pantalla.blit(fondo, [0, 0])

        # Dibujar íconos arriba de los botones
        pantalla.blit(img_fabricar, img_fabricar.get_rect(center=(rect_fabricar.centerx, rect_fabricar.centery - 100)))
        pantalla.blit(img_mochila, img_mochila.get_rect(center=(rect_objetos.centerx, rect_objetos.centery - 100)))

        # Dibujar todos los botones de forma genérica
        for boton in botones:
            hover = boton["rect"].collidepoint(mouse_pos)
            imagen = boton_hover if hover else boton_base
            pantalla.blit(imagen, imagen.get_rect(center=boton["rect"].center))

            texto = fuente.render(boton["nombre"], True, (255, 255, 255))
            texto_rect = texto.get_rect(center=boton["rect"].center)
            pantalla.blit(texto, texto_rect)

        pygame.display.flip()
        reloj.tick(60)

if __name__ == "__main__":
    main()








