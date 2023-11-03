# для всего интерфейса
import tkinter as tk
# для вывода текста в рабочем окне
from tkinter import messagebox
from tkinter import scrolledtext
# для случайного выбора команд
import random

# очищаем активное окно от виджетов
def clear(root):
    for widget in root.winfo_children():
        widget.destroy()

# отображаем текстовый виджет с названиями команд
def display_teams(teams, root):
        clear(root)
        # формируем текстовый виджет и отображаем ее
        text_area = scrolledtext.ScrolledText(root, width=50, height=30)
        text_area.pack()
        # заполняем виджет
        for i, team in enumerate(teams):
            text_area.insert(tk.END, f"{i + 1}. {team}\n")

# заполнение возвращаемого массива с выбранными командами (которые передаются)
def appending(first, second):    
    team.append(first - 1)
    team.append(second - 1)
    root.destroy()

# выбор команд пользователем
def choose_teams(root):
    clear(root)

    # отображает команды
    display_teams(teams, root)

    # выводит два поля для ввода команд 
    entry_label1 = tk.Label(root, text="Введите номер первой команды:")
    entry_label1.pack()
    entry1 = tk.Entry(root)
    entry1.pack()

    entry_label2 = tk.Label(root, text="Введите номер второй команды:")
    entry_label2.pack()
    entry2 = tk.Entry(root)
    entry2.pack()

    # кнопка Ок
    button = tk.Button(root, text="Ok", command=lambda: appending(int(entry1.get()), int(entry2.get())))
    button.pack(pady=10)

# выбор случайных команд
def random_teams():
    x = 0
    y = 0
    while (x == y):
        x = random.randint(0,29)
        y = random.randint(0,29)
    team.append(x)
    team.append(y)
    # закрываем окно
    root.destroy()

# заполняет возвращаемое значение и разрешает движение по коду дальше
def way(entry, list_clicked):
    way_for_table = way
    list_clicked[0].set(True)

# возвращает в первое "меню"
def return_to_main(root):
    clear(root)
    # формируем кнопку и отображаем ее
    button1 = tk.Button(root, text="Cлучайный матч", command=lambda: first_choose(0, root), width=20, height=3)
    button1.pack(pady=60)
    # формируем кнопку и отображаем ее
    button2 = tk.Button(root, text="Один игрок", command=lambda: first_choose(1, root), width=20, height=3)
    button2.pack(pady=60)
    # формируем кнопку и отображаем ее
    button3 = tk.Button(root, text="Своя настройка", command=lambda: player_stats(root), width=20, height=3)
    button3.pack(pady=60)

# создает меню для ввода своего пути к таблице    
def player_stats(root):
    clear(root)
    user_clicked = tk.BooleanVar()
    # формируем текст и отображаем его
    entry_label1 = tk.Label(root, text="Введите ccылку на свою таблицу:")
    entry_label1.pack()
    # формируем поле для ввода и отображаем его
    entry1 = tk.Entry(root)
    entry1.pack()
    # формируем кнопку и отображаем ее
    button = tk.Button(root, text="Ok", command=lambda: way(entry1.get(), [user_clicked]))
    button.pack(pady=10)
    root.wait_variable(user_clicked)
    return_to_main(root)

# предлагает выбрать команды самостоятельно или случайно
def first_choose(number, root):
    # очищаем
    clear(root)
    # указываем тип игры (потом вернем это)
    type_of_game.append(number)
    # формируем кнопку и отображаем ее
    new_button1 = tk.Button(root, text="Выбрать команды самостоятельно", command=lambda: choose_teams(root), width=40, height=3)
    new_button1.pack(pady=120)
    # формируем кнопку и отображаем ее
    new_button2 = tk.Button(root, text="Случайный выбор", command=lambda: random_teams(), width=40, height=3)
    new_button2.pack(pady=60) 

# первое меню, где можно выбрать случайно играть игру или самому, а также перейти в страницу с своей игрой
def MyApp(root):
    root = root
    # название окна
    root.title("Выбор команд")
    # размер окна
    root.geometry("600x700")
    
    clear(root)
    button1 = tk.Button(root, text="Cлучайный матч", command=lambda: first_choose(0, root), width=20, height=3)
    button1.pack(pady=60)
    button2 = tk.Button(root, text="Один игрок", command=lambda: first_choose(1, root), width=20, height=3)
    button2.pack(pady=60)
    button3 = tk.Button(root, text="Своя настройка", command=lambda: player_stats(root), width=20, height=3)
    button3.pack(pady=60)

team = []
# список команд по умолчанию
teams = [
    "Atlanta Hawks", "Boston Celtics", "Brooklyn Nets", "Charlotte Hornets",
    "Chicago Bulls", "Cleveland Cavaliers", "Dallas Mavericks", "Denver Nuggets",
    "Detroit Pistons", "Golden State Warriors", "Houston Rockets", "Indiana Pacers",
    "LA Clippers", "Los Angeles Lakers", "Memphis Grizzlies", "Miami Heat",
    "Milwaukee Bucks", "Minnesota Timberwolves", "New Orleans Pelicans",
    "New York Knicks", "Oklahoma City Thunder", "Orlando Magic", "Philadelphia 76ers",
    "Phoenix Suns", "Portland Trail Blazers", "Sacramento Kings", "San Antonio Spurs",
    "Toronto Raptors", "Utah Jazz", "Washington Wizards"]

root = tk.Tk()
# контейнер, в котором будет храниться тип игры
type_of_game = []
# переменная, в которой вернем пользовательский путь
way_for_table = "Basket.csv"

def start():
    # создаем и отображаем окно
    app = MyApp(root)
    root.mainloop()
    # возвращаем все нужные значения
    return team, *type_of_game, way_for_table