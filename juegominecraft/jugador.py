# import pygame
# import sys
# import csv
# import os

# RUTA_USUARIOS = "usuarios.csv"

# # ===========================
# # FUNCIONES DE CSV SIN TRY/EXCEPT
# # ===========================
# def cargar_usuarios():
#     """Carga los usuarios desde el CSV en una lista de 3 slots."""
#     slots = ["", "", ""]
#     if os.path.exists(RUTA_USUARIOS):
#         f = open(RUTA_USUARIOS, newline="", encoding="utf-8")
#         reader = csv.DictReader(f)
#         for fila in reader:
#             slot = int(fila["slot"])
#             nombre = fila["nombre"]
#             slots[slot] = nombre
#         f.close()
#     else:
#         guardar_usuarios(slots)  # crea CSV si no existe
#     return slots

# def guardar_usuarios(slots):
#     """Guarda la lista de slots en el CSV."""
#     f = open(RUTA_USUARIOS, "w", newline="", encoding="utf-8")
#     writer = csv.DictWriter(f, fieldnames=["slot", "nombre"])
#     writer.writeheader()
#     for i, nombre in enumerate(slots):
#         writer.writerow({"slot": i, "nombre": nombre})
#     f.close()

# # ===========================
# # INTERFAZ GRÁFICA
# # ===========================
# def dibujar_boton(pantalla, texto, rect, fuente, color_normal, color_hover, mouse_pos):
#     color = color_hover if rect.collidepoint(mouse_pos) else color_normal
#     pygame.draw.rect(pantalla, color, rect, border_radius=10)
#     texto_render = fuente.render(texto, True, (255, 255, 255))
#     texto_rect = texto_render.get_rect(center=rect.center)
#     pantalla.blit(texto_render, texto_rect)

# def seleccionar_usuario():
#     """Muestra la pantalla de selección/creación de usuario y devuelve el nombre seleccionado."""
#     pygame.init()
#     ancho, alto = 800, 600
#     pantalla = pygame.display.set_mode((ancho, alto))
#     pygame.display.set_caption("Seleccionar Usuario")
#     fuente = pygame.font.SysFont("Minecraft", 28)
#     reloj = pygame.time.Clock()

#     slots = cargar_usuarios()
#     mouse_pos = (0, 0)

#     # Fondo estilo Dirt
#     fondo = pygame.image.load("botones y fondos\Dirt_background_BE1.png").convert()
#     fondo = pygame.transform.scale(fondo, (ancho, alto))

#     # Rectángulos de los slots
#     botones_slots = []
#     ancho_btn, alto_btn = 400, 60
#     x_pos = 200
#     y_inicio = 150
#     espacio = 80
#     for i in range(3):
#         rect = pygame.Rect(x_pos, y_inicio + i * espacio, ancho_btn, alto_btn)
#         botones_slots.append(rect)

#     estado_input = False
#     input_text = ""
#     slot_seleccionado = None

#     while True:
#         mouse_pos = pygame.mouse.get_pos()
#         for evento in pygame.event.get():
#             if evento.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()

#             if estado_input:
#                 if evento.type == pygame.KEYDOWN:
#                     if evento.key == pygame.K_RETURN:
#                         if input_text.strip() != "":
#                             slots[slot_seleccionado] = input_text.strip()
#                             guardar_usuarios(slots)
#                         return slots[slot_seleccionado]
#                     elif evento.key == pygame.K_BACKSPACE:
#                         input_text = input_text[:-1]
#                     else:
#                         if len(input_text) < 20:
#                             input_text += evento.unicode
#             else:
#                 if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
#                     for i, rect in enumerate(botones_slots):
#                         if rect.collidepoint(mouse_pos):
#                             slot_seleccionado = i
#                             if slots[i] == "":
#                                 estado_input = True
#                                 input_text = ""
#                             else:
#                                 return slots[i]

#         # --- DIBUJO ---
#         pantalla.blit(fondo, (0, 0))  # <-- fondo Dirt

#         for i, rect in enumerate(botones_slots):
#             # Color del botón: gris oscuro normal, gris claro hover
#             color_normal = (50, 50, 50)
#             color_hover = (100, 100, 100)
#             texto = slots[i] if slots[i] != "" else "(vacio) - click para crear"
#             dibujar_boton(pantalla, texto, rect, fuente, color_normal, color_hover, mouse_pos)

#         if estado_input:
#             input_rect = pygame.Rect(200, 450, 400, 50)
#             pygame.draw.rect(pantalla, (0,0,0), input_rect)
#             pygame.draw.rect(pantalla, (255,255,255), input_rect, 2)
#             texto_input = fuente.render(input_text, True, (255,255,255))
#             pantalla.blit(texto_input, (input_rect.x+10, input_rect.y+10))

