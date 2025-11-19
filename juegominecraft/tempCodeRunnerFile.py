

    # Imagen de botón base y hover
    boton_base = pygame.image.load("botones y fondos/boton chico.png").convert_alpha()
    boton_hover = boton_base.copy()
    boton_hover.set_alpha(255)
    boton_base.set_alpha(180)

    # Definir rectángulos
    rect_fabricar = pygame.Rect(ancho // 2 - 240, 340, 120, 60)