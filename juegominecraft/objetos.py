#madera, metal, palo, pico, espada, blablabla

import pygame

def cargar_sprite(ruta):
    imagen = pygame.image.load(ruta).convert_alpha()
    return pygame.transform.scale(imagen, (48, 48))

OBJETOS = {
    "madera": {"sprite": cargar_sprite("juegominecraft\objetos sprites\\tronco_roble.png"), "tipo": "material"},
    "oro": {"sprite": cargar_sprite("juegominecraft\objetos sprites\gold.png"), "tipo": "material"},
    "espada": {"sprite": cargar_sprite("juegominecraft\objetos sprites\swordwood.png"), "tipo": "arma"},
    "manzana_dorada": {"sprite": cargar_sprite("juegominecraft\objetos sprites\goldenapple.png"), "tipo": "comida"},
    # etc.
}

