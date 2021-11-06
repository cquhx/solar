import random
from functools import cmp_to_key


# 一个乘车请求，包含开始、结束和路程时间
class Trip:
    def __init__(self, b, f):
        self.start_time = b
        self.finish_time = f
        self.cost = f - b

    # 重载小于号，让花费时间少的排前面
    def __lt__(self, other):
        return self.cost < other.cost

    def __str__(self):
        return str(self.start_time) + ' ' + str(self.finish_time)


# 判断两个Trip是否相交
def intersect(trip1, trip2):
    return not (trip1.start_time >= trip2.finish_time or trip1.finish_time <= trip2.start_time)


# 为每个电动出租车分配单子
def k_vsta(k, e_avs, p_ch, p_tr, e_cs, t_cs, _trips, T):

    u = [[] for i in range(k)]
    sum = [0 for i in range(k)]    # 第i辆车已经花费的时间

    trips = _trips

    while True:

        trips.sort()

        end_flag = True
        for i in range(k):
            for j in range(len(trips)):
                trip = trips[j]

                intersect_flag = False
                for used in u[i]:
                    if intersect(trip, used):
                        intersect_flag = True
                        break
                # 与已经预定的行程有冲突
                if intersect_flag:
                    continue

                if sum[i] <= (T * p_ch + e_avs[i] - e_cs) / (p_tr + p_ch):
                    u[i].append(trip)
                    sum[i] += trip.cost
                    trips = [trips[_] for _ in range(len(trips)) if _ != j]    #删去该行程
                    end_flag = False
                    break

        if end_flag:
            break

    return u


if __name__ == '__main__':

    k = 20
    n = 1000
    T = 1000
    trips = []
    for i in range(n):
        t = random.randint(5, 60)
        b = random.randint(0, T - t)
        trips.append(Trip(b, b + t))
    e_avs = []
    for i in range(k):
        e_avs.append(random.uniform(5, 25))

    p_ch = random.uniform(0.05, 0.1)    # 充电速度,kwh/min
    p_tr = random.uniform(0.03, 0.05)   # 耗电速度,kwh/min
    e_cs = 1.0                          # 去往充电站的平均耗能(kwh)
    t_cs = 10                           # 去往充电站的平均时间(min)

    u = k_vsta(k, e_avs, p_ch, p_tr, e_cs, t_cs, trips, T)

    count = 0
    for i in range(k):
        u[i].sort(key=cmp_to_key(lambda x, y: x.start_time - y.start_time))
        for trip in u[i]:
            print('({}, {})'.format(trip.start_time, trip.finish_time), end=' ')
            count += 1
        print('\n')
    print(count)
