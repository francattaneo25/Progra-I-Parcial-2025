import pygame
import json
from inventario import matriz_inventario
from objetos import OBJETOS
from recetario import pantalla_recetario

# === MATRIZ DE FABRICACIÓN ===
mesa_fabricacion = [
    [None, None, None],
    [None, None, None],
    [None, None, None]
]

# Resultado de la mesa (1x1)
resultado = [[None]]


def pantalla_fabricacion(pantalla):
    """Muestra la mesa de crafteo y el inventario."""
    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont("Minecraft", 16)

    tablero_img = pygame.image.load("juegominecraft/botones y fondos/Tablero.png").convert_alpha()
    tablero_img = pygame.transform.scale(tablero_img, (532, 499))
    rect_tablero = tablero_img.get_rect(center=(pantalla.get_width() // 2, pantalla.get_height() // 2))

    tam_celda = 50
    tam_celda_resultado = 70
    tam_celda_inv = 55
    inicio_fab_x, inicio_fab_y = rect_tablero.left + 95, rect_tablero.top + 55
    inicio_result_x, inicio_result_y = rect_tablero.left + 360, rect_tablero.top + 90
    inicio_inv_x, inicio_inv_y = rect_tablero.left + 20, rect_tablero.top + 250

    # --- BOTÓN INVISIBLE DEL LIBRITO VERDE ---
    libro_x = inicio_fab_x - 70   # ← si querés más pegado, bajalo a -35
    libro_y = inicio_fab_y + 50   # centrado verticalmente
    boton_recetario = pygame.Rect(libro_x, libro_y, 50, 50)

    # Variables para drag & drop
    item_en_mano = None
    origen = None

    ejecutando = True
    while ejecutando:
        mouse_pos = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                ejecutando = False

            # === CLICK IZQUIERDO (tomar ítem) ===
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:

                if boton_recetario.collidepoint(mouse_pos):
                    pantalla_recetario(pantalla)
                    continue
                
                # --- Click en la mesa de crafteo ---
                col_fab = (mouse_pos[0] - inicio_fab_x) // tam_celda
                fila_fab = (mouse_pos[1] - inicio_fab_y) // tam_celda

                if 0 <= fila_fab < 3 and 0 <= col_fab < 3:
                    if mesa_fabricacion[fila_fab][col_fab]:
                        item_en_mano = mesa_fabricacion[fila_fab][col_fab]
                        mesa_fabricacion[fila_fab][col_fab] = None
                        origen = ("mesa", fila_fab, col_fab)
                    continue

                # --- Click en el inventario ---
                col_inv = (mouse_pos[0] - inicio_inv_x) // tam_celda
                fila_inv = (mouse_pos[1] - inicio_inv_y) // tam_celda

                if 0 <= fila_inv < 3 and 0 <= col_inv < 9:
                    if matriz_inventario[fila_inv][col_inv]:
                        item_en_mano = matriz_inventario[fila_inv][col_inv]
                        matriz_inventario[fila_inv][col_inv] = None
                        origen = ("inv", fila_inv, col_inv)
                    continue


                # --- Click en el resultado ---
                col_res = (mouse_pos[0] - inicio_result_x) // tam_celda_resultado
                fila_res = (mouse_pos[1] - inicio_result_y) // tam_celda_resultado

                if 0 <= fila_res < 1 and 0 <= col_res < 1:
                    if resultado[0][0]:
                        item_en_mano = resultado[0][0]
                        resultado[0][0] = None
                        origen = ("resultado", 0, 0)
                    continue
                
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 3:

                # --- Mesa ---
                col_fab = (mouse_pos[0] - inicio_fab_x) // tam_celda
                fila_fab = (mouse_pos[1] - inicio_fab_y) // tam_celda

                if 0 <= fila_fab < 3 and 0 <= col_fab < 3:
                    celda = mesa_fabricacion[fila_fab][col_fab]
                    if celda and item_en_mano is None:
                        item_en_mano = {"nombre": celda["nombre"], "sprite": celda["sprite"], "cantidad": 1}
                        celda["cantidad"] -= 1
                        if celda["cantidad"] == 0:
                            mesa_fabricacion[fila_fab][col_fab] = None
                        origen = ("mesa", fila_fab, col_fab)
                    continue

                # --- Inventario ---
                col_inv = (mouse_pos[0] - inicio_inv_x) // tam_celda
                fila_inv = (mouse_pos[1] - inicio_inv_y) // tam_celda

                if 0 <= fila_inv < 3 and 0 <= col_inv < 9:
                    celda = matriz_inventario[fila_inv][col_inv]
                    if celda and item_en_mano is None:
                        item_en_mano = {"nombre": celda["nombre"], "sprite": celda["sprite"], "cantidad": 1}
                        celda["cantidad"] -= 1
                        if celda["cantidad"] == 0:
                            matriz_inventario[fila_inv][col_inv] = None
                        origen = ("inv", fila_inv, col_inv)
                    continue

                # --- Resultado ---
                col_res = (mouse_pos[0] - inicio_result_x) // tam_celda_resultado
                fila_res = (mouse_pos[1] - inicio_result_y) // tam_celda_resultado

                if 0 <= fila_res < 1 and 0 <= col_res < 1:
                    celda_resultado = resultado[0][0]
                    if celda_resultado:
                        # 1) Tomo el item de resultado
                        item_en_mano = celda_resultado
                        resultado[0][0] = None
                        origen = ("resultado", 0, 0)
                        # 2) CONSUMIR los materiales de la mesa según la receta
                        for fila in range(3):
                            for col in range(3):
                                if mesa_fabricacion[fila][col]:
                                    mesa_fabricacion[fila][col]["cantidad"] -= 1
                                    if mesa_fabricacion[fila][col]["cantidad"] <= 0:
                                        mesa_fabricacion[fila][col] = None
                        continue

            # === SOLTAR EL CLICK (soltar ítem) ===
            elif evento.type == pygame.MOUSEBUTTONUP and item_en_mano is not None:
                # --- Soltar en la mesa de crafteo ---
                col = (mouse_pos[0] - inicio_fab_x) // tam_celda
                fila = (mouse_pos[1] - inicio_fab_y) // tam_celda

                if 0 <= fila < 3 and 0 <= col < 3:
                    celda = mesa_fabricacion[fila][col]
                    if celda is None:
                        mesa_fabricacion[fila][col] = item_en_mano
                        verificar_receta()
                    else:
                        # Si hay algo, lo devolvemos a su origen
                        if origen[0] == "inv":
                            matriz_inventario[origen[1]][origen[2]] = item_en_mano
                        else:
                            mesa_fabricacion[origen[1]][origen[2]] = item_en_mano
                    item_en_mano = None
                    origen = None
                    continue

                # --- Soltar en el inventario ---
                col = (mouse_pos[0] - inicio_inv_x) // tam_celda
                fila = (mouse_pos[1] - inicio_inv_y) // tam_celda
                if 0 <= fila < 3 and 0 <= col < 9:
                    celda = matriz_inventario[fila][col]

                    # Si está vacía, simplemente soltamos el ítem
                    if celda is None:
                        matriz_inventario[fila][col] = item_en_mano

                    # Si hay un ítem igual, sumamos cantidades
                    elif celda["nombre"] == item_en_mano["nombre"]:
                        celda["cantidad"] += item_en_mano["cantidad"]

                    # Si hay un ítem diferente, los intercambiamos
                    else:
                        matriz_inventario[fila][col], item_en_mano = item_en_mano, celda

                    item_en_mano = None
                    origen = None

        # === DIBUJO ===
        pantalla.fill((0, 0, 0))
        pantalla.blit(tablero_img, rect_tablero)

        color_lineas = (0, 0, 0)  # negro
        grosor_linea = 1

        # Mesa de crafteo
        for f in range(3):
            for c in range(3):
                rect = pygame.Rect(inicio_fab_x + c * tam_celda, inicio_fab_y + f * tam_celda, tam_celda, tam_celda)
                pygame.draw.rect(pantalla, color_lineas, rect, grosor_linea)  # <-- marco negro
                if mesa_fabricacion[f][c]:
                    item = mesa_fabricacion[f][c]
                    sprite = item["sprite"]
                    sprite_rect = sprite.get_rect(center=rect.center)
                    pantalla.blit(sprite, sprite_rect)

        # Resultado
        rect_res = pygame.Rect(inicio_result_x, inicio_result_y, tam_celda_resultado, tam_celda_resultado)
        pygame.draw.rect(pantalla, color_lineas, rect_res, grosor_linea)
        if resultado[0][0]:
            sprite = resultado[0][0]["sprite"]
            sprite_rect = sprite.get_rect(center=rect_res.center)
            pantalla.blit(sprite, sprite_rect)

        # Inventario
        for f in range(3):
            for c in range(9):
                rect = pygame.Rect(
                    inicio_inv_x + c * tam_celda_inv,
                    inicio_inv_y + f * tam_celda_inv,
                    tam_celda_inv,
                    tam_celda_inv
                )
                pygame.draw.rect(pantalla, color_lineas, rect, grosor_linea)  # Marco negro

                if matriz_inventario[f][c]:
                    item = matriz_inventario[f][c]
                    sprite = item["sprite"]
                    sprite_rect = sprite.get_rect(center=rect.center)
                    pantalla.blit(sprite, sprite_rect)

                    # Mostrar cantidad si hay más de 1
                    if item["cantidad"] > 1:
                        fuente_cant = pygame.font.SysFont("Minecraft", 14, bold=True)
                        texto_cant = fuente_cant.render(str(item["cantidad"]), True, (255, 255, 255))
                        sombra = fuente_cant.render(str(item["cantidad"]), True, (0, 0, 0))

                        x = rect.right - texto_cant.get_width() - 4
                        y = rect.bottom - texto_cant.get_height() - 2
                        pantalla.blit(sombra, (x + 1, y + 1))
                        pantalla.blit(texto_cant, (x, y))

        # Ítem en mano (sigue el cursor)
        if item_en_mano:
            sprite_rect = item_en_mano["sprite"].get_rect(center=mouse_pos)
            pantalla.blit(item_en_mano["sprite"], sprite_rect)

            if item_en_mano["cantidad"] > 1:
                fuente_cant = pygame.font.SysFont("Minecraft", 14, bold=True)
                texto_cant = fuente_cant.render(str(item_en_mano["cantidad"]), True, (255, 255, 255))
                sombra = fuente_cant.render(str(item_en_mano["cantidad"]), True, (0, 0, 0))
                x = sprite_rect.right - texto_cant.get_width() - 4
                y = sprite_rect.bottom - texto_cant.get_height() - 2
                pantalla.blit(sombra, (x + 1, y + 1))
                pantalla.blit(texto_cant, (x, y))

        texto = fuente.render("Mesa de Crafteo", True, (255, 255, 255))
        pantalla.blit(texto, (pantalla.get_width()//2 - texto.get_width()//2, 15))
        pygame.draw.rect(pantalla, (0, 0, 0), boton_recetario, 1)

        pygame.display.flip()
        reloj.tick(60)


def cargar_recetas_desde_json(ruta_archivo: str) -> list:
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        data = json.load(archivo)
    return data["recetas"]
recetas = cargar_recetas_desde_json("juegominecraft/recetas.json")

def coincide_patron(patron_mesa, patron_receta):
    for f in range(3):
        for c in range(3):
            if patron_mesa[f][c] != patron_receta[f][c]:
                return False
    return True


# === FUNCIÓN PARA FABRICAR ===
def fabricar_objeto(nombre_objeto: str):
    objeto = OBJETOS.get(nombre_objeto)
    if objeto:
        return objeto["sprite"]
    return None


# === FUNCIÓN PARA VERIFICAR SI LA MESA COINCIDE CON ALGUNA RECETA ===
def verificar_receta():
    patron_actual = [
        [celda["nombre"] if celda else None for celda in fila]
        for fila in mesa_fabricacion
    ]

    for receta in recetas:
        patron = receta["ingredientes"]
        nombre_resultado = receta["result"]

        if coincide_patron(patron_actual, patron):
            objeto = OBJETOS.get(nombre_resultado)
            if objeto:
                resultado[0][0] = {
                    "nombre": nombre_resultado,
                    "sprite": objeto["sprite"],
                    "cantidad": 1
                }
                print(f"✅ Receta encontrada: {nombre_resultado}")
                return nombre_resultado

    resultado[0][0] = None
    print("❌ Ninguna receta coincide")
    return None

# === FUNCIÓN PARA LIMPIAR LA MESA ===
def limpiar_mesa():
    """Reinicia la mesa de fabricación."""
    for i in range(3):
        for j in range(3):
            mesa_fabricacion[i][j] = None
    resultado[0][0] = None