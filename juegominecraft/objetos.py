import pygame

def cargar_sprite(ruta):
    if not pygame.get_init():
        pygame.init()
        pygame.display.set_mode((1, 1))

    imagen = pygame.image.load(ruta).convert_alpha()
    imagen = pygame.transform.scale(imagen, (48, 48))
    return imagen


OBJETOS = {
    "madera": {"sprite": cargar_sprite("juegominecraft/objetos sprites/tronco_roble.png"), "tipo": "material"},
    "oro": {"sprite": cargar_sprite("juegominecraft/objetos sprites/gold.png"), "tipo": "material"},
    "espada": {"sprite": cargar_sprite("juegominecraft/objetos sprites/swordwood.png"), "tipo": "arma"},
    "manzana_dorada": {"sprite": cargar_sprite("juegominecraft/objetos sprites/goldenapple.png"), "tipo": "comida"},
    "manzana": {"sprite": cargar_sprite("juegominecraft/objetos sprites/apple.png"), "tipo": "comida"}
}


# === FUNCIÓN PARA COLOCAR OBJETOS INICIALES EN EL INVENTARIO ===
def spawnear_objetos_iniciales(matriz_inventario):
    matriz_inventario[0][0] = {"nombre": "madera", "sprite": OBJETOS["madera"]["sprite"], "cantidad": 1}
    matriz_inventario[0][1] = {"nombre": "oro", "sprite": OBJETOS["oro"]["sprite"], "cantidad": 1}
    matriz_inventario[0][2] = {"nombre": "espada", "sprite": OBJETOS["espada"]["sprite"], "cantidad": 1}
    matriz_inventario[1][0] = {"nombre": "manzana", "sprite": OBJETOS["manzana"]["sprite"], "cantidad": 1}
    matriz_inventario[1][1] = {"nombre": "manzana", "sprite": OBJETOS["manzana"]["sprite"], "cantidad": 1}

