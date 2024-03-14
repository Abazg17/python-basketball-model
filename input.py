import pygame
import sys
from button import ImageButton
import game_interface
import teams

pygame.init()

WIDTH, HEIGHT = 996, 664
MAX_FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu test")
#main_background = pygame.image.load("graphics/background1.jpg")
main_background = pygame.image.load("/home/abazg17/Рабочий стол/bg.jpg")
clock = pygame.time.Clock()

cursor = pygame.image.load("graphics/cursor.png")
pygame.mouse.set_visible(False)

def main_menu():
    simulation_button = ImageButton(WIDTH/2-(252/2) - 12, 50, 252, 74, "Симуляция", "graphics/green_button2.jpg", "graphics/green_button2_hover.jpg")
    player_button = ImageButton(WIDTH/2-(252/2) - 12, 150, 252, 74, "Против ИИ", "graphics/green_button2.jpg", "graphics/green_button2_hover.jpg")
    author_button = ImageButton(WIDTH/2-(252/2) - 12, HEIGHT - 220, 252, 74, "Авторы", "graphics/green_button2.jpg", "graphics/green_button2_hover.jpg")
    exit_button = ImageButton(WIDTH/2-(252/2) - 12, HEIGHT - 120, 252, 74, "Выйти", "graphics/green_button2.jpg", "graphics/green_button2_hover.jpg")

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(main_background, (0, 0))

        font = pygame.font.Font(None, 72)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == simulation_button:
                print("Кнопка 'Старт' была нажата!")
                fade()
                return 0

            if event.type == pygame.USEREVENT and event.button == player_button:
                print("Кнопка 'Настройки' была нажата!")
                fade()
                return 1

            if event.type == pygame.USEREVENT and event.button == exit_button:
                running = False
                pygame.quit()
                sys.exit()

            for btn in [simulation_button, player_button, exit_button, author_button]:
                btn.handle_event(event)

        for btn in [simulation_button, player_button, exit_button, author_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        x, y = pygame.mouse.get_pos()
        screen.blit(cursor, (x-2, y-2))

        pygame.display.flip()

def fade():
    running = True
    fade_alpha = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        fade_surface = pygame.Surface((WIDTH, HEIGHT))
        fade_surface.fill((0, 0, 0))
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0, 0))

        fade_alpha += 5
        if fade_alpha >= 105:
            fade_alpha = 255
            running = False

        pygame.display.flip()
        clock.tick(MAX_FPS)

def get_color(index) -> str:
    index += 1
    if (index in [12, 14, 24]):
        return 'yellow'
    if (index in [2, 17]):
        return 'green'
    if (index == 26):
        return 'violet'
    if (index in [3, 6, 8, 11, 13, 19, 27]):
        return 'black'
    if (index in [20, 21]):
        return 'orange'
    if (index in [1, 5, 9, 16, 25, 28, 30]):
        return 'red'
    return 'blue'

def interface_of_choise(teams_logos, index, x, y, bool = False):
        font = pygame.font.Font(None, 50)

        team_logo_1 = teams_logos[index]["logo"]
        new_width = 150
        ratio = new_width / team_logo_1.get_width()
        new_height = int(team_logo_1.get_height() * ratio)
        current_team_logo_1 = pygame.transform.scale(team_logo_1, (new_width, new_height))
        logo_rect_1 = current_team_logo_1.get_rect(center=(x - 12, HEIGHT / 4 + HEIGHT / 2 * (bool == True)))
        screen.blit(current_team_logo_1, logo_rect_1)

        current_team_name_1 = teams_logos[index]["name"]
        team_name_text_1 = font.render(current_team_name_1, True, get_color(index))
        team_name_rect_1 = team_name_text_1.get_rect(center=(x - 12, y))
        screen.blit(team_name_text_1, team_name_rect_1)

        outline_text = font.render(current_team_name_1, True, 'white')
        outline_rect = outline_text.get_rect()
        outline_rect.center = (x - 10, y + 2)
        screen.blit(outline_text, outline_rect)

def get_logos(): 
    # Индекс текущей команды
    teams = ["Atlanta Hawks", "Boston Celtics", "Brooklyn Nets", "Charlotte Hornets",
             "Chicago Bulls", "Cleveland Cavaliers", "Dallas Mavericks", "Denver Nuggets",
             "Detroit Pistons", "Golden State Warriors", "Houston Rockets", "Indiana Pacers",
             "LA Clippers", "Los Angeles Lakers", "Memphis Grizzlies", "Miami Heat",
             "Milwaukee Bucks", "Minnesota Timberwolves", "New Orleans Pelicans",
             "New York Knicks", "Oklahoma City Thunder", "Orlando Magic", "Philadelphia 76ers",
             "Phoenix Suns", "Portland Trail Blazers", "Sacramento Kings", "San Antonio Spurs",
             "Toronto Raptors", "Utah Jazz", "Washington Wizards"]

    teams_logos = []
    for i, team in enumerate(teams):
        teams_logos.append({"name": team, "logo": pygame.image.load(f"logos/{i+1}.png")})
    
    return teams, teams_logos

