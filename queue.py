import random as rm
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


class Queue:
    def __init__(self, seed=rm.randint(0, 10 ** 5), days=50, lam=20, u=0.5, rooms=100, price=1):
        self.seed = seed
        rm.seed(self.seed)
        self.lam = lam  # скорость прибытия клиентов на стойку регистрации
        self.u = u  # 1\u - ожидаемое время пребывания клиента (дни) в отеле
        self.days = days  # ограничение очереди количеством дней
        self.rooms = rooms  # количество комнат
        self.free_rooms = rooms  # количество свободных комнат

        self.tac = []  # time of arrival of clients
        self.crt = []  # client's residence time
        time_of_arrive = 0
        self.profit = []
        time_next_customers = rm.expovariate(lam)

        while time_of_arrive + time_next_customers < days:
            if self._get_free_rooms(time_of_arrive) > 0:
                time_of_arrive += time_next_customers
                self.tac.append(time_of_arrive)

                time_of_leave = time_of_arrive + 1 + int(rm.expovariate(u))
                if len(self.profit) <= int(time_of_arrive):
                    self.profit.append(round(time_of_leave - time_of_arrive, 2) * price)
                else:
                    self.profit[int(time_of_arrive)] += round(time_of_leave - time_of_arrive, 2) * price
                self.add_crt(time_of_leave)
            else:
                time_of_arrive += time_next_customers

            time_next_customers = rm.expovariate(lam)
            # print("отказ в выдаче комнаты")

        self.time_line = [0] * days  # something like income
        for i in range(len(self.tac)):
            self.time_line[int(self.tac[i])] += self.crt[i]

        self.average_number_of_clients = [0] * days
        for i in range(days):
            self.average_number_of_clients[i] = \
                (self.average_number_of_clients[i - 1] * i + self.profit[i]/price) // (i + 1)

    def add_crt(self, time):
        if not self.crt:
            self.crt = [time]
            return
        else:
            for i in range(len(self.crt) - 1, -1, -1):
                if self.crt[i] < time:
                    self.crt.insert(i + 1, time)
                    return
        self.crt.insert(0, time)
        # print("добавление прошло безуспешно - crt", len(self.crt))
        return

    def get_tac(self):
        return self.tac

    def get_crt(self):
        return self.crt

    def get_toe(self):
        return self.time_of_events

    def _get_free_rooms(self, time):
        if not self.crt:
            return self.rooms
        for i in range(len(self.crt) - 1, -1, -1):
            if self.crt[i] < time:
                # print("normalno i rabotau :", self.rooms + i + 1 - len(self.tac), 'leave:', i + 1, "tac", len(self.tac))
                return self.rooms + i + 1 - len(self.tac)
        return self.rooms - len(self.tac)

    def free_rooms_alt(self, time):
        if not self.crt:
            return self.rooms
        arrive_clients = 0
        for i in range(len(self.tac) - 1, -1, -1):
            if self.tac[i] < time:
                arrive_clients = i + 1
                break
        for i in range(len(self.crt) - 1, -1, -1):
            if self.crt[i] < time:
                # print("normalno i rabotau :", self.rooms + i + 1 - arrive_clients, 'leave:', i + 1, "tac", arrive_clients)
                return self.rooms + i + 1 - arrive_clients
        return self.rooms - arrive_clients

    def draw_(self, array_name: str, sort=False):
        arrays = {"tac": self.tac,
                  "crt": self.crt,
                  "average_number_of_clients": self.average_number_of_clients,
                  "time_line": self.time_line
                  }
        if array_name in arrays:
            sns.barplot(x=[i for i in range(len(arrays[array_name]))],
                        y=(arrays[array_name].sort if sort else arrays[array_name]))
            plt.show()
        else:
            print(
                "----------------------------------------\nмассив не найден\n----------------------------------------")

    def draw_hist(self):
        df = pd.DataFrame({'day': [i for i in range(self.days)], 'proceeds': self.days})
        sns.barplot(x='day', y='proceeds', data=df)

