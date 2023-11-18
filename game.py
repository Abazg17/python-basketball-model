from globals import Const
# для случайных чисел без распределения
import random
import numpy as np
# для случайного распределения
from scipy.stats import bernoulli    

# исключение для начала новой атаки и сброса всей предыдущей
class NewAttackException(Exception):
    def __init__(self, now_game, condition = True):
        if (condition):
            # устанавливает время для новой атаки, обновляет число пасов, меняет владение, меняет флаг исключения
            now_game.attack_time = Const.kBaseAttackTime
            now_game.window.change_attack_time()
            now_game.passes_now = 1
            now_game.possession = not now_game.possession
            now_game.exception = True

# вызывает функции из файла, отвечающего за само окно, меняющее время
# также сбрасывает атаку и передает владение, если время закончилось
def big_time_change(game, decr):
    game.attack_time -= decr
    game.time -= decr
    # обновляем время в окне
    game.window.change_attack_time(max(game.attack_time,0))
    game.window.change_time(max(game.time,0))
    # если время "уже истекало" передаем владение
    if (game.time_exp == True):
        game.time_exp = False
        game.window.add_log(game.score, "Время истекло. Переход владения")  
        raise NewAttackException(game, True)
    # если время утекло только что даем шанс на еще одно действие
    if (game.time < 0):
        game.time = 1
        game.window.change_time(1)
        game.time_exp = True

    if (game.attack_time < 0):
        game.attack_time = 1
        game.window.change_attack_time(1)
        game.time_exp = True

# функция выбирает действие ИИ в атаке в зависимости от времени
def CPU_random_att(time):
     # если мало времени, будет бросок
    if (time < 3):
        return ("throw3")
    # если много времени, будут пасы
    if (time > 13):
        # распределение Бернулли с вероятностью успеха p
        pass_r = bernoulli.rvs(size = 1, p = 0.83)[0]
        throw_r = bernoulli.rvs(size = 1, p = 0.05)[0]
        if (pass_r == 1):
            return ("pass")
        if (throw_r == 1):
            return ("throw3")
        return ("dribble")
    pass_r = bernoulli.rvs(size = 1, p = 0.65)[0]
    dribble_r = bernoulli.rvs(size = 1, p = 0.18)[0]
    if (pass_r == 1):
        return ("pass")
    if (dribble_r == 1):
        return ("dribble")
    return ("throw3")    

# функция выбирает действие ИИ в обороне в зависимости от времени
def CPU_random_def(time):
    # если мало времени, будет бросок
    if (time < 3):
        return ("def_throw")
    # если много времени, будут пасы
    if (time > 13):
        pass_r = bernoulli.rvs(size = 1, p = 0.8)[0]
        throw_r = bernoulli.rvs(size = 1, p = 0.07)[0]
        if (pass_r == 1):
            return ("def_pass")
        if (throw_r == 1):
            return ("def_throw")
        return ("def_dribble")
    pass_r = bernoulli.rvs(size = 1, p = 0.6)[0]
    dribble_r = bernoulli.rvs(size = 1, p = 0.2)[0]
    if (pass_r == 1):
        return ("def_pass")
    if (dribble_r == 1):
        return ("def_dribble")
    return ("def_throw")    

