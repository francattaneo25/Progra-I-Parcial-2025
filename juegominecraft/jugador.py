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


# ==================================
#   INTERFAZ GRÁFICA
# ==================================

def dibujar_boton(pantalla, texto, rect, fuente, color_normal, color_hover, mouse_pos):
    if rect.collidepoint(mouse_pos):
        color = color_hover
    else:
        color = color_normal

    pygame.draw.rect(pantalla, color, rect, border_radius=10)
    texto_render = fuente.render(texto, True, (255, 255, 255))
    texto_rect = texto_render.get_rect(center=rect.center)
    pantalla.blit(texto_render, texto_rect)


# def seleccionar_usuario():
#     pygame.init()
#     ancho = 800
#     alto = 600
#     pantalla = pygame.display.set_mode((ancho, alto))
#     pygame.display.set_caption("Seleccionar Usuario")
#     fuente = pygame.font.SysFont("Minecraft", 28)
#     reloj = pygame.time.Clock()

#     datos = cargar_usuarios()

#     mouse_pos = (0, 0)

#     fondo = pygame.image.load("botones y fondos/Dirt_background_BE1.png").convert()
#     fondo = pygame.transform.scale(fondo, (ancho, alto))

#     botones_slots = []
#     ancho_btn = 400
#     alto_btn = 60
#     x_pos = 200
#     y_inicio = 150
#     espacio = 80

#     # Se crean 3 botones (3 slots)
#     for i in range(3):
#         rect = pygame.Rect(x_pos, y_inicio + i * espacio, ancho_btn, alto_btn)
#         botones_slots.append(rect)

#     estado_input = False
#     input_text = ""
#     slot_seleccionado = -1

#     while True:
#         mouse_pos = pygame.mouse.get_pos()

#         for evento in pygame.event.get():
#             if evento.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()

#             # Si el usuario está escribiendo un nombre
#             if estado_input:
#                 if evento.type == pygame.KEYDOWN:

#                     if evento.key == pygame.K_RETURN:
#                         if input_text.strip() != "":
#                             datos["slots"][slot_seleccionado]["nombre"] = input_text.strip()
#                             guardar_usuarios(datos)

#                         # Se devuelve slot + nombre
#                         return slot_seleccionado, datos["slots"][slot_seleccionado]["nombre"]

#                     elif evento.key == pygame.K_BACKSPACE:
#                         largo = len(input_text)
#                         if largo > 0:
#                             input_text = input_text[:largo-1]

#                     else:
#                         if len(input_text) < 20:
#                             input_text = input_text + evento.unicode

#             else:
#                 # Todavía no está escribiendo, está eligiendo un slot
#                 if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
#                     # Recorremos los 3 botones con for + range
#                     for i in range(3):
#                         rect = botones_slots[i]

#                         if rect.collidepoint(mouse_pos):
#                             slot_seleccionado = i

#                             nombre_guardado = datos["slots"][i]["nombre"]

#                             if nombre_guardado == "":
#                                 estado_input = True
#                                 input_text = ""
#                             else:
#                                 # Se devuelve slot + nombre existente
#                                 return slot_seleccionado, nombre_guardado

#         pantalla.blit(fondo, (0, 0))

#         # Dibujar botones de selección
#         for i in range(3):
#             rect = botones_slots[i]
#             texto = datos["slots"][i]["nombre"]

#             if texto == "":
#                 texto = "(vacío) - click para crear"

#             dibujar_boton(
#                 pantalla,
#                 texto,
#                 rect,
#                 fuente,
#                 (50, 50, 50),
#                 (100, 100, 100),
#                 mouse_pos
#             )

#         # Cuadro para escribir nombre si corresponde
#         if estado_input:
#             input_rect = pygame.Rect(200, 450, 400, 50)
#             pygame.draw.rect(pantalla, (0, 0, 0), input_rect)
#             pygame.draw.rect(pantalla, (255, 255, 255), input_rect, 2)

#             texto_input = fuente.render(input_text, True, (255, 255, 255))
#             pantalla.blit(texto_input, (input_rect.x + 10, input_rect.y + 10))

#             indicacion = fuente.render("Ingrese nombre y presione ENTER", True, (255, 255, 255))
#             pantalla.blit(indicacion, (200, 400))

#         pygame.display.flip()
#         reloj.tick(60)


# # ================================
# #   PROGRAMA PRINCIPAL
# # ================================

