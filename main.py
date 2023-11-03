# свои файлы
import from_csv
import teams
import input
import game_interface

if __name__ == '__main__':
    # получаем порядковые номера команд, тип игры и пользовательский путь до файла
    team, type, way = input.start()
    # получаем статистику выбранных команд
    stats_array = from_csv.get_stats(way)
    # создаем объекты
    first = teams.Teams(stats_array, team[0] + 1)
    second = teams.Teams(stats_array, team[1] + 1)
    # начинаем игру
    game_interface.start(first, second, type)