# для копирования таблицы Эксель
import csv

csv_array = []

#возвращаем массив со статистикой, из которого потом создадим объект команды
def get_stats(csv_file_path = "Basket.csv"):
    try:
        #читаем файл, добавляем статистику в массив
        with open(csv_file_path, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                csv_array.append(row)
        return csv_array
    #если пользовательский путь неверен, то используем путь по умолчанию
    except Exception as e:
        with open("Basket.csv", 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                csv_array.append(row)
        return csv_array