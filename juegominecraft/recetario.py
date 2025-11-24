import pygame
import json
from objetos import OBJETOS

# Cargar recetas desde JSON
def cargar_recetas():
    with open("recetas.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["recetas"]

recetas = cargar_recetas()

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
    ("decoracion", pygame.transform.scale(pygame.image.load("objetos sprites\Stone_Axe_JE2_BE2.png"), (40, 40))),
    ("comida", pygame.transform.scale(pygame.image.load("objetos sprites/apple.png"), (40, 40))),
    ("redstone", pygame.transform.scale(pygame.image.load("objetos sprites\Redstone_Dust_JE2_BE2.png"), (40, 40))),
]

    ejecutando = True
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

        for r in recetas:
            nombre = r["result"].lower()

            # filtrar por categoría
            if categoria_seleccionada != "todo":
                if r.get("categoria", "todo") != categoria_seleccionada:
                    continue

            # filtrar búsqueda
            if search_text.lower() not in nombre:
                continue

            filtradas.append(r)

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
            pygame.draw.rect(pantalla, (200, 60, 60), rect, 3)  # borde rojo

            objeto = OBJETOS.get(receta["result"])
            if objeto:
                sprite = objeto["sprite"]
                pantalla.blit(sprite, (rx+10, ry+10))

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