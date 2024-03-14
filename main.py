# свои файлы
import from_csv
import teams
import input

if __name__ == '__main__':
    # получаем статистику выбранных команд
    stats_array = from_csv.get_stats()
    # получаем порядковые номера команд, тип игры и пользовательский путь до файла
    team, type = input.start(stats_array)
    # создаем объекты
    first = teams.Teams(stats_array, teams[0] + 1)
    second = teams.Teams(stats_array, teams[1] + 1)
    print (first.name, second.name)
    # начинаем игру
    input.statistics(first, second, [])
    #game_interface.start(first, second, type)