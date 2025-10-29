import pygame
import sys

def dibujar_boton(pantalla, texto, rect, fuente, color_normal, color_hover, mouse_pos):
    color = color_hover if rect.collidepoint(mouse_pos) else color_normal
    pygame.draw.rect(pantalla, color, rect, border_radius=10)
    texto_render = fuente.render(texto, True, (255, 255, 255))
    texto_rect = texto_render.get_rect(center=rect.center)
    pantalla.blit(texto_render, texto_rect)

def seleccionar_usuario(slots):
    pygame.init()
    pantalla = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Seleccionar Usuario")
    fuente = pygame.font.SysFont("Minecraft", 28)

    reloj = pygame.time.Clock()
    mouse_pos = (0, 0)

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
                            slots[slot_seleccionado] = input_text.strip()
                        input_text = ""
                        estado_input = False
                        return slots[slot_seleccionado]
                    elif evento.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        if len(input_text) < 20:
                            input_text += evento.unicode

            else:
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    for i, rect in enumerate(botones_slots):
                        if rect.collidepoint(mouse_pos):
                            slot_seleccionado = i
                            if slots[i] == "":
                                estado_input = True
                                input_text = ""
                            else:
                                return slots[i]

        pantalla.fill((0, 0, 0))

        for i, rect in enumerate(botones_slots):
            texto = slots[i] if slots[i] != "" else "(vacio) - click para crear"
            dibujar_boton(pantalla, texto, rect, fuente, (50, 50, 50), (100, 100, 100), mouse_pos)

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