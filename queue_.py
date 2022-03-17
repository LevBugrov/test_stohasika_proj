import contextvars
import random as rm
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


class Queue:
    def __init__(self, seed=rm.randint(0, 10 ** 5), days=50, lam=20, u=1, size=10):
        self.seed = seed
        rm.seed(self.seed)
        self.lam = lam  # интенсивность прибытия запросов
        self.u = u  # 1\u - ожидаемое время обслуживания
        self.days = days  # ограничение очереди количеством дней
        self.server_size = size  # максимальное количество запросов которое может обслужить сервер за раз

        self.tac = []  # time of arrival of clients
        self.spr = []  # the time the server is processing requests 
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

            requests_in_queue = self._get_queued_requests(service_time)
            requests_in_server = requests_in_queue if requests_in_queue <= self.server_size else self.server_size
            self.requests_served += requests_in_server
            time_next_service = rm.expovariate(u)
            # (время начала обслуживания, время обслуживания, количество людей в лифте, количество людей в очереди)
            self.spr.append((service_time, time_next_service, requests_in_server, requests_in_queue - requests_in_server))

        # распорядок каждого клиента
        # (время когда клиент встал в очередь, время когда клиент вошел в лифт, время когда клиент покинул лифт)
        self.client_schedule = []
        tac_iter = 0

        for i in self.spr:
            k = i[2]
            for j in range(k):
                self.client_schedule.append((self.tac[tac_iter], i[0], i[0] + i[1]))
                tac_iter += 1

    def _get_queued_requests(self, time):
        for i in range(len(self.tac)):
            if time == self.tac[i]:
                out = i + 1 - self.requests_served
                return out if out > 0 else 0
            elif time < self.tac[i]:
                out = i - self.requests_served
                return out if out > 0 else 0
        return 0

    def _a(self, time):
        counter = 0
        for i in self.client_schedule:
            if i[0]<= time and i[1] > time:
                counter += 1
        return counter

    def time_of_next_client(self, time):
        for i in self.tac:
            if i >= time:
                return i
        return 0

    def draw_(self, array_name: str, sort=False):
        arrays = {"tac": self.tac,
                  "spr": self.spr
                  }
        if array_name in arrays:
            sns.barplot(x=[i for i in range(len(arrays[array_name]))],
                        y=(arrays[array_name].sort if sort else arrays[array_name]))
            plt.show()
        else:
            print("--------------------------------------\n массив не найден \n--------------------------------------")

    def draw_hist(self):
        df = pd.DataFrame({'day': [i for i in range(self.days)], 'proceeds': self.days})
        sns.barplot(x='day', y='proceeds', data=df)