class Game:
    # конструктор объекта игра, где хранится вся общая информация (счет, время, команды)
    def __init__(self, team1, team2, windows, type):
        self.attack_time = Const.kBaseAttackTime
        self.time = Const.kBasePeriodTime
        self.period = 1
        self.score = [0,0]
        self.fouls = [0,0]
        self.comands_name = [team1.name,team2.name]
        self.possession = random.randint(0,1)
        self.window = windows
        self.team_to_int = {team1 : 0, team2 : 1}
        self.int_to_team = {0 : team1, 1 : team2}
        self.team_one = team1
        self.passes_now = 1
        self.type = type
        self.time_exp = False
    
    # обновляет период и, соответственно, время и фолы, 
    def new_period(self):
        self.window.change_period(self.score, self.period)
        self.period += 1
        self.time = Const.kBasePeriodTime
        self.attack_time = Const.kBaseAttackTime
        self.fouls = [0,0]
        if self.period % 2 == 1:
            self.possession = random.randint(0,1)
        self.window.change_time(self.time)
        self.window.change_attack_time(self.attack_time)

    # возвращает объект соперника по объекту нашей команды
    def against_team(self, team):
        a = [key for key,value in self.team_to_int.items() if value != self.team_to_int[team]][0]
        return (a)

    # функция для типа игры "случайная". Выбирает действие команды в обороне. Затем передается это 
    # в функцию, которая выбирает действие для атаки (ниже)
    def CPU_game(self, team_d):
        defence = CPU_random_def(self.time)
        if (defence == "def_pass"):
            Player_defence.try_block_pass(self, team_d)
        elif (defence == "def_dribble"):
            Player_defence.try_steal(self, team_d)
        elif (defence == "def_throw"):
            Player_defence.try_block_throw(self, team_d)

    # отвечает за атаку одной команды (тратится время и в зависимости от типа вызывается ли функция, 
    # отвечающая за выбор ИИ, или функция, отображающая кнопки с действиями для пользователя)
    def player_attack(self, team):
        dec_time = random.randint(0,1)
        big_time_change (self, dec_time)
        if (self.type == 1):
            if (self.attack_time > 0):
                self.window.player_attack(self, team)
        else:
            self.CPU_game((self.against_team(team)))

    # по аналогии с прошлой функцией отвечает за защитные действия: либо вызывает функцию с кнопками для 
    # пользователя, либо генерирует оборонительное действие команды
    def player_defense(self, team):
        dec_time = random.randint(0,1)
        big_time_change (self, dec_time)
        if (self.type == 1):
            if (self.attack_time > 0):
                self.window.player_defence(self, team)
        else:
            self.CPU_game(team)

    # запускает атаку в зависимости от владения
    def play (self, type, possession):
        if (possession == 0) :
            self.player_attack(self.team_one)
        else:
            self.player_defense(self.team_one)

    # теперь "игровые функции"

    # подбор (после бросков)
    def rebound(self, team):
        # берем статистику
        att_reb = team.off_rebound
        def_reb = self.int_to_team[not self.possession].def_rebound
        # генерируем подбор
        res = (bernoulli.rvs(size=1, p = att_reb/(att_reb+def_reb)))[0]
        # вычитаем время
        dec_time = random.randint(2,3)
        big_time_change (self, dec_time)
        # если подобрала защита, выводим текст в лог игры, добавляем статистику игры и начинаем новую атаку
        if (res == 0):
            self.window.add_log(self.score,"Защита подобрала мяч ({})".format(self.comands_name[not self.possession]))
            self.int_to_team[not self.possession].my_def_reb()
            team.my_att_reb(False)
            raise NewAttackException(self)
        # если подобрала атака, обновляем время атаки, обновляем статистику, продолжаем игру
        self.int_to_team[not self.possession].my_def_reb(False)
        team.my_att_reb()
        self.attack_time = 14
        self.window.change_attack_time(self.attack_time)
        self.window.add_log(self.score,"Атака подобрала мяч ({})".format(self.comands_name[self.possession]))


    # поле bonus корректирует вероятность в зависимости от игровой ситуации (если игрок сразу бросает 
    # треочковый первым действием, то вероятность блока будет больше, если игрок сразу идет в дриблинг, то
    # вероятность отбора будет больше)

    # генерируем отбор
    def steal(self, team, bonus = 1):
        res = bernoulli.rvs(size = 1, p = team.steal)[0]
        # если отбор состоялся, то обновляем статистику и начинаем новую атаку
        if (res == 1):
            self.int_to_team[not self.possession].my_steal()
            self.window.add_log(self.score,"Защита отобрала мяч ({})".format(self.comands_name[not self.possession]))
            raise NewAttackException(self)
        # добавляем статистику, если отбор не состоялся
        self.int_to_team[not self.possession].my_steal(False)

    # генерируем перехват паса. Аналогично. Если пас прошел, просто добавляем статистику, если не прошел, то еще 
    # выводим это в лог игры и начинаем новую атаку
    def block_pass(self, team, bonus = 1):
        res = bernoulli.rvs(size = 1, p = team.turnover * bonus / 2)[0]
        if (res == 1):
            self.int_to_team[not self.possession].my_turnover()
            self.window.add_log(self.score,"Защита перехватила пас ({})".format(self.comands_name[not self.possession]))
            raise NewAttackException(self)
        self.int_to_team[not self.possession].my_turnover(False)

    # генерируем блокировку, все абсолютно аналогично
    def block_throw(self, team, bonus = 1):
        res = bernoulli.rvs(size = 1, p = team.block * bonus)[0]
        if (res == 1):
            self.int_to_team[not self.possession].my_block()
            self.window.add_log(self.score,"Защита заблокировала бросок ({})".format(self.comands_name[not self.possession]))
            raise NewAttackException(self)
        self.int_to_team[not self.possession].my_block(False)

    # генерирует штрафные броски (принимаем на сколько бросков был фол)
    def free_throw(self, team, num):
        # кроме последнего
        for i in range(num - 1):
            self.score[self.possession] += (goal := bernoulli.rvs(size = 1, p=team.free_points)[0])
            # если попал, добавили статистику, вывели в лог игры, сменили счет
            if (goal == 1):
                team.throw(1)
                self.window.add_log(self.score,"{}-ый штрафной заброшен ({})".format(i+1, (self.comands_name[self.possession])), self.time)
                self.window.change_score(self.score[0], self.score[1])
            # не попал - просто добавили статистику, вывели лог
            else:
                team.throw(1, False)
                self.window.add_log(self.score,"{}-ый штрафной не заброшен ({})".format(i+1, self.comands_name[self.possession]))
        self.score[self.possession] += (goal := (bernoulli.rvs(size = 1, p=team.free_points)[0]))
        # если забил последний, то новая атака (счет, статистика, лог аналогично)
        if (goal == 1):
            team.throw(1)
            self.window.add_log(self.score,"Последний штрафной заброшен ({})".format(self.comands_name[self.possession]), self.time)
            self.window.change_score(self.score[0], self.score[1])
            raise NewAttackException(self)
        # если последний не забил, то генерируем подбор мяча
        team.throw(1, False)
        self.window.add_log(self.score,"Последний штрафной не заброшен. Подбор.")
        self.rebound(team)

    # генерируем фол (храним на сколько бросков фол)
    def foul(self, team, if_throw = 0, bonus = 1) :
        # фолит соперник
        a_team = (self.against_team(team))
        if_foul = bernoulli.rvs(size = 1, p = a_team.fouls * bonus)
        # если бы фол
        if (if_foul == 1):
            # обновляем статистику
            self.int_to_team[not self.possession].my_foul()
            self.fouls[self.team_to_int[a_team]] += 1
            # проверяем, пробиваемый ли фол. Да - вызываем штрафные броски, нет - новая атака
            if (self.fouls[self.team_to_int[a_team]] > Const.kMaxFouls) or (if_throw != 0):
                self.window.add_log(self.score,"Фол защиты co штрафным ({})".format(self.comands_name[not self.possession]))
                self.free_throw(team, if_throw)
            else:
                self.window.add_log(self.score,"Фол защиты без штрафного ({})".format(self.comands_name[not self.possession]))
                self.attack_time = Const.kBaseAttackTime
                self.window.change_attack_time(self.attack_time)
            return True
        # если не фол, просто добавляем статистику
        self.int_to_team[not self.possession].my_foul(False)
        return False

