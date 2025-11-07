import pygame

def cargar_sprite(ruta):
    if not pygame.get_init():
        pygame.init()
        pygame.display.set_mode((1, 1))

    imagen = pygame.image.load(ruta).convert_alpha()
    return imagen


OBJETOS = {
    "madera": {"sprite": cargar_sprite("juegominecraft/objetos sprites/tronco_roble.png"), "tipo": "material"},
    "oro": {"sprite": cargar_sprite("juegominecraft/objetos sprites/gold.png"), "tipo": "material"},
    "espada": {"sprite": cargar_sprite("juegominecraft/objetos sprites/swordwood.png"), "tipo": "arma"},
    "manzana_dorada": {"sprite": cargar_sprite("juegominecraft/objetos sprites/goldenapple.png"), "tipo": "comida"},
}


# === FUNCIÓN PARA COLOCAR OBJETOS INICIALES EN EL INVENTARIO ===
def spawnear_objetos_iniciales(matriz_inventario):
    """
    Coloca algunos ítems del diccionario OBJETOS en la matriz de inventario.
    Modifica la matriz recibida por referencia.
    """
    # Ejemplo: colocar 4 objetos distintos en posiciones fijas
    matriz_inventario[0][0] = OBJETOS["madera"]["sprite"]
    matriz_inventario[0][1] = OBJETOS["oro"]["sprite"]
    matriz_inventario[0][2] = OBJETOS["espada"]["sprite"]
    matriz_inventario[1][0] = OBJETOS["manzana_dorada"]["sprite"]

