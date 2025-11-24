import pygame
import json
from objetos import OBJETOS
from fabricacion import matriz_inventario

tick = pygame.transform.scale(pygame.image.load("botones y fondos\green-check-mark-icon-png-11.png"), (15, 15))
cruz = pygame.transform.scale(pygame.image.load("botones y fondos\cross-red-x-pixel-art.png"), (15, 15))

# Cargar recetas desde JSON
def cargar_recetas():
    with open("recetas.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["recetas"]

recetas = cargar_recetas()

def receta_disponible_inventario(inventario, receta):
    """
    Verifica si el inventario contiene TODOS los items necesarios para fabricar la receta,
    sin importar la posición en una mesa de crafteo.
    """
    ingredientes = receta.get("ingredientes")
    if not ingredientes:
        return False

    # Contar ingredientes de la receta
    requeridos = {}

    for fila in ingredientes:
        for obj in fila:
            if obj not in (None, ""):
                requeridos[obj] = requeridos.get(obj, 0) + 1

    # Contar inventario real
    disponibles = {}

    for f in range(3):
        for c in range(9):
            celda = inventario[f][c]
            if celda:
                nombre = celda["nombre"]
                cant = celda["cantidad"]
                disponibles[nombre] = disponibles.get(nombre, 0) + cant

    # Comparar requeridos vs disponibles
    for nombre, cant_req in requeridos.items():
        if disponibles.get(nombre, 0) < cant_req:
            return False

    return True

# ===========================
#   NUEVO RECETARIO ESTILO MC
# ===========================
def pantalla_recetario(pantalla):
    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont("Minecraft", 20)
    fuente_peq = pygame.font.SysFont("Minecraft", 16)

    categoria_seleccionada = "Todo"
    pagina_actual = 0
    recetas_por_pagina = 20
    search_text = ""

    # Iconos laterales
    iconos = [
    ("todo", pygame.transform.scale(pygame.image.load("objetos sprites\Compass_JE3_BE3.png"), (40, 40))),
    ("bloques", pygame.transform.scale(pygame.image.load("objetos sprites\Bricks_JE5_BE3.png"), (40, 40))),
    ("decoracion", pygame.transform.scale(pygame.image.load("objetos sprites\Stone_Axe.png"), (40, 40))),
    ("comida", pygame.transform.scale(pygame.image.load("objetos sprites/apple.png"), (40, 40))),
    ("redstone", pygame.transform.scale(pygame.image.load("objetos sprites\Redstone_Dust_JE2_BE2.png"), (40, 40))),
]

    ejecutando = True
    receta_seleccionada = None  # Guardará la receta clickeada
    while ejecutando:
        mouse_pos = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False

                # escribir en barra de búsqueda
                elif evento.key == pygame.K_BACKSPACE:
                    search_text = search_text[:-1]
                else:
                    if len(evento.unicode) == 1:
                        search_text += evento.unicode

            # click mouse
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    # botón cerrar
                    if cerrar_rect.collidepoint(mouse_pos):
                        ejecutando = False
                    
                    # flechas izquierda / derecha
                    if flecha_izq.collidepoint(mouse_pos):
                        pagina_actual = max(0, pagina_actual - 1)
                    if flecha_der.collidepoint(mouse_pos):
                        max_pag = max(0, (len(filtradas)-1)//recetas_por_pagina)
                        pagina_actual = min(max_pag, pagina_actual + 1)

                    # categorías
                    for i, (cat, img) in enumerate(iconos):
                        r = pygame.Rect(20, 80 + i*55, 40, 40)
                        if r.collidepoint(mouse_pos):
                            categoria_seleccionada = cat
                    
                    # Click en la grilla de objetos
                    x = 150
                    y = 90
                    ancho = 60
                    alto = 60
                    columnas = 5

                    inicio = pagina_actual * recetas_por_pagina
                    fin = inicio + recetas_por_pagina
                    pagina_items = filtradas[inicio:fin]

                    for i, receta in enumerate(pagina_items):
                        col = i % columnas
                        fila = i // columnas
                        rx = x + col * (ancho + 10)
                        ry = y + fila * (alto + 10)
                        rect = pygame.Rect(rx, ry, ancho, alto)
                        if rect.collidepoint(mouse_pos):
                            # Buscar la receta real en JSON
                            nombre_obj = receta["result"]
                            receta_real = next((r for r in recetas if r["result"] == nombre_obj), None)
                            receta_seleccionada = receta_real  # Puede ser None si no tiene receta
                            break

        # =========================
        # DIBUJO DE LA PANTALLA
        # =========================
        pantalla.fill((30, 30, 30))

        # Panel izquierdo
        pygame.draw.rect(pantalla, (200, 200, 200), (10, 10, 70, pantalla.get_height()-20))

        # Dibujar iconos
        for i, (cat, img) in enumerate(iconos):
            r = pygame.Rect(20, 80 + i * 55, 40, 40)
            pygame.draw.rect(pantalla, (150,150,150) if cat == categoria_seleccionada else (100,100,100), r, border_radius=5)
            pantalla.blit(img, r.topleft)

        # Panel central
        pygame.draw.rect(pantalla, (220, 220, 220), (100, 10, pantalla.get_width()-110, pantalla.get_height()-20))

        # Barra búsqueda
        pygame.draw.rect(pantalla, (50,50,50), (150, 30, 300, 35), border_radius=5)
        texto_busq = fuente_peq.render(search_text, True, (255,255,255))
        pantalla.blit(texto_busq, (160, 35))

        # Botón cerrar
        cerrar_rect = pygame.Rect(460, 30, 35, 35)
        pygame.draw.rect(pantalla, (180,60,60), cerrar_rect, border_radius=5)
        pantalla.blit(fuente_peq.render("X", True, (255,255,255)), (cerrar_rect.x+10, cerrar_rect.y+5))

        # ============================
        # FILTRADO DE RECETAS
        # ============================
        filtradas = []

        for nombre, datos in OBJETOS.items():
            tipo = datos["tipo"]

            # FILTRO POR CATEGORÍA
            if categoria_seleccionada == "comida":
                if tipo != "comida":
                    continue

            elif categoria_seleccionada == "decoracion":
                if tipo != "arma":
                    continue

            elif categoria_seleccionada == "redstone":
                if "redstone" not in nombre.lower():
                    continue

            elif categoria_seleccionada == "bloques":
                if tipo != "bloque":   # cuando agregues bloques funcionará
                    continue

            # FILTRO BÚSQUEDA
            if search_text.lower() not in nombre.lower():
                continue

            # Buscar si el OBJETO tiene receta real en el JSON
            receta_real = next((r for r in recetas if r["result"] == nombre), None)

            # Guardamos siempre result, y si tiene receta guardamos ingredientes también
            filtradas.append(receta_real if receta_real else {"result": nombre})

        # ============================
        # MOSTRAR RECETAS EN GRILLA
        # ============================
        x = 150
        y = 90
        ancho = 60
        alto = 60
        columnas = 5

        inicio = pagina_actual * recetas_por_pagina
        fin = inicio + recetas_por_pagina
        pagina_items = filtradas[inicio:fin]

        for i, receta in enumerate(pagina_items):
            col = i % columnas
            fila = i // columnas

            rx = x + col * (ancho + 10)
            ry = y + fila * (alto + 10)

            rect = pygame.Rect(rx, ry, ancho, alto)
            pygame.draw.rect(pantalla, (30, 30, 30), rect, 3)  # borde rojo

            objeto = OBJETOS.get(receta["result"])
            if objeto:
                sprite = objeto["sprite"]
                pantalla.blit(sprite, (rx+10, ry+10))

            # Solo si la receta tiene ingredientes reales
            if "ingredientes" in receta:
                se_puede = receta_disponible_inventario(matriz_inventario, receta)

                icono = tick if se_puede else cruz

                # esquina inferior derecha del cuadrado
                pantalla.blit(icono, (rx + ancho - 16, ry + alto - 18))

        # Mostrar matriz 3x3 de la receta seleccionada
        if receta_seleccionada is not None:
            start_x = pantalla.get_width() - 250
            start_y = 100
            tam_celda = 50
            espacio = 5

            ingredientes = receta_seleccionada.get("ingredientes", [[None]*3 for _ in range(3)])
            for f in range(3):
                for c in range(3):
                    x = start_x + c * (tam_celda + espacio)
                    y = start_y + f * (tam_celda + espacio)
                    rect = pygame.Rect(x, y, tam_celda, tam_celda)
                    pygame.draw.rect(pantalla, (180, 180, 180), rect)   # fondo celda
                    pygame.draw.rect(pantalla, (100, 100, 100), rect, 2) # borde celda

                    item = None
                    if f < len(ingredientes) and c < len(ingredientes[f]):
                        item = ingredientes[f][c]

                    if item and item in OBJETOS:
                        sprite = OBJETOS[item]["sprite"]
                        pantalla.blit(sprite, sprite.get_rect(center=rect.center))

        # ============================
        # PAGINACIÓN
        # ============================
        total_pag = max(1, (len(filtradas)-1) // recetas_por_pagina + 1)

        pag_text = fuente_peq.render(f"{pagina_actual+1}/{total_pag}", True, (0,0,0))
        pantalla.blit(pag_text, (330, pantalla.get_height()-50))

        flecha_izq = pygame.Rect(300, pantalla.get_height()-55, 25, 25)
        flecha_der = pygame.Rect(370, pantalla.get_height()-55, 25, 25)

        pygame.draw.rect(pantalla, (150,150,150), flecha_izq)
        pygame.draw.rect(pantalla, (150,150,150), flecha_der)

        pantalla.blit(fuente_peq.render("<", True, (0,0,0)), (flecha_izq.x+8, flecha_izq.y+4))
        pantalla.blit(fuente_peq.render(">", True, (0,0,0)), (flecha_der.x+8, flecha_der.y+4))

        pygame.display.flip()
        reloj.tick(60)