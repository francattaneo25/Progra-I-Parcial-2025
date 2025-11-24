import pygame
import random
from objetos import spawnear_objetos_iniciales, OBJETOS

# === MATRIZ DE INVENTARIO ===
matriz_inventario = [
    [None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None]
]

# Al iniciar el inventario, spawneamos objetos iniciales
spawnear_objetos_iniciales(matriz_inventario)


# --- FUNCIÓN PARA DIBUJAR INVENTARIO ---
def dibujar_inventario(pantalla, matriz, x_inicial, y_inicial, tam_celda, item_en_mano, mouse_pos):
    """Dibuja la cuadrícula del inventario y coloca los sprites dentro de cada celda."""
    for fila in range(len(matriz)):
        for col in range(len(matriz[fila])):
            x = x_inicial + col * tam_celda
            y = y_inicial + fila * tam_celda

            rect = pygame.Rect(x, y, tam_celda, tam_celda)
            pygame.draw.rect(pantalla, (80, 80, 80), rect, 2)

            if matriz[fila][col] is not None:
                # Si el slot contiene un dict (como {"nombre":..., "sprite":..., "cantidad":...})
                if isinstance(matriz[fila][col], dict):
                    sprite = matriz[fila][col]["sprite"]
                else:
                    sprite = matriz[fila][col]

                sprite_rect = sprite.get_rect(center=rect.center)
                pantalla.blit(sprite, sprite_rect)

    if item_en_mano is not None:
        sprite_rect = item_en_mano.get_rect(center=mouse_pos)
        pantalla.blit(item_en_mano, sprite_rect)


