class Teams:
    def __init__(self, array_of_stats, num):
        self.name = array_of_stats[num][1]
        #процент попадания двухочковых
        self.field_point = float(array_of_stats[num][2])/100.0
        #процент трехочковых
        self.three_point = float(array_of_stats[num][3])/100.0
        #процент попадания штрафных
        self.free_points = float(array_of_stats[num][4])/100.0
        # количество подборов в атаке за матч (в алгоритме конвертируется в проценты)
        self.off_rebound = float(array_of_stats[num][5])
        # количество подборов в защите
        self.def_rebound = float(array_of_stats[num][6])
        # шанс (процент) перехвата
        self.turnover = float(array_of_stats[num][7])/100.0
        # шанс отбора
        self.steal = float(array_of_stats[num][8])/100.0
        # шанс блока броска
        self.block = float(array_of_stats[num][9])/100.0
        # шанс фола
        self.fouls = float(array_of_stats[num][10])/200.0
        self.const_arr = array_of_stats[num]
        # массив для хранения статистики игры
        self.stats = [[0] * 2 for _ in range(9)]

    # Следующие функции отвечают за формирования массива с статистикой по игре
    # Названия совпадают с полями, переменная success означает, удачно ли действие
    def throw(self, point, success=True):
        if (point == 2):
            self.stats[0][1] += 1
            self.stats[0][0] += int(success)
        elif (point == 3):
            self.stats[1][1] += 1
            self.stats[1][0] += int(success)
        elif (point == 1):
            self.stats[2][1] += 1
            self.stats[2][0] += int(success)
    
    def my_att_reb(self, success = True):
        self.stats[3][1] += 1
        self.stats[3][0] += int(success)
    
    def my_def_reb(self, success = True):
        self.stats[4][1] += 1
        self.stats[4][0] += int(success)
    
    def my_turnover(self, success = True):
        self.stats[5][1] += 1
        self.stats[5][0] += int(success)
    
    def my_steal(self, success = True):
        self.stats[6][1] += 1
        self.stats[6][0] += int(success)

    def my_block(self, success = True):
        self.stats[7][1] += 1
        self.stats[7][0] += int(success)

    def my_foul(self, success = True):
        self.stats[8][1] += 1
        self.stats[8][0] += int(success)

    def __str__(self):
        return f"Player: {self.name}\n" \
            f"Field Point Percentage: {self.field_point}\n" \
            f"Three Point Percentage: {self.three_point}\n" \
            f"Free Throw Percentage: {self.free_points}\n" \
            f"Offensive Rebounds: {self.off_rebound}\n" \
            f"Defensive Rebounds: {self.def_rebound}\n" \
            f"Turnover Percentage: {self.turnover}\n" \
            f"Steal Percentage: {self.steal}\n" \
            f"Block Percentage: {self.block}\n" \
            f"Foul Percentage: {self.fouls}\n"