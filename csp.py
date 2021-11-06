import random
import math

width = 10
height = 10
px, py = 0, 0

def get_pos(p):
    x = int(p / width)
    y = int(p) - x * width
    return x, y


def d(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


class Grid:
    def __init__(self, id, r, s):
        self.id = id
        self.r = r
        self.s = s
        self.x, self.y = get_pos(id)

    def __lt__(self, other):
        if abs(self.s - other.s) > 1:
            return self.s > other.s
        else:
            return d(self.x, self.y, px, py) < d(other.x, other.y, px, py)

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return '({}, {}, {})'.format(self.x, self.y, round(self.s, 2))


class Region:
    def __init__(self):
        self.m = 0
        self.p = 0
        self.g = []
        self.h = []
        self.b = []
        self.width = 10
        self.height = 10

        # 生成地区编号x，随机生成r
        for i in range(self.height):
            for j in range(self.width):
                x = i * self.width + j
                r = 1 if random.uniform(0, 1) > 0.8 else 0
                s = random.uniform(0, 100)
                self.g.append(Grid(x, r, s))

        # 计算p和m
        for i in self.g:
            self.p += i.r * i.x
            self.m += i.r
        self.p /= self.m

        global px, py
        px, py = get_pos(self.p)

        self.g.sort()

    def get_max(self):
        pass

    def select(self, k):
        print('m = ', self.m)
        a = self.g[0 : self.m]
        result = []
        b = []

        choice = random.randint(0, len(a) - 1)
        result.append(a[choice])
        b.append([a[i] for i in range(len(a)) if i != choice])

        for i in range(k - 1):
            max_dis = 0

            # 找到u
            uj = 0
            for j in range(len(result)):
                r = result[j]
                for b_ in b[j]:
                    dis = d(b_.x, b_.y, r.x, r.y)
                    if dis > max_dis:
                        max_dis = dis
                        u = b_
                        uj = j

            b[uj] = [_ for _ in b[uj] if _ != u]

            new_b_item = []
            # 重新分配
            for j in range(len(result)):
                r = result[j]

                erase_list = []

                for _ in range(len(b[j])):
                    dis_pre = d(b[j][_].x, b[j][_].y, r.x, r.y)
                    dis_now = d(b[j][_].x, b[j][_].y, u.x, u.y)
                    if dis_now < dis_pre:
                        erase_list.append(_)

                new_b_item.extend(b[j][_] for _ in range(len(b[j])) if _ in erase_list)
                b[j] = [b[j][_] for _ in range(len(b[j])) if _ not in erase_list]

            result.append(u)
            b.append(new_b_item)

        self.h = result
        self.b = b
        return result, b

    def add(self, p, f):
        for h in self.h:
            if h == p:
                return
        if random.uniform(0, 1) <= 1.0 / f:
            self.h.append(p)

    def remove(self, p, n, e, f):
        if random.uniform(0, 1) <= max(0, 1.0 / f - n / e / f):
            self.h = [_ for _ in self.h if _ != p]



if __name__ == '__main__':
    r = Region()
    # k = input()
    k = 5
    result, b =  r.select(int(k))

    for i in range(len(result)):
        r = result[i]
        print(r)
        for j in range(len(b[i])):
            print(b[i][j], end=' ')
        print('\n')