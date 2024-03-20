import pygame
import sys
import game
import teams
import globals

from button import ImageButton
from authors import author
from authors import fade

class Buttons:
    def __init__(self, left, mid, right):
        self.left = left
        self.mid = mid
        self.right = right
                
    def but_attack(self):
        self.left.rename("Отдать пас")
        self.mid.rename("Трехочковый")
        self.right.rename("Дриблинг и бросок")
            
    def but_defence(self):
        self.left.rename("Аккуратная опека")
        self.mid.rename("Подпрыгнуть")
        self.right.rename("Попытка отобрать")

    def but_start_period(self, period):
        self.left.rename("Выйти")
        self.mid.rename("Сменить режим")
        self.right.rename(f"Начать {period} период")
            
    def but_start_match(self):
        self.left.rename("Выйти")
        self.mid.rename("Сменить режим")
        self.right.rename("Начать")

    def but_stats(self):
        self.left.rename("-->")
        self.mid.rename("Cтатистика")
        self.right.rename("<--")

    def __getitem__(self, key):
        if (key == 0):
            return self.left
        if (key == 1):
            return self.mid
        return self.right

class Interface:
    def __init__(self, for_color, screen, teams_logos, play_teams):
        self.left_number = 0
        self.right_number = 0
        self.period = 1
        self.time_period = 720
        self.attack_time = 24
        self.color = for_color
        self.screen = screen
        
        self.text = ""
        self.scroll = 0
        self.font = pygame.font.SysFont(None, 18)
        self.bold_font = pygame.font.SysFont(None, 20, True)
        self.text_window_rect = pygame.Rect(260, 60, 457, 500)
        
        self.speed = 0
        self.teams_logos = teams_logos
        self.play_teams = play_teams

        self.buttons = 0
        self.score_mode = True

    def set_buttons(self, buttons):
        self.buttons = buttons

    def change_score_mode(self):
        self.score_mode = not self.score_mode

    def change_mode(self, mode):
        self.button_mode = mode

    def scrolling(self, iter):
        self.scroll += iter

    def change_score(self, left_v, right_v):
        self.left_number = left_v
        self.right_number = right_v

    def change_period(self, score, new_value):
        if (new_value > 1):
            self.add_log(score, '\n')
        self.add_log(score, "{}-ый период".format(new_value), 720)
        self.period = new_value

    def change_time(self, new_value):
        self.time_period = new_value

    def change_attack_time(self, new_value = globals.Const.kBaseAttackTime):
        self.attack_time = new_value

    def add_log(self, score, new_text, mtime = -1):
        if (mtime > -1): 
            self.text = " {} - {} {:02d}:{:02d}  ".format(score[0], score[1], self.time_period // 60, self.time_period % 60) + new_text + '\n' + self.text
        else:
            self.text = new_text + '\n' + self.text
        self.scroll = -228 
        
    def interface_start_period(self, now_game, type, period):
        self.buttons.but_start_period(period)
        interface_of_game(self, now_game)

    def display_numbers(self, score_show = True):
        labels_font = pygame.font.SysFont(None, 24)

        if (score_show):
            score_font = pygame.font.SysFont(None, 180)
            left_text = score_font.render(str(self.left_number), True, get_color(self.color[0]))
            right_text = score_font.render(str(self.right_number), True, get_color(self.color[1]))
            left_text_rect = left_text.get_rect(center=(125, 350))
            self.screen.blit(left_text, left_text_rect)
            right_text_rect = right_text.get_rect(center=(globals.Const.WIDTH - 140, 350))
            self.screen.blit(right_text, right_text_rect)

        period_text = labels_font.render("Период: " + str(self.period), True, 'white')
        attack_time_text = labels_font.render("Время атаки: " + "{:02d}".format(self.attack_time), True, 'white')
        
        min_sec_time = "{:02d}:{:02d}".format(self.time_period // 60, self.time_period % 60)
        time_period_text = labels_font.render("Время периода: " + min_sec_time, True, 'white')
        
        self.screen.blit(period_text, (globals.Const.WIDTH // 2 - 220, 20))
        self.screen.blit(time_period_text, (globals.Const.WIDTH // 2 - 120, 20))
        self.screen.blit(attack_time_text, (globals.Const.WIDTH // 2 + 80, 20))

    def player_attack(self, now_game, team):
        self.buttons.but_attack()
        interface_of_game(self, now_game)
    
    def player_defence(self, now_game, team):
        self.buttons.but_defence()
        interface_of_game(self, now_game)

    def stats(self, now_game):
        self.buttons.but_stats()

def main_menu(screen, clock):
    pygame.display.set_caption("Menu window")
    main_background = pygame.image.load("graphics/bg.jpg")

    cursor = pygame.image.load("graphics/cursor.png")
    pygame.mouse.set_visible(False)

    simulation_button = ImageButton(globals.Const.WIDTH/2-(252/2) - 12, 50, 252, 74, "Симуляция", "graphics/green_button2.jpg", "graphics/green_button2_hover.jpg")
    player_button = ImageButton(globals.Const.WIDTH/2-(252/2) - 12, 150, 252, 74, "Против ИИ", "graphics/green_button2.jpg", "graphics/green_button2_hover.jpg")
    author_button = ImageButton(globals.Const.WIDTH/2-(252/2) - 12, globals.Const.HEIGHT - 220, 252, 74, "Авторы", "graphics/green_button2.jpg", "graphics/green_button2_hover.jpg")
    exit_button = ImageButton(globals.Const.WIDTH/2-(252/2) - 12, globals.Const.HEIGHT - 120, 252, 74, "Выйти", "graphics/green_button2.jpg", "graphics/green_button2_hover.jpg")

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
                fade(screen, clock)
                return 0

            if event.type == pygame.USEREVENT and event.button == player_button:
                fade(screen, clock)
                return 1
            
            if event.type == pygame.USEREVENT and event.button == author_button:
                fade(screen, clock)
                author(screen)

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

def get_color(index) -> str:
    index += 1
    if (index in [12, 14, 24, 20, 21]):
        return 'yellow'
    if (index in [2, 17]):
        return (10,80,40)
    if (index == 26):
        return 'violet'
    if (index in [3, 6, 8, 11, 13, 19, 27]):
        return 'black'
    if (index in [1, 5, 9, 16, 25, 28, 30]):
        return 'red'
    return 'blue'

def interface_of_choise(screen, teams_logos, index, x, y, bool = False, font_size=50):
        font = pygame.font.Font(None, font_size)
        
        team_logo_1 = teams_logos[index]["logo"]
        new_width = 150
        ratio = new_width / team_logo_1.get_width()
        new_height = int(team_logo_1.get_height() * ratio)
        current_team_logo_1 = pygame.transform.scale(team_logo_1, (new_width, new_height))
        logo_rect_1 = current_team_logo_1.get_rect(center=(x - 12, globals.Const.HEIGHT / 4 + globals.Const.HEIGHT / 2 * (bool == True)))
        screen.blit(current_team_logo_1, logo_rect_1)

        current_team_name_1 = teams_logos[index]["name"]
        team_name_text_1 = font.render(current_team_name_1, True, get_color(index))
        team_name_rect_1 = team_name_text_1.get_rect(center=(x - 12, y))
        screen.blit(team_name_text_1, team_name_rect_1)

        outline_text = font.render(current_team_name_1, True, 'white')
        outline_rect = outline_text.get_rect()
        outline_rect.center = (x - 10, y + 2)
        screen.blit(outline_text, outline_rect)

def get_logos(indexes = -1): 
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
        teams_logos.append({"name": team, "logo": pygame.image.load(f"logos/{i+1}.png"), "index": i})
    
    if (indexes == -1):
        return teams, teams_logos
    return teams[indexes], teams_logos[indexes]

def get_teams(screen, clock) -> list:

    pygame.display.set_caption("Choose teams")
    main_background = pygame.image.load("graphics/bg.jpg")
    clock = pygame.time.Clock()

    cursor = pygame.image.load("graphics/cursor.png")
    pygame.mouse.set_visible(False)

    current_team_index = [0, 0]

    teams, teams_logos = get_logos()

    menu_button = ImageButton(7, globals.Const.HEIGHT / 2, 252, 74, "В меню", "graphics/green_button2.jpg", "graphics/green_button2_hover.jpg")
    confirm_button = ImageButton(globals.Const.WIDTH - 272, globals.Const.HEIGHT / 2, 262, 74, "Подтвердить", "graphics/green_button2.jpg", "graphics/green_button2_hover.jpg")
    back_button_1 = ImageButton(300, globals.Const.HEIGHT / 4, 40, 40, "<", "graphics/green_button2.jpg", "graphics/green_button2_hover.jpg")
    next_button_1 = ImageButton(globals.Const.WIDTH - 340, globals.Const.HEIGHT / 4, 40, 40, ">", "graphics/green_button2.jpg", "graphics/green_button2_hover.jpg")
    back_button_2 = ImageButton(300, globals.Const.HEIGHT * 3 / 4, 40, 40, "<", "graphics/green_button2.jpg", "graphics/green_button2_hover.jpg")
    next_button_2 = ImageButton(globals.Const.WIDTH - 340, globals.Const.HEIGHT * 3 / 4, 40, 40, ">", "graphics/green_button2.jpg", "graphics/green_button2_hover.jpg")

    while True:
        screen.blit(main_background, main_background.get_rect())

        interface_of_choise(screen, teams_logos, current_team_index[0], globals.Const.WIDTH // 2, 50)
        interface_of_choise(screen, teams_logos, current_team_index[1], globals.Const.WIDTH // 2, 610, True)

        # Отрисовка кнопки "В меню"
        menu_button.draw(screen)
        confirm_button.draw(screen)
        back_button_1.draw(screen)
        next_button_1.draw(screen)
        back_button_2.draw(screen)
        next_button_2.draw(screen)

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
                    fade(screen, clock)
                    return current_team_index
                elif event.key == pygame.K_ESCAPE:
                    fade(screen, clock)
                    return []
            elif event.type == pygame.USEREVENT and event.button == confirm_button:
                fade(screen, clock)
                return current_team_index
            elif event.type == pygame.USEREVENT and event.button == menu_button:
                fade(screen, clock)
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

        x, y = pygame.mouse.get_pos()
        screen.blit(cursor, (x-2, y-2))

        pygame.display.flip()

def statistics(screen, play_indexes, team, teams_logos, names_of_stats, score):
    pygame.display.set_caption("Statistics")
    main_background = pygame.image.load("graphics/stats_bg.jpg")
    clock = pygame.time.Clock()
    
    values1 = [s[0] for s in team[0].stats]
    values2 = [s[0] for s in team[1].stats]
    for i in range(3):
        values1.insert(i*2 + 1, team[0].stats[i][1])
        values2.insert(i*2 + 1, team[1].stats[i][1])

    cursor = pygame.image.load("graphics/cursor.png")
    pygame.mouse.set_visible(False)

    font = pygame.font.SysFont(None, 22)

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
                pygame.quit()
                sys.exit()
            elif event.type == pygame.USEREVENT and event.button == exit_button:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.USEREVENT and event.button == menu_button:
                pygame.quit()
                return
            
            for btn in [menu_button, exit_button]:
                btn.handle_event(event)
        
        for btn in [menu_button, exit_button]:
                btn.check_hover(pygame.mouse.get_pos())
                btn.draw(screen)

        for i in range(len(values1)):
            pygame.draw.rect(screen, get_color(play_indexes[0]), (globals.Const.start_x, 160 + 43 * i, 370 * values1[i]/(values1[i]+values2[i]), 10))
            pygame.draw.rect(screen, get_color(play_indexes[1]), (globals.Const.start_x + 370 * values1[i]/(values1[i]+values2[i]), 160 + 43 * i, 370 * values2[i]/(values1[i]+values2[i]), 10))

            value1_text = font.render(str(values1[i]), True, 'white')
            value2_text = font.render(str(values2[i]), True, 'white')
            value3_text = font.render(names_of_stats[i], True, 'white')
            screen.blit(value3_text, (globals.Const.start_x + 165 - 2 * len(names_of_stats[i]), 142 + 43 * i))
            screen.blit(value1_text, (globals.Const.start_x - 25, 160 + 43 * i))
            screen.blit(value2_text, (globals.Const.start_x + 385, 160 + 43 * i))

        score_team1 = pygame.font.SysFont(None, 90).render(str(score[0]), True, get_color(play_indexes[0]))
        screen.blit(score_team1, (300, 50))
        score_team2 = pygame.font.SysFont(None, 90).render(str(score[1]), True, get_color(play_indexes[1]))
        screen.blit(score_team2, (570, 50))
        
        outline_text = pygame.font.SysFont(None, 90).render(str(score[0]), True, 'white')
        screen.blit(outline_text, (303, 52))
        outline_text2 = pygame.font.SysFont(None, 90).render(str(score[1]), True, 'white')
        screen.blit(outline_text2, (573, 52))
       
        interface_of_choise(screen, teams_logos, play_indexes[0], 135, 50, font_size=35)
        interface_of_choise(screen, teams_logos, play_indexes[1], globals.Const.WIDTH - 125, 50, font_size=35)

        x, y = pygame.mouse.get_pos()  
        screen.blit(cursor, (x, y))

        pygame.display.flip()
        clock.tick(globals.Const.MAX_FPS)

    pygame.quit()

def scrollable_text(surface, font, bold, color, rect, text, scroll_pos):
    text_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    text_surface.fill((255, 255, 255, 0))
    
    lines = text.split('\n')
    center_y = rect.height / 2
    max_distance = center_y

    y = 0

    for line in lines:
        if line and line[0] == ' ':
            text_line = bold.render(line, True, color)
        else:
            text_line = font.render(line, True, color)
        distance_to_center = abs(y - scroll_pos - center_y)
        alpha = max(0, min(255, int(255 - (255 * distance_to_center / max_distance))))
        text_line.set_alpha(alpha)
        text_surface.blit(text_line, (10, y - scroll_pos))
        y += text_line.get_height() + 3

    surface.blit(text_surface, (rect.x, rect.y))

def left_clicked(interface, button, now_game):
    if (button.get_text() == "Выйти"):
        pygame.quit()
    elif (button.get_text() == "Отдать пас"):
        game.Player_attack.try_pass(now_game, now_game.my_team)
    elif (button.get_text() == "Аккуратная опека"):
        game.Player_defence.try_block_pass(now_game, now_game.my_team)
    elif (button.get_text() == "-->"):
        return False
    return True
    
def mid_clicked(interface, button, now_game):
    if (button.get_text() == "Сменить режим"):
        interface.change_score_mode()
        return False
    elif (button.get_text() == "Трехочковый"):
        game.Player_attack.throwing(now_game, now_game.my_team, 3)
    elif (button.get_text() == "Подпрыгнуть"):
        game.Player_defence.try_block_throw(now_game, now_game.my_team)
    elif (button.get_text() == "Статистика"):
        pass
    return True

def right_clicked(interface, button, now_game):    
    if (button.get_text() == "Начать"): 
        game.start_game(now_game.type, now_game.int_to_team[0], now_game.int_to_team[1], interface, now_game)
        return False
    elif (button.get_text()[:2] == "На"):
        game.start_period(now_game, now_game.type)
    elif (button.get_text() == "Дриблинг и бросок"):
        game.Player_attack.try_dribble(now_game, now_game.my_team)
    elif (button.get_text() == "Попытка отобрать"):
        game.Player_defence.try_steal(now_game, now_game.my_team)
    elif (button.get_text() == "<--"):
        return False
    return True

def interface_of_game(values, now_game):
    pygame.display.set_caption("Game")
    main_background = pygame.image.load("graphics/game_bg.jpg")

    cursor = pygame.image.load("graphics/cursor.png")
    pygame.mouse.set_visible(False)

    running = True
    while running:
        values.screen.fill((0, 0, 0))
        values.screen.blit(main_background, (0, 0))
        
        values.buttons[0].draw(values.screen)
        values.buttons[1].draw(values.screen)
        values.buttons[2].draw(values.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.USEREVENT and event.button == values.buttons[0]:
                need_return = left_clicked(values, values.buttons[0], now_game)
                if (need_return):
                    return
            elif event.type == pygame.USEREVENT and event.button == values.buttons[1]:
                need_return = mid_clicked(values, values.buttons[1], now_game)
                if (need_return):
                    return
            elif event.type == pygame.USEREVENT and event.button == values.buttons[2]:
                need_return = right_clicked(values, values.buttons[2], now_game)
                if (need_return):
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    values.scrolling(10)
                elif event.button == 5:
                    values.scrolling(-10)

            for btn in [values.buttons[0], values.buttons[1], values.buttons[2]]:
                btn.handle_event(event)

        for btn in [values.buttons[0], values.buttons[1], values.buttons[2]]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(values.screen)
        
        x, y = pygame.mouse.get_pos()  
        values.screen.blit(cursor, (x, y))
        
        scrollable_text(values.screen, values.font, values.bold_font, (255, 255, 255), values.text_window_rect, values.text, values.scroll)
    
        interface_of_choise(values.screen, values.teams_logos, values.play_teams[0], 135, 50, font_size=30)
        interface_of_choise(values.screen, values.teams_logos, values.play_teams[1], globals.Const.WIDTH - 125, 50)

        values.display_numbers(values.score_mode)
        
        pygame.display.flip()
    pygame.quit()

def start(level_of_teams):

    left = ImageButton(0, 590, 260, 74, "Выйти", "graphics/green_button2.jpg", "graphics/green_button2_hover.jpg")
    mid = ImageButton(716 / 2, 590, 260, 74, "Сменить режим", "graphics/green_button2.jpg", "graphics/green_button2_hover.jpg")
    right = ImageButton(716, 590, 996 - 716, 74, "Начать", "graphics/green_button2.jpg", "graphics/green_button2_hover.jpg")
    
    while True:
        pygame.init()
        screen = pygame.display.set_mode((globals.Const.WIDTH, globals.Const.HEIGHT))
        clock = pygame.time.Clock()
        play_teams = []
        while len(play_teams) < 2:
            type = main_menu(screen, clock)
            play_teams = get_teams(screen, clock)

        first = teams.Teams(level_of_teams, play_teams[0] + 1)
        second = teams.Teams(level_of_teams, play_teams[1] + 1)
        _, teams_logos = get_logos()
        
        values = Interface(play_teams, screen, teams_logos, play_teams)
        now_game = game.Game(first, second, values, type)
        
        values.set_buttons(Buttons(left, mid, right))

        interface_of_game(values, now_game)
        score = now_game.score
        if (now_game.period > 3):
            statistics(screen, play_teams, [first, second], teams_logos, globals.Const.labels, score)