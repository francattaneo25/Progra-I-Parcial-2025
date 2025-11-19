import pygame
import json
from objetos import OBJETOS

# Cargar recetas desde JSON
def cargar_recetas():
    with open("juegominecraft/recetas.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["recetas"]

recetas = cargar_recetas()

def pantalla_recetario(pantalla):
    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont("Minecraft", 18)
    
    scroll_y = 0

    ejecutando = True
    while ejecutando:
        mouse_pos = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                ejecutando = False

            # Scroll rueda del mouse
            elif evento.type == pygame.MOUSEWHEEL:
                scroll_y += evento.y * 30  # velocidad scroll

        # === DIBUJO ===
        pantalla.fill((20, 20, 20))

        y = 50 + scroll_y

        # Mostrar cada receta en una fila
        for receta in recetas:
            texto = fuente.render(receta["result"], True, (255,255,255))
            pantalla.blit(texto, (50, y))

            # Mostrar sprite del resultado
            obj = OBJETOS.get(receta["result"])
            if obj:
                sprite = obj["sprite"]
                sprite_rect = sprite.get_rect(topleft=(200, y))
                pantalla.blit(sprite, sprite_rect)

            y += 80

        titulo = fuente.render("Recetario", True, (255,255,0))
        pantalla.blit(titulo, (pantalla.get_width()//2 - titulo.get_width()//2, 10))

        pygame.display.flip()
        reloj.tick(60)