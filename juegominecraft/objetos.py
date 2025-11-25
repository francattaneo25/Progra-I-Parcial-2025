import pygame

def cargar_sprite(ruta):
    if not pygame.get_init():
        pygame.init()
        pygame.display.set_mode((1, 1))

    imagen = pygame.image.load(ruta).convert_alpha()
    imagen = pygame.transform.scale(imagen, (48, 48))
    return imagen


OBJETOS = {
    "madera": {"sprite": cargar_sprite("objetos sprites/tronco_roble.png"), "tipo": "material"},
    "lingote oro": {"sprite": cargar_sprite("objetos sprites\gold.png"), "tipo": "material"},
    "espada madera": {"sprite": cargar_sprite("objetos sprites\swordwood.png"), "tipo": "arma"},
    "espada piedra": {"sprite": cargar_sprite("objetos sprites\Stone_Sword.png"), "tipo": "arma"},
    "espada hierro": {"sprite": cargar_sprite("objetos sprites\Iron_Sword.png"), "tipo": "arma"},
    "espada diamante": {"sprite": cargar_sprite("objetos sprites\Diamond_Sword.png"), "tipo": "arma"},
    "manzana_dorada": {"sprite": cargar_sprite("objetos sprites\goldenapple.png"), "tipo": "comida"},
    "manzana": {"sprite": cargar_sprite("objetos sprites/apple.png"), "tipo": "comida"},
    "diamante": {"sprite": cargar_sprite("objetos sprites\diamond.png"), "tipo": "material"},
    "palo": {"sprite": cargar_sprite("objetos sprites/stick.png"), "tipo": "material"},
    "tablon de madera": {"sprite": cargar_sprite("objetos sprites/Oak_Planks.png"), "tipo": "material"},
    "lingote hierro": {"sprite": cargar_sprite("objetos sprites/Iron_Ingot.png"), "tipo": "material"},
    "piedra": {"sprite": cargar_sprite("objetos sprites/Cobblestone.png"), "tipo": "material"},
    "carbon": {"sprite": cargar_sprite("objetos sprites/Coal.png"), "tipo": "material"},
    "antorcha": {"sprite": cargar_sprite("objetos sprites/Torch.png"), "tipo": "material"},
    "antorcha redstone": {"sprite": cargar_sprite("objetos sprites/Redstone_Torch.png"), "tipo": "material"},
    "redstone": {"sprite": cargar_sprite("objetos sprites/Redstone_Dust_JE2_BE2.png"), "tipo": "material"},
    "zanahoria": {"sprite": cargar_sprite("objetos sprites/Carrot.png"), "tipo": "comida"},
    "zanahoria dorada": {"sprite": cargar_sprite("objetos sprites/Golden_Carrot.png"), "tipo": "comida"},
    "pepita oro": {"sprite": cargar_sprite("objetos sprites/Pepita_oro.png"), "tipo": "material"},
    "lonja melon": {"sprite": cargar_sprite("objetos sprites\Melon_Slice.png"), "tipo": "comida"},
    "melon": {"sprite": cargar_sprite("objetos sprites\Melon.png"), "tipo": "comida"},
    "hacha madera": {"sprite": cargar_sprite("objetos sprites\Wooden_Axe.png"), "tipo": "arma"},
    "hacha piedra": {"sprite": cargar_sprite("objetos sprites\Stone_Axe.png"), "tipo": "arma"},
    "hacha hierro": {"sprite": cargar_sprite("objetos sprites\Iron_Axe.png"), "tipo": "arma"},
    "hacha oro": {"sprite": cargar_sprite("objetos sprites\Golden_Axe.png"), "tipo": "arma"},
    "hacha diamante": {"sprite": cargar_sprite("objetos sprites\Diamond_Axe.png"), "tipo": "arma"},
    "espada oro": {"sprite": cargar_sprite("objetos sprites\Golden_Sword.png"), "tipo": "arma"},
    "pala madera": {"sprite": cargar_sprite("objetos sprites\Wooden_Shovel.png"), "tipo": "arma"},
    "pala piedra": {"sprite": cargar_sprite("objetos sprites\Stone_Shovel.png"), "tipo": "arma"},
    "pala hierro": {"sprite": cargar_sprite("objetos sprites\Iron_Shovel.png"), "tipo": "arma"},
    "pala oro": {"sprite": cargar_sprite("objetos sprites\Golden_Shovel.png"), "tipo": "arma"},
    "pala diamante": {"sprite": cargar_sprite("objetos sprites\Diamond_Shovel.png"), "tipo": "arma"},
    "horno": {"sprite": cargar_sprite("objetos sprites/Furnace.png"), "tipo": "material"},
    "trigo": {"sprite": cargar_sprite("objetos sprites/Wheat.png"), "tipo": "material"},
    "pan": {"sprite": cargar_sprite("objetos sprites/Pan.png"), "tipo": "comida"},
}


# === FUNCIÓN PARA COLOCAR OBJETOS INICIALES EN EL INVENTARIO ===
def spawnear_objetos_iniciales(matriz_inventario):
    matriz_inventario[0][0] = {"nombre": "madera", "sprite": OBJETOS["madera"]["sprite"], "cantidad": 1}
    matriz_inventario[0][1] = {"nombre": "lingote oro", "sprite": OBJETOS["lingote oro"]["sprite"], "cantidad": 1}
    matriz_inventario[0][2] = {"nombre": "espada madera", "sprite": OBJETOS["espada madera"]["sprite"], "cantidad": 1}
    matriz_inventario[1][0] = {"nombre": "manzana", "sprite": OBJETOS["manzana"]["sprite"], "cantidad": 1}
    matriz_inventario[1][1] = {"nombre": "manzana", "sprite": OBJETOS["manzana"]["sprite"], "cantidad": 1}
    matriz_inventario[1][3] = {"nombre": "diamante", "sprite": OBJETOS["diamante"]["sprite"], "cantidad": 1}