#             indicacion = fuente.render("Ingrese nombre y presione ENTER", True, (255,255,255))
#             pantalla.blit(indicacion, (200, 400))

#         pygame.display.flip()
#         reloj.tick(60)

# # ===========================
# # EJEMPLO DE USO
# # ===========================
# if __name__ == "__main__":
#     nombre = seleccionar_usuario()
#     print(f"Usuario seleccionado: {nombre}")











import pygame
import sys
import json

RUTA_USUARIOS = "usuarios.json"



def crear_json_inicial():
    datos = {
        "slots": [
            {"nombre": "", "objetos": [], "resultados": [[0]]},
            {"nombre": "", "objetos": [], "resultados": [[0]]},
            {"nombre": "", "objetos": [], "resultados": [[0]]}
        ]
    }
    f = open(RUTA_USUARIOS, "w", encoding="utf-8")
    json.dump(datos, f, indent=4)
    f.close()
    return datos


def cargar_usuarios():
    f = open(RUTA_USUARIOS, "a+", encoding="utf-8")
    f.seek(0)
    contenido = f.read()
    f.close()

    if contenido == "" or contenido.strip() == "":
        return crear_json_inicial()

    f = open(RUTA_USUARIOS, "r", encoding="utf-8")
    datos = json.load(f)
    f.close()

    return datos


def guardar_usuarios(datos):
    f = open(RUTA_USUARIOS, "w", encoding="utf-8")
    json.dump(datos, f, indent=4)
    f.close()

# ===========================
# INTERFAZ GRÁFICA
# ===========================

def dibujar_boton(pantalla, texto, rect, fuente, color_normal, color_hover, mouse_pos):
    color = color_hover if rect.collidepoint(mouse_pos) else color_normal
    pygame.draw.rect(pantalla, color, rect, border_radius=10)
    texto_render = fuente.render(texto, True, (255, 255, 255))
    texto_rect = texto_render.get_rect(center=rect.center)
    pantalla.blit(texto_render, texto_rect)


def seleccionar_usuario():
    pygame.init()
    ancho, alto = 800, 600
    pantalla = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Seleccionar Usuario")
    fuente = pygame.font.SysFont("Minecraft", 28)
    reloj = pygame.time.Clock()

    datos = cargar_usuarios()

    # Convertimos los nombres para el menú
    slots = [
        datos["slots"][0]["nombre"],
        datos["slots"][1]["nombre"],
        datos["slots"][2]["nombre"]
    ]

    mouse_pos = (0, 0)

    fondo = pygame.image.load("botones y fondos/Dirt_background_BE1.png").convert()
    fondo = pygame.transform.scale(fondo, (ancho, alto))

    botones_slots = []
    ancho_btn, alto_btn = 400, 60
    x_pos = 200
    y_inicio = 150
    espacio = 80

    for i in range(3):
        rect = pygame.Rect(x_pos, y_inicio + i * espacio, ancho_btn, alto_btn)
        botones_slots.append(rect)

    estado_input = False
    input_text = ""
    slot_seleccionado = None

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if estado_input:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        if input_text.strip() != "":
                            datos["slots"][slot_seleccionado]["nombre"] = input_text.strip()
                            guardar_usuarios(datos)
                        return datos["slots"][slot_seleccionado]["nombre"]

                    elif evento.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        if len(input_text) < 20:
                            input_text += evento.unicode

            else:
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    for i, rect in enumerate(botones_slots):
                        if rect.collidepoint(mouse_pos):
                            slot_seleccionado = i

                            if datos["slots"][i]["nombre"] == "":
                                estado_input = True
                                input_text = ""
                            else:
                                return datos["slots"][i]["nombre"]

        pantalla.blit(fondo, (0, 0))

        for i, rect in enumerate(botones_slots):
            color_normal = (50, 50, 50)
            color_hover = (100, 100, 100)

            texto = datos["slots"][i]["nombre"]
            if texto == "":
                texto = "(vacío) - click para crear"

            dibujar_boton(pantalla, texto, rect, fuente, color_normal, color_hover, mouse_pos)

        if estado_input:
            input_rect = pygame.Rect(200, 450, 400, 50)
            pygame.draw.rect(pantalla, (0,0,0), input_rect)
            pygame.draw.rect(pantalla, (255,255,255), input_rect, 2)
            texto_input = fuente.render(input_text, True, (255,255,255))
            pantalla.blit(texto_input, (input_rect.x+10, input_rect.y+10))

            indicacion = fuente.render("Ingrese nombre y presione ENTER", True, (255,255,255))
            pantalla.blit(indicacion, (200, 400))

        pygame.display.flip()
        reloj.tick(60)


if __name__ == "__main__":
    nombre = seleccionar_usuario()
    print("Usuario seleccionado:", nombre)