def get_teams() -> list:
    current_team_index = [0, 0]

    teams, teams_logos = get_logos()

    menu_button = ImageButton(7, HEIGHT / 2, 252, 74, "В меню", "graphics/green_button2.jpg", "graphics/green_button2_hover.jpg")
    confirm_button = ImageButton(WIDTH - 272, HEIGHT / 2, 262, 74, "Подтвердить", "graphics/green_button2.jpg", "graphics/green_button2_hover.jpg")
    back_button_1 = ImageButton(300, HEIGHT / 4, 40, 40, "<", "graphics/green_button2.jpg", "graphics/green_button2_hover.jpg")
    next_button_1 = ImageButton(WIDTH - 340, HEIGHT / 4, 40, 40, ">", "graphics/green_button2.jpg", "graphics/green_button2_hover.jpg")
    back_button_2 = ImageButton(300, HEIGHT * 3 / 4, 40, 40, "<", "graphics/green_button2.jpg", "graphics/green_button2_hover.jpg")
    next_button_2 = ImageButton(WIDTH - 340, HEIGHT * 3 / 4, 40, 40, ">", "graphics/green_button2.jpg", "graphics/green_button2_hover.jpg")

    while True:
        screen.blit(main_background, main_background.get_rect())

        interface_of_choise(teams_logos, current_team_index[0], WIDTH // 2, 50)
        interface_of_choise(teams_logos, current_team_index[1], WIDTH // 2, 610, True)

        # Отрисовка кнопки "В меню"
        menu_button.draw(screen)
        confirm_button.draw(screen)
        back_button_1.draw(screen)
        next_button_1.draw(screen)
        back_button_2.draw(screen)
        next_button_2.draw(screen)

        x, y = pygame.mouse.get_pos()
        screen.blit(cursor, (x-2, y-2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_team_index[0] = (current_team_index[0] - 1) % len(teams)
                elif event.key == pygame.K_RIGHT:
                    current_team_index[0] = (current_team_index[0] + 1) % len(teams)
                elif event.key == pygame.K_UP:
                    current_team_index[1] = (current_team_index[1] + 1) % len(teams)
                elif event.key == pygame.K_DOWN:
                    current_team_index[1] = (current_team_index[1] - 1) % len(teams)
                elif event.key == pygame.K_RETURN:
                    return current_team_index
                elif event.key == pygame.K_ESCAPE:
                    fade()
                    return []
            elif event.type == pygame.USEREVENT and event.button == confirm_button:
                return current_team_index
            elif event.type == pygame.USEREVENT and event.button == menu_button:
                fade()
                return []
            elif event.type == pygame.USEREVENT and event.button == back_button_1:
                current_team_index[0] = (current_team_index[0] - 1) % len(teams)
            elif event.type == pygame.USEREVENT and event.button == next_button_1:
                current_team_index[0] = (current_team_index[0] + 1) % len(teams)
            elif event.type == pygame.USEREVENT and event.button == back_button_2:
                current_team_index[1] = (current_team_index[1] - 1) % len(teams)
            elif event.type == pygame.USEREVENT and event.button == next_button_2:
                current_team_index[1] = (current_team_index[1] + 1) % len(teams)
            for btn in [menu_button, confirm_button, back_button_1, next_button_1, next_button_2, back_button_2]:
                btn.handle_event(event)

        for btn in [menu_button, confirm_button, back_button_1, next_button_1, next_button_2, back_button_2]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        pygame.time.Clock().tick(120)

        pygame.display.flip()

def interface_of_game():
    pass

def statistics(team1, team2):
    pygame.init()

    WIDTH, HEIGHT = 996, 664
    MAX_FPS = 60

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Menu test")
    main_background = pygame.image.load("/home/abazg17/Рабочий стол/bg.jpg")
    clock = pygame.time.Clock()

    cursor = pygame.image.load("graphics/cursor.png")
    pygame.mouse.set_visible(False)

    running = True

    values1 = [s[0] for s in team1.stats]
    values2 = [s[0] for s in team2.stats]
    print(values1, values2)
    gap = 20
    oval_width = 40
    max_height = HEIGHT - 100

    total_ovals = max(len(values1), len(values2))

    start_x = (WIDTH - (oval_width + gap) * total_ovals) // 2
    start_y = HEIGHT - max_height

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Отрисовка фона
        screen.blit(main_background, (0, 0))

        # Отрисовка столбцов для values1
        for i, value in enumerate(values1):
            oval_height = value * max_height / max(values1)
            pygame.draw.ellipse(screen, get_color(1), (start_x + (oval_width + gap) * i, start_y, oval_width, oval_height))

        # Отрисовка столбцов для values2
        for i, value in enumerate(values2):
            oval_height = value * max_height / max(values2)
            pygame.draw.ellipse(screen, get_color(2), (start_x + (oval_width + gap) * i, start_y, oval_width, oval_height))

        # Отрисовка курсора
        x, y = pygame.mouse.get_pos()
        screen.blit(cursor, (x-2, y-2))

        # Обновление экрана
        pygame.display.flip()

        # Ограничение FPS
        clock.tick(MAX_FPS)

def start(level_of_teams):
    play_teams = []
    while len(play_teams) < 2:
        type = main_menu()
        play_teams = get_teams()

    first = teams.Teams(level_of_teams, play_teams[0] + 1)
    second = teams.Teams(level_of_teams, play_teams[1] + 1)

    #interface_of_game(first, second, type)

    pygame.quit()
    score = game_interface.start(first, second, type)
    statistics(first, second)