import sys
import pygame
import globals

from button import ImageButton

def fade(screen, clock = pygame.time.Clock()):
    running = True
    fade_alpha = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        fade_surface = pygame.Surface((globals.Const.WIDTH, globals.Const.HEIGHT))
        fade_surface.fill((0, 0, 0))
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0, 0))

        fade_alpha += 5
        if fade_alpha >= 105:
            fade_alpha = 255
            running = False

        pygame.display.flip()
        clock.tick(globals.Const.MAX_FPS)

def author(screen):
    pygame.display.set_caption("Authors")
    cursor = pygame.image.load("graphics/cursor.png")
    pygame.mouse.set_visible(False)
    
    font = pygame.font.SysFont(None, 42)
    main_background = pygame.image.load("graphics/stats_bg.jpg")
    text_lines = [
        "Программист и математик: ",
        "Ватаман Михаил",
        " ",
        "Креативный дизайнер:",
        "Морочковский Владислав",
        " ",
        "Технический дизайнер:",
        "Рустамов Рустам",
        " ",
        "Моральный вдохновитель:",
        "Морозова София",
        " ",
        "Реклама:",
        "ПФК ЦСКА",
        " ",
        "Отель?",
        "Триваго",
        " ",
        "7400 MMR в Dota2",
        "Мусько Денис"
    ]

    text_surfaces = [font.render(line, True, 'white') for line in text_lines]
    text_surfaces[12] = font.render(text_lines[12], True, 'blue')
    text_surfaces[13] = font.render(text_lines[13], True, 'red')

    text_height = sum(surface.get_height() for surface in text_surfaces)

    y_position = globals.Const.HEIGHT
    speed = 1.5
    
    menu_button = ImageButton(0, 590, 260, 74, "В меню", "graphics/green_button2.jpg", "graphics/green_button2_hover.jpg")
    
    running = True
    while running:
        x, y = pygame.mouse.get_pos()  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.USEREVENT and event.button == menu_button:
                fade(screen)
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                fade(screen)
                return
            
            menu_button.handle_event(event)

        screen.blit(main_background, (0, 0))
        
        current_y = y_position
        for text_surface in text_surfaces:
            screen.blit(text_surface, ((globals.Const.WIDTH - text_surface.get_width()) // 2 - 10, current_y))
            current_y += text_surface.get_height()
        
        y_position -= speed
        if y_position + text_height < 0:
            y_position = globals.Const.HEIGHT
        menu_button.check_hover((x, y))
        menu_button.draw(screen)

        screen.blit(cursor, (x, y))
        pygame.display.flip()
        pygame.time.delay(10)