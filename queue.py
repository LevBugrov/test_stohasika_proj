import random as rm
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


class Queue:
    def __init__(self, seed=rm.randint(0, 10 ** 5), days=50, lam=20, u=0.5, rooms=100):
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
        time_of_leave = 0

        self.time_of_events = []
        while self.time_of_events or self.time_of_events[-1][0] < days:
            if self.free_rooms > 0:
                time_of_arrive += rm.expovariate(lam)
                self.free_rooms -= 1
                self.add_toe(time_of_arrive, True)

                time_of_leave = time_of_arrive + 1 + int(rm.expovariate(u))
                self.add_toe(time_of_leave, False)


        # while self.tac[-1] < self.days:
        #     time += rm.expovariate(lam)
        #     if self.free_rooms > 0:
        #         self.tac.append(time)
        #         self.crt.append(1 + int(rm.expovariate(u)))
        #         self.free_rooms -= 1
        #     else:
        #         pass

        # self.timeline = [0 for i in range(int(self.tac[-1]) + 1)]
        # for i in range(len(nums)):
        #     self.timeline[int(self.tac[i])] += self.crt[i]

    def add_toe(self, time, customer_has_arrived: bool):
        if not self.time_of_events:
            self.time_of_events = [[]]
        else:
            for i in range(len(self.time_of_events)-1, 0, -1):
                if self.time_of_events[i][0] < time:
                    self.time_of_events.insert(i+1, [time, customer_has_arrived])
                    return
        print("добавление прошло безуспешно")
        return

    def get_tac(self):
        return self.tac

    def get_crt(self):
        return self.crt

    def get_toe(self):
        return self.time_of_events

    def draw_(self, array_name: str, sort=False):
        arrays = {"tac": self.tac,
                  "crt": self.crt
                  }
        if array_name in arrays:
            sns.barplot(x=[i for i in range(len(arrays[array_name]))],
                        y=(arrays[array_name].sort if sort else arrays[array_name]))
            plt.show()
        else:
            print(
                "----------------------------------------\nмассив не найден\n----------------------------------------")
