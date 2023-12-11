from globals import Const
# для всего интерфейса
import tkinter as tk
# свой файл
import game
# для вывода текста в рабочем окне
from tkinter import scrolledtext
from tkinter import font
# для скорости игры
import time

# весь файл отвечает за окно с игрой
class InteractiveWindow:
    # формируем начальное окно
    def __init__(self, root, type, fteam = "Golden State Warriors", steam = "Brooklyn Nets", fcount = 0, scount = 0):
        self.speed = 0
        self.root = root
        # заголовок окна
        root.title("Окно игры")
        # размер окна
        root.geometry("1200x800")
        # переменная для ожидания нажатия на кнопку
        self.user_clicked = tk.BooleanVar()
        self.user_clicked.set(False)

        # текст с номером периода (меняется по ходу игры) в левом верхнем углу
        self.period_label = tk.Label(root, text="Период: 1")
        self.period_label.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        # текст с названием команд (правее)
        self.team_label = tk.Label(root, text=(fteam.name + " - " + steam.name), font=("italic"))
        self.team_label.grid(row=0, column=1, columnspan=4, pady=0)

        # текст с временем в периоде (под номером периода) - тоже меняется по ходу игры
        self.time_label = tk.Label(root, text="Время: 12:00")
        self.time_label.grid(row=1, column=0, sticky="nw", padx=10, pady=0)

        # счет. аналогично
        self.score_label = tk.Label(root, text=str(fcount) + " - " + str(scount))
        self.score_label.grid(row=1, column=1, columnspan=3, pady=0)

        # создаем большую область справа для вывода лога (комментариев) игры
        self.commentary_label = tk.Label(root, text="Текст игры:")
        self.commentary_label.grid(row=0, column=12, columnspan=3, padx=200)
        self.text_area = scrolledtext.ScrolledText(root, width=80, height=40)
        # запрещаем пользователю туда писать
        self.text_area.configure(state="disabled")
        self.text_area.grid(row=1, column = 14, rowspan=15, padx = 30, pady=0)

        # три начальные кнопки. В СЛУЧАЙНОМ РЕЖИМЕ КНОПКИ - и + отвечают за "скорость игры"
        self.button1 = tk.Button(root, text="-", command=lambda: self.dec_speed(), width=25, height=1)
        self.button1.grid(row=2, column=2, pady=0)

        self.button2 = tk.Button(root, text="Начать игру", command=lambda: game.start_game(type, fteam, steam, self),width=25, height=1)
        self.button2.grid(row=3, column=2, pady=0)

        self.button3 = tk.Button(root, text="+", command=lambda: self.inc_speed(), width=25, height=1)
        self.button3.grid(row=4, column=2, pady=0)

        # текст с временем атаки
        self.attack_time_label = tk.Label(root, text="Время атаке: 24'")
        self.attack_time_label.grid(row=2, column=0, sticky="nw", padx=10, pady=0)

    # две функции, отвечающие за ускорение и замедление скорости игры
    def dec_speed(self):
        self.speed -= 0.2
        if (self.speed < 0):
            self.speed = 0
    
    def inc_speed(self):
        self.speed += 0.2

    # добавление лога игры в текстовое окно
    def real_add_log(self, score, text, mtime = -1):
        if (mtime != -1): 
            # выводим время
            min = mtime // 60
            sec = mtime % 60
            log_text = "  {} - {} {:02d}:{:02d}".format(score[0], score[1], min, sec) + ' ' + text
            # сам текст с жирным 14-ым Ариалом
            self.text_area.tag_configure("import", font=("Arial", 14, "bold"))
            self.text_area.configure(state="normal")
            self.text_area.insert(tk.END, log_text + '\n', "import")
            self.text_area.configure(state="disabled")
        # если не передавалось время, то это посредственное сообщение - выводим мелко    
        else:
            log_text = "    " + text
            self.text_area.configure(state="normal")
            self.text_area.insert(tk.END, log_text + '\n')
            self.text_area.configure(state="disabled")
        self.text_area.yview(tk.END)
        self.root.update()
        self.text_area.yview(tk.END)

    # вспомогательная функция для замедления или ускорения скорости игры
    def add_log(self, score, text, mtime = -1):
        time.sleep(self.speed)
        self.real_add_log(score, text, mtime)

    # меняет время периода в окне    
    def change_time(self, time):
        min = time // Const.kSecInMin
        sec = time % Const.kSecInMin
        self.time_label.config(text="Время: {:02d}:{:02d}".format(min, sec))

    # меняет время атаки в окне
    def change_attack_time(self, time = Const.kBaseAttackTime):
        self.attack_time_label.config(text="Время атаке: {:02d}'".format(time))

    # меняет счет
    def change_score(self, score1, score2):
        self.score_label.config(text="{} - {}".format(score1, score2))

    # меняет период на экране
    def change_period(self, score, period):
        if (period > 1):
            self.add_log(score, '\n')
        self.add_log(score,"{}-ый период".format(period), 720)
        self.period_label.config(text="Период: {}".format(period))

    # кнопка для старта нового периода
    def button_start_period(self, now_game, type, num):
        self.off_button_click()
        self.button1.config(text="-", command=lambda: self.dec_speed())
        self.button3.config(text="+", command=lambda: self.inc_speed())
        self.button2.config(text="Начать {} период".format(num), command=lambda: (game.start_period(now_game, type), self.on_button_click()))
        self.root.update()
        self.root.wait_variable(self.user_clicked)

    # меняет состояние кнопки для продолжение программы
    def on_button_click(self):
        self.user_clicked.set(True)

    def off_button_click(self):
        self.user_clicked.set(False)

    # кнопки для выбора действия в атаке пользователем
    def player_attack(self, now_game, team):
        self.off_button_click()
        self.button1.config(text="Отдать пас в зону", command=lambda: (self.on_button_click(), game.Player_attack.try_pass(now_game, team)))
        self.button3.config(text="Дриблинг (+ двухочковый)", command=lambda: (self.on_button_click(), game.Player_attack.try_dribble(now_game, team)))
        self.button2.config(text="Бросить трехочковый", command=lambda: (self.on_button_click(), game.Player_attack.throwing(now_game, team, 3)))
        self.root.update()
        # ждет нажатия
        self.root.wait_variable(self.user_clicked)

    # кнопки для выбора действия в защите пользователем
    def player_defence(self, now_game, team):
        self.off_button_click()
        self.button1.config(text="Попытаться отобрать", command=lambda: (self.on_button_click(), game.Player_defence.try_steal(now_game, team)))
        self.button3.config(text="Сыграть аккуратно", command=lambda: (self.on_button_click(), game.Player_defence.try_block_pass(now_game, team)))
        self.button2.config(text="Подпрыгнуть", command=lambda: (self.on_button_click(), game.Player_defence.try_block_throw(now_game, team), self.on_button_click()))
        self.root.update()
        # ждет нажатия
        self.root.wait_variable(self.user_clicked)

    # функция отвечает за вывод статистики
    def after_game(self, team1, team2, score):
        # три кнопки и ожидание нажатия на "Показать статистику"
        self.off_button_click()
        self.button1.config(text="-", command="")
        self.button3.config(text="-", command="")
        self.button2.config(text="Показать статистику", command=lambda: self.on_button_click())
        self.root.update()
        self.root.wait_variable(self.user_clicked)        
        
        # удаляем все
        for widget in self.root.winfo_children():
            widget.destroy() 
        
        self.root.destroy()

        # создаем новое окно
        self.root = tk.Tk()

        # новое заглавие
        self.root.title("Статистика")
        canvas = tk.Canvas(self.root, height=800, width=1000)
        canvas.pack(expand=tk.YES, fill=tk.BOTH)

        # формируем статистики
        values1 = [s[0] for s in team1.stats]
        values2 = [s[0] for s in team2.stats]

        # формируем еще статистики (там мы брали успешные действия, а тут определенные "все")
        for i in range(3):
            values1.insert(i*2 + 1, team1.stats[i][1])
            values2.insert(i*2 + 1, team2.stats[i][1])
        
        # добавляем счет
        values1.insert(0, score[0])
        values2.insert(0, score[1])

        # это наши статистики в нужном порядке
        labels = [
            "Points",
            "Field Point made",
            "Field Point attempted",
            "Three Point made",
            "Three Point attempted",
            "Free Throw made",
            "Free Point attempted",
            "Offensive Rebounds",
            "Defensive Rebounds",
            "Turnovers made",
            "Steals made",
            "Blocks made",
            "Fouls made"
        ]

        # формируем интерфейс нашей статистики
        bar_height = 10
        bar_spacing = 40

        text_x = 500
        text_y = 30
        temp_font = font.Font(family="Arial", size=16, weight="bold")
        team1_name_width = temp_font.measure(team1.name + " ")
        # верхняя крупная надпись с командами
        canvas.create_text(text_x - team1_name_width, text_y, anchor=tk.W, text=f"{team1.name} - {team2.name}", font=("Arial", 16, "bold"))

        # важные геометрические расчеты для аккуратного отображения наших статистик
        for i, (value1, value2) in enumerate(zip(values1, values2)):
            x1 = 100
            y1 = 20 * (i > 0) + 50 + bar_spacing + i * (bar_height + bar_spacing)
            x2 = 1000 * (value1 / (value2 + value1))
            y2 = y1 + bar_height
            # особые условия, если у одной команды одна из статистик нулевая
            if (value1 == 0) and (value2 != 0):
                x2 = 100
            if (value1 == 0) and (value2 == 0):
                continue
            if (value1 != 0) and (value2 == 0):
                x2 = 900
            # вывод полоски для первой команды
            canvas.create_rectangle(x1, y1, x2, y2, fill="blue")

            x3 = 900
            # вывод полоски для первой команды
            canvas.create_rectangle(x2, y1, x3, y2, fill="green")

            text_x = 500
            text_y = y1 - 2 
            canvas.create_text(text_x, text_y, anchor=tk.S, text=f"{labels[i]}", font=("Arial", 12,"bold"))

            canvas.create_text(x1 - 5, (y1 + y2) / 2, anchor=tk.E, text=f"{value1:.0f}")
            canvas.create_text(x3 + 5, (y1 + y2) / 2, anchor=tk.W, text=f"{value2:.0f}")

# функция, создающая главное окно и выводящая его на экран
def start(name1, name2,type):
    root = tk.Tk()
    app = InteractiveWindow(root,type, name1, name2)
    root.mainloop()