class Player_attack:
    # функция, отвечающая за бросок команды в кольцо
    @classmethod
    def throwing(cls, now_game, team, points, bonus_def = 1):
        goal = 0
        # отнимаем время
        dec_time = random.randint(2,4)
        big_time_change (now_game, dec_time)
        # проверяем на фол и блок броска
        now_game.foul(team, points, 0.6)
        now_game.block_throw(now_game.against_team(team), (42 - now_game.passes_now) / 30 * bonus_def * (1 + 0.4 * (now_game.attack_time > 10)))
        # сложными математическими вычислениями вычисляем вероятность попадания в кольцо
        if points == 2:
            now_game.score[now_game.possession] += (goal := (bernoulli.rvs(size = 1, p=min((team.field_point * (9 + 0.5 * now_game.passes_now) / 10) * (1 - 0.15 * (now_game.attack_time > 10)), 0.99))[0] * points))
        else:
            now_game.score[now_game.possession] += (goal := (bernoulli.rvs(size = 1, p=min((team.three_point * (7 + 0.9 * now_game.passes_now) / 10) * (1 - 0.5 * (now_game.attack_time > 16)), 0.99))[0] * points))
        # если попали в кольцо, добавляем статистику, пишем в лог и меняем счет и время, а также начинаем новую атаку
        if (goal != 0):
            team.throw(points)
            now_game.window.add_log(now_game.score,"Заброшен {}-очковый ({})".format(points, (now_game.comands_name[now_game.possession])),now_game.time)
            now_game.window.change_score(now_game.score[0], now_game.score[1])
            now_game.window.change_time(now_game.time)
            raise NewAttackException(now_game)
        # если не попали, то после добавления в статистику генерируем подбор
        now_game.window.add_log(now_game.score,"бросок... промах! ({})".format(now_game.comands_name[now_game.possession]))
        team.throw(points, False)
        now_game.rebound(team)

    # функция, отвечающая за "пас". Количество пасов считается, отнимается время на пас
    @classmethod
    def try_pass(cls, now_game, team, bonus_def = 1):
        # проверка на то, был ли отбор
        now_game.block_pass(now_game.against_team(team), bonus_def)
        dec_time = random.randint(1,2)
        big_time_change (now_game, dec_time)
        now_game.passes_now += 1

    # аналогично с дриблингом. проверяем на фол, проверяем на отбор, отнимаем время и кидаем двухочковый
    @classmethod
    def try_dribble(cls, now_game, team, bonus_def = 1):
        # проверяем на фол
        now_game.foul(team, 0, bonus_def / 2 + 0.6)
        # вычитаем время
        dec_time = random.randint(2,4)
        big_time_change (now_game, dec_time)
        # проверяем на отбор
        now_game.steal(now_game.against_team(team), 1.7 * (now_game.passes_now**(-0.4)) * bonus_def)
        Player_attack.throwing(now_game, team, Const.kScoreTwoPointer)

