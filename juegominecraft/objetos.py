#madera, metal, palo, pico, espada, blablabla

import pygame

def cargar_sprite(ruta):
    if not pygame.get_init():
        pygame.init()
        pygame.display.set_mode((1, 1))

    imagen = pygame.image.load(ruta).convert_alpha()
    return imagen

OBJETOS = {
    "madera": {"sprite": cargar_sprite("juegominecraft/objetos sprites/tronco_roble.png"), "tipo": "material"},
    "oro": {"sprite": cargar_sprite("juegominecraft\\objetos sprites\\gold.png"), "tipo": "material"},
    "espada": {"sprite": cargar_sprite("juegominecraft\\objetos sprites\\swordwood.png"), "tipo": "arma"},
    "manzana_dorada": {"sprite": cargar_sprite("juegominecraft\\objetos sprites\\goldenapple.png"), "tipo": "comida"},
    # etc.
}

