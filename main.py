# свои файлы
import from_csv
import input

if __name__ == '__main__':
    # получаем статистику выбранных команд
    stats_array = from_csv.get_stats()
    # получаем порядковые номера команд, тип игры и пользовательский путь до файла
    team, type = input.start(stats_array)