class Player_defence:
    # если ИИ или игрок выбрали отбор
    @classmethod
    def try_steal(cls,now_game, team):
        # если пользователь играет сам пишем в лог игры о его действии
        if (now_game.type == 1):
            now_game.window.add_log(now_game.score, "Пытаемся отобрать")
        # выбираем действие для ИИ
        act = CPU_random_att(now_game.attack_time)
        # если пас, то мы увеличиваем вероятность отбора
        if (act == "pass"):
            Player_attack.try_pass(now_game, now_game.against_team(team), 1.1)
        # если дриблинг, то мы сильно увеличиваем вероятность отбора
        if (act == "dribble"):
            Player_attack.try_dribble(now_game, now_game.against_team(team), 1.3)
        # если бросок, то защитник ошибся и с меньшей вероятностью заблокирует бросок
        if (act == "throw3"):
            Player_attack.throwing(now_game, now_game.against_team(team), Const.kScoreThreePointer, 0.8)

    # все аналогично с попыткой перехватить пас
    @classmethod
    def try_block_pass(cls, now_game, team):
        if (now_game.type == 1):
            now_game.window.add_log(now_game.score, "Пытаемся заблокировать пас")
        # выбираем действие для ИИ
        act = CPU_random_att(now_game.attack_time)
        # если угадали, то бонус
        if (act == "pass"):
            Player_attack.try_pass(now_game, now_game.against_team(team), 1.3)
        # если дриблинг, то немного увеличиваем вероятность отбора
        if (act == "dribble"):
            Player_attack.try_dribble(now_game, now_game.against_team(team), 1.1)
        # если бросок, то вероятность заблокировать уменьшается
        if (act == "throw3"):
            Player_attack.throwing(now_game, now_game.against_team(team), Const.kScoreThreePointer, 0.85)

    # тоже аналогично с броском
    @classmethod
    def try_block_throw(cls, now_game, team):
        if (now_game.type == 1):
            now_game.window.add_log(now_game.score, "Пытаемся заблокировать бросок")
        # выбираем действие для ИИ
        act = CPU_random_att(now_game.attack_time)
        # если не бросок, скорее всего не отберем мяч (уменьшили вероятность)
        if (act == "pass"):
            Player_attack.try_pass(now_game, now_game.against_team(team), 0.8)
        elif (act == "dribble"):
            Player_attack.try_dribble(now_game, now_game.against_team(team), 0.95)
        # если бросок, то блокируем с большой вероятностью
        elif (act == "throw3"):
            Player_attack.throwing(now_game, now_game.against_team(team), Const.kScoreThreePointer, 2)

# функция отвечает за период в игре: пока не кончится время, команды играют
def start_period(now_game, type):
    now_game.possession = random.randint(0,1)
    while (now_game.time > 0):
        try:
            now_game.play(type, now_game.possession)
        # если новая атака, то мы при создании исключения поменяли владение и просто продолжаем
        except NewAttackException as e:
            continue

# главная функция файла. Создает объект игры и генерирует игру в 4 периодах и затем, пока равных счет
# затем вызывает функцию, которая выводит статистику 
def start_game(type, first, second, window):
    now_game = Game(first, second, window, type)
    for period in range(Const.kPeriodNumber):
        now_game.new_period()
        window.button_start_period(now_game, type, period + 1)
    while (now_game.score[0] == now_game.score[1]):
        now_game.new_period()
        window.button_start_period(now_game, type, now_game.period)
    window.after_game(first, second, now_game.score)