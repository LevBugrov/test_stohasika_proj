import random as rm
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


class Queue:
    def __init__(self, seed=rm.randint(0, 10 ** 5), days=50, lam=1, u=2, size=10):
        self.seed = seed
        rm.seed(self.seed)
        self.lam = lam  # интенсивность прибытия запросов
        self.u = u  # 1\u - ожидаемое время обслуживания
        self.days = days  # ограничение очереди количеством дней
        self.server_size = size  # максимальное количество запросов которое может обслужить сервер за раз

        self.tac = []  # time of arrival of clients
        self.spr = []  # the time the server is processing requests and
        self.requests_served = 0
        self.average_number_of_clients = [0] * days  # доделать

        # цикл заполняющий массив временем поступления нового запроса
        time_of_arrive = 0
        time_next_request = rm.expovariate(lam)

        while time_of_arrive + time_next_request < days:
            time_of_arrive += time_next_request
            self.tac.append(time_of_arrive)
            time_next_request = rm.expovariate(lam)

        # цикл заполняющий массив временем начала обработки заявок
        service_time = 0
        time_next_service = 0
        while service_time + time_next_service < days and self.time_of_next_client(service_time+time_next_service):
            server_is_waiting = False
            service_time += time_next_service

            if self._get_queued_requests(service_time) == 0:
                service_time = self.time_of_next_client(service_time)
                print('wait... to ', service_time)
                server_is_waiting = True
            requests_in_server_now = self._get_queued_requests(service_time)
            self.requests_served += requests_in_server_now
            self.spr.append((service_time, requests_in_server_now, server_is_waiting))
            time_next_service = rm.expovariate(u)

    def _get_queued_requests(self, time):
        for i in range(len(self.tac)):
            if time == self.tac[i]:
                out = i + 1 - self.requests_served
                return out if out > 0 else 0
            elif time < self.tac[i]:
                out = i - self.requests_served
                return out if out > 0 else 0
        return 0

    def time_of_next_client(self, time):
        for i in self.tac:
            if i >= time:
                return i
        return 0

    def draw_(self, array_name: str, sort=False):
        arrays = {"tac": self.tac,
                  "spr": self.spr,
                  "average_number_of_clients": self.average_number_of_clients
                  }
        if array_name in arrays:
            sns.barplot(x=[i for i in range(len(arrays[array_name]))],
                        y=(arrays[array_name].sort if sort else arrays[array_name]))
            plt.show()
        else:
            print("--------------------------------------\nмассив не найден\n--------------------------------------")

    def draw_hist(self):
        df = pd.DataFrame({'day': [i for i in range(self.days)], 'proceeds': self.days})
        sns.barplot(x='day', y='proceeds', data=df)