# if __name__ == "__main__":
#     slot, nombre = seleccionar_usuario()
#     print("Slot:", slot)
#     print("Usuario seleccionado:", nombre)




def seleccionar_usuario():
    pygame.init()
    ancho = 800
    alto = 600
    pantalla = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Seleccionar Usuario")
    fuente = pygame.font.SysFont("Minecraft", 28)
    reloj = pygame.time.Clock()

    datos = cargar_usuarios()

    mouse_pos = (0, 0)

    fondo = pygame.image.load("botones y fondos/Dirt_background_BE1.png").convert()
    fondo = pygame.transform.scale(fondo, (ancho, alto))

    # ============= AGREGADO: TACHO PARA BORRAR =============
    tacho_img = pygame.image.load("botones y fondos/tacho.png").convert_alpha()
    tacho_img = pygame.transform.scale(tacho_img, (40, 40))
    # ========================================================

    botones_slots = []
    botones_eliminar = []  # <--- AGREGADO

    ancho_btn = 400
    alto_btn = 60
    x_pos = 200
    y_inicio = 150
    espacio = 80

    # Se crean 3 botones (3 slots)
    for i in range(3):
        rect = pygame.Rect(x_pos, y_inicio + i * espacio, ancho_btn, alto_btn)
        botones_slots.append(rect)

        # Rect del tacho
        tacho_rect = pygame.Rect(x_pos + ancho_btn + 10, y_inicio + i * espacio + 10, 40, 40)
        botones_eliminar.append(tacho_rect)

    estado_input = False
    input_text = ""
    slot_seleccionado = -1

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Si está escribiendo
            if estado_input:
                if evento.type == pygame.KEYDOWN:

                    if evento.key == pygame.K_RETURN:
                        if input_text.strip() != "":
                            datos["slots"][slot_seleccionado]["nombre"] = input_text.strip()
                            guardar_usuarios(datos)

                        return slot_seleccionado, datos["slots"][slot_seleccionado]["nombre"]

                    elif evento.key == pygame.K_BACKSPACE:
                        largo = len(input_text)
                        if largo > 0:
                            input_text = input_text[:largo-1]
                    else:
                        if len(input_text) < 20:
                            input_text = input_text + evento.unicode

            else:
                # No está escribiendo, está eligiendo usuario o tachito
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:

                    # --------- REVISAR SI APRETÓ EL TACHITO ------------
                    for i in range(3):
                        if botones_eliminar[i].collidepoint(mouse_pos):
                            datos["slots"][i]["nombre"] = ""
                            datos["slots"][i]["objetos"] = []
                            datos["slots"][i]["resultados"] = [[0]]
                            guardar_usuarios(datos)
                            break
                    # ---------------------------------------------------

                    # Revisar selección de slot
                    for i in range(3):
                        if botones_slots[i].collidepoint(mouse_pos):

                            slot_seleccionado = i
                            nombre_guardado = datos["slots"][i]["nombre"]

                            if nombre_guardado == "":
                                estado_input = True
                                input_text = ""
                            else:
                                return slot_seleccionado, nombre_guardado

        pantalla.blit(fondo, (0, 0))

        # Dibujar botones de selección + tachos
        for i in range(3):
            rect = botones_slots[i]
            texto = datos["slots"][i]["nombre"]

            if texto == "":
                texto = "(vacio) - click para crear"

            dibujar_boton(
                pantalla,
                texto,
                rect,
                fuente,
                (50, 50, 50),
                (100, 100, 100),
                mouse_pos
            )

            # DIBUJAR TACHO
            pantalla.blit(tacho_img, botones_eliminar[i])

        # Cuadro para escribir
        if estado_input:
            input_rect = pygame.Rect(200, 450, 400, 50)
            pygame.draw.rect(pantalla, (0, 0, 0), input_rect)
            pygame.draw.rect(pantalla, (255, 255, 255), input_rect, 2)

            texto_input = fuente.render(input_text, True, (255, 255, 255))
            pantalla.blit(texto_input, (input_rect.x + 10, input_rect.y + 10))

            indicacion = fuente.render("Ingrese nombre y presione ENTER", True, (255, 255, 255))
            pantalla.blit(indicacion, (200, 400))

        pygame.display.flip()
        reloj.tick(60)

# ================================
#   PROGRAMA PRINCIPAL
# ================================

if __name__ == "__main__":
    slot, nombre = seleccionar_usuario()
    print("Slot:", slot)
    print("Usuario seleccionado:", nombre)