# --- NUEVA FUNCIÓN: PANTALLA DE MOCHILA ---
def mostrar_mochila(pantalla):
    """Muestra una cuadrícula con todos los objetos disponibles para agregar al inventario."""
    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont("Minecraft", 18)

    objetos_lista = list(OBJETOS.items())
    columnas = 6
    tam_celda = 80
    margen_x, margen_y = 120, 120
    espacio = 30
    ancho, alto = pantalla.get_size()

    # Paginación
    items_por_pagina = 18  # 3 filas × 6 columnas
    pagina_actual = 0

    ejecutando = True
    while ejecutando:
        mouse_pos = pygame.mouse.get_pos()

        # ------------------------------------------------------------------
        # EVENTOS
        # ------------------------------------------------------------------
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                ejecutando = False

            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:

                # Detectar click en flechas
                if flecha_izq.collidepoint(mouse_pos) and pagina_actual > 0:
                    pagina_actual -= 1
                    continue

                if flecha_der.collidepoint(mouse_pos) and pagina_actual < total_pag - 1:
                    pagina_actual += 1
                    continue

                # Click en los objetos visibles en esta página
                inicio = pagina_actual * items_por_pagina
                fin = inicio + items_por_pagina
                pagina_items = objetos_lista[inicio:fin]

                for i, (nombre, datos) in enumerate(pagina_items):
                    fila = i // columnas
                    col = i % columnas

                    rect = pygame.Rect(
                        margen_x + col * (tam_celda + espacio),
                        margen_y + fila * (tam_celda + espacio),
                        tam_celda,
                        tam_celda
                    )

                    if rect.collidepoint(mouse_pos):
                        agregar_a_inventario(nombre, datos)
                        ejecutando = False
                        break

        # ------------------------------------------------------------------
        # DIBUJAR PANTALLA
        # ------------------------------------------------------------------
        pantalla.fill((40, 40, 40))

        titulo = fuente.render("MOCHILA - Haz clic en un objeto para agregarlo", True, (255, 255, 255))
        pantalla.blit(titulo, (ancho // 2 - titulo.get_width() // 2, 50))

        # Items de la página actual
        inicio = pagina_actual * items_por_pagina
        fin = inicio + items_por_pagina
        pagina_items = objetos_lista[inicio:fin]

        # Dibujar objetos
        for i, (nombre, datos) in enumerate(pagina_items):
            fila = i // columnas
            col = i % columnas
            x = margen_x + col * (tam_celda + espacio)
            y = margen_y + fila * (tam_celda + espacio)

            rect = pygame.Rect(x, y, tam_celda, tam_celda)

            pygame.draw.rect(pantalla, (80, 80, 80), rect, border_radius=8)
            pygame.draw.rect(pantalla, (200, 200, 200), rect, 2, border_radius=8)

            sprite = pygame.transform.scale(datos["sprite"], (60, 60))
            pantalla.blit(sprite, sprite.get_rect(center=rect.center))

            texto_nombre = fuente.render(nombre, True, (255, 255, 255))
            pantalla.blit(texto_nombre, (x + (tam_celda // 2 - texto_nombre.get_width() // 2), y + tam_celda + 5))

        # ------------------------------------------------------------------
        # PAGINACIÓN VISUAL
        # ------------------------------------------------------------------
        total_pag = max(1, (len(objetos_lista) - 1) // items_por_pagina + 1)

        # Texto "1/5"
        pag_text = fuente.render(f"{pagina_actual + 1}/{total_pag}", True, (255, 255, 255))
        pantalla.blit(pag_text, (ancho // 2 - pag_text.get_width() // 2, alto - 60))

        # Flechas
        flecha_izq = pygame.Rect(ancho // 2 - 70, alto - 65, 30, 30)
        flecha_der = pygame.Rect(ancho // 2 + 40, alto - 65, 30, 30)

        pygame.draw.rect(pantalla, (150, 150, 150), flecha_izq, border_radius=5)
        pygame.draw.rect(pantalla, (150, 150, 150), flecha_der, border_radius=5)

        pantalla.blit(fuente.render("<", True, (0, 0, 0)), (flecha_izq.x + 8, flecha_izq.y + 2))
        pantalla.blit(fuente.render(">", True, (0, 0, 0)), (flecha_der.x + 8, flecha_der.y + 2))

        # ------------------------------------------------------------------

        pygame.display.flip()
        reloj.tick(60)


# --- FUNCIÓN PARA AGREGAR OBJETOS AL INVENTARIO ---
def agregar_a_inventario(nombre, datos):
    """Agrega un objeto a una posición vacía aleatoria del inventario."""
    posiciones_vacias = [
        (f, c)
        for f in range(len(matriz_inventario))
        for c in range(len(matriz_inventario[f]))
        if matriz_inventario[f][c] is None
    ]

    if not posiciones_vacias:
        print("⚠️ Inventario lleno.")
        return

    fila, col = random.choice(posiciones_vacias)
    matriz_inventario[fila][col] = {"nombre": nombre, "sprite": datos["sprite"], "cantidad": 1}
    print(f"✅ {nombre} agregado a ({fila}, {col})")


# --- PANTALLA PRINCIPAL DE INVENTARIO ---
def pantalla_inventario(pantalla):
    reloj = pygame.time.Clock()
    tam_celda = 64
    x_inicial = pantalla.get_width() // 2 - (9 * tam_celda) // 2
    y_inicial = 200

    item_en_mano = None
    origen = None

    ejecutando = True
    while ejecutando:
        mouse_pos = pygame.mouse.get_pos()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False
                elif evento.key == pygame.K_m:
                    mostrar_mochila(pantalla)  # ← abre la mochila al presionar M

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                col = (mouse_pos[0] - x_inicial) // tam_celda
                fila = (mouse_pos[1] - y_inicial) // tam_celda

                if 0 <= fila < len(matriz_inventario) and 0 <= col < len(matriz_inventario[0]):
                    if matriz_inventario[fila][col] is not None:
                        item_en_mano = matriz_inventario[fila][col]["sprite"]
                        origen = (fila, col)
                        matriz_inventario[fila][col] = None

            elif evento.type == pygame.MOUSEBUTTONUP and item_en_mano is not None:
                col = (mouse_pos[0] - x_inicial) // tam_celda
                fila = (mouse_pos[1] - y_inicial) // tam_celda

                if 0 <= fila < len(matriz_inventario) and 0 <= col < len(matriz_inventario[0]):
                    if matriz_inventario[fila][col] is None:
                        matriz_inventario[fila][col] = {"nombre": "objeto", "sprite": item_en_mano, "cantidad": 1}
                    else:
                        matriz_inventario[origen[0]][origen[1]], matriz_inventario[fila][col] = matriz_inventario[fila][col], {"nombre": "objeto", "sprite": item_en_mano, "cantidad": 1}
                else:
                    matriz_inventario[origen[0]][origen[1]] = {"nombre": "objeto", "sprite": item_en_mano, "cantidad": 1}

                item_en_mano = None
                origen = None

        pantalla.fill((50, 50, 50))
        dibujar_inventario(pantalla, matriz_inventario, x_inicial, y_inicial, tam_celda, item_en_mano, mouse_pos)

        fuente = pygame.font.SysFont("Minecraft", 20)
        texto = fuente.render("Presioná M para abrir la mochila", True, (255, 255, 255))
        pantalla.blit(texto, (20, 20))

        pygame.display.flip()
        reloj.tick(60)
