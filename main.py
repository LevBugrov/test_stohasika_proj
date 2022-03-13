import queue as qu

days = 20
queue_front_desk = qu.Queue(days=days, rooms=30)
queue_online = qu.Queue(days=days, rooms=30)
for i in range(days):
    print(f"day N{i} number of free rooms: {queue_front_desk.free_rooms_alt(i)}")


print(queue_front_desk.profit)
