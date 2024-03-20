import sys
import pygame

class ImageButton:
    def __init__(self, x, y, width, height, text, image_path, hover_image_path=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.hover_image = self.image
        if hover_image_path:
            self.hover_image = pygame.image.load(hover_image_path)
            self.hover_image = pygame.transform.scale(self.hover_image, (width, height)) 
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_hovered = False

    def draw(self, screen):
        current_image = self.hover_image if self.is_hovered else self.image
        screen.blit(current_image, self.rect.topleft)

        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))

def statistics(team, logos, names_of_stats, score):
    pygame.init()

    WIDTH, HEIGHT = 996, 664
    MAX_FPS = 60
    start_x = 300

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Menu test")
    main_background = pygame.image.load("graphics/stats_bg.jpg")
    clock = pygame.time.Clock()

    cursor = pygame.image.load("graphics/cursor.png")
    pygame.mouse.set_visible(False)

    font = pygame.font.SysFont(None, 22)

    team1 = "Portland Trail Blazers"
    team2 = "Portland Trail Blazers"
    logo1 = pygame.image.load("logos/1.png")
    logo2 = pygame.image.load("logos/2.png")
    list1 = [1,2,3,4,5, 6, 7, 8, 9, 10, 11, 12]
    list2 = [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    score1 = 100
    score2 = 120
    name_stats = ["Throws"] * 12

    menu_button = ImageButton(0, 590, 260, 74, "В меню", "graphics/green_button2.jpg", "graphics/green_button2_hover.jpg")
    exit_button = ImageButton(716, 590, 996 - 716, 74, "Закрыть игру", "graphics/green_button2.jpg", "graphics/green_button2_hover.jpg")

    running = True
        
    while running:
        screen.fill((0, 0, 0))
        
        screen.blit(main_background, (0, 0))

        menu_button.draw(screen)
        exit_button.draw(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.USEREVENT and event.button == exit_button:
                pygame.quit()
                sys.exit()
            
            for btn in [menu_button, exit_button]:
                btn.handle_event(event)
        
        for btn in [menu_button, exit_button]:
                btn.check_hover(pygame.mouse.get_pos())
                btn.draw(screen)

        x, y = pygame.mouse.get_pos()  

        for i in range(len(list1)):
            pygame.draw.rect(screen, 'blue', (start_x, 160 + 43 * i, 370 * list1[i]/(list1[i]+list2[i]), 10))
            pygame.draw.rect(screen, 'red', (start_x + 370 * list1[i]/(list1[i]+list2[i]), 160 + 43 * i, 370 * list2[i]/(list1[i]+list2[i]), 10))

            value1_text = font.render(str(list1[i]), True, 'white')
            value2_text = font.render(str(list2[i]), True, 'white')
            color = 'white' if list1[i] < list2[i] else 'white'
            value3_text = font.render(name_stats[i] + str(i), True, color)
            screen.blit(value3_text, (start_x + 165, 142 + 43 * i))
            screen.blit(value1_text, (start_x - 25, 160 + 43 * i))
            screen.blit(value2_text, (start_x + 385, 160 + 43 * i))
        
        name_team1 = pygame.font.SysFont(None, 35).render(team1, True, 'blue')
        team_name_rect_1 = name_team1.get_rect(center=(start_x + 100, 20))
        screen.blit(name_team1, team_name_rect_1)
        name_team2 = pygame.font.SysFont(None, 35).render(team2, True, 'red')
        team_name_rect_1 = name_team2.get_rect(center=(start_x + 565 - 13 * len(team2), 50))
        screen.blit(name_team2, (team_name_rect_1))

        outline_text = pygame.font.SysFont(None, 35).render(team1, True, 'white')
        outline_rect = outline_text.get_rect()
        outline_rect.center = (start_x + 102, 22)
        screen.blit(outline_text, outline_rect)
        outline_text2 = pygame.font.SysFont(None, 35).render(team2, True, 'white')
        outline_rect2 = outline_text2.get_rect()
        outline_rect2.center = (start_x + 567 - 13 * len(team2), 52)
        screen.blit(outline_text2, outline_rect2)

        score_team1 = pygame.font.SysFont(None, 80).render(str(score1), True, 'blue')
        screen.blit(score_team1, (300, 50))
        score_team2 = pygame.font.SysFont(None, 80).render(str(score2), True, 'red')
        screen.blit(score_team2, (570, 80))
        
        outline_text = pygame.font.SysFont(None, 80).render(str(score1), True, 'white')
        screen.blit(outline_text, (303, 52))
        outline_text2 = pygame.font.SysFont(None, 80).render(str(score2), True, 'white')
        screen.blit(outline_text2, (573, 82))
        
        new_width = 200
        ratio = new_width / logo1.get_width()
        new_height = int(logo1.get_height() * ratio)
        logo_1 = pygame.transform.scale(logo1, (new_width, new_height))
        logo_rect_1 = logo_1.get_rect(center=(130, 90))
        screen.blit(logo_1, logo_rect_1)

        new_width = 200
        ratio = new_width / logo2.get_width()
        new_height = int(logo2.get_height() * ratio)
        logo_2 = pygame.transform.scale(logo2, (new_width, new_height))
        logo_rect_2 = logo_2.get_rect(center=(876, 90))
        screen.blit(logo_2, logo_rect_2)

        screen.blit(cursor, (x, y))

        pygame.display.flip()
        clock.tick(MAX_FPS)

    pygame.quit()