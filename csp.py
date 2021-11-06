import random
import math

width = 10    # 一个区域的宽度
height = 10   # 一个区域的高度,height*width个格子构成一个区域
px, py = 0, 0    # p是区域中心的编号，px代表在第几列，py代表在第几行


# 输入编号，返回是哪一列哪一行
def get_pos(p):
    x = int(p / width)
    y = int(p) - x * width
    return x, y


# 两个格子之间的距离
def d(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


class Grid:
    def __init__(self, id, r, s):
        self.id = id    # 编号
        self.r = r      # 请求数
        self.s = s      # 收获的太阳能
        self.x, self.y = get_pos(id)

    # 重载小于号，排序用
    def __lt__(self, other):
        if abs(self.s - other.s) > 1:
            return self.s > other.s
        else:
            return d(self.x, self.y, px, py) < d(other.x, other.y, px, py)

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return '({}, {}, {})'.format(self.x, self.y, round(self.s, 2))


class Region:    # 一个Region就是多个Grid的集合
    def __init__(self):
        self.m = 0    # 总的充电请求数
        self.p = 0    # 区域中心
        self.g = []   # 区域的所有格子
        self.h = []   # 充电站
        self.b = []   # 论文中的clusters
        # self.width = 10
        # self.height = 10

        # 生成地区编号x，随机生成r
        for i in range(height):
            for j in range(width):
                # 编号
                x = i * width + j
                # 以0.2的概率该格子内出现一个充电请求
                r = 1 if random.uniform(0, 1) > 0.8 else 0
                # 随机生成太阳能的能量
                s = random.uniform(0, 100)
                self.g.append(Grid(x, r, s))

        # 计算p和m
        for i in self.g:
            self.p += i.r * i.x
            self.m += i.r
        self.p /= self.m

        # 中心p的横纵坐标
        global px, py
        px, py = get_pos(self.p)

        # 排序，让太阳能大的放前面
        self.g.sort()

    # 忘了干啥的了，反正也没用到
    def get_max(self):
        pass

    # 选择k个地方当充电站
    def select(self, k):
        print('m = ', self.m)
        a = self.g[0 : self.m]
        result = []    # 即论文中的H
        b = []         # 论文中的B

        # 先随机选一个地方当充电站
        choice = random.randint(0, len(a) - 1)
        result.append(a[choice])
        b.append([a[i] for i in range(len(a)) if i != choice])

        for i in range(k - 1):
            max_dis = 0

            # 找到距离最大的点u
            uj = 0
            for j in range(len(result)):
                r = result[j]
                for b_ in b[j]:
                    dis = d(b_.x, b_.y, r.x, r.y)
                    if dis > max_dis:
                        max_dis = dis
                        u = b_
                        uj = j

            # 从B中删除u
            b[uj] = [_ for _ in b[uj] if _ != u]

            new_b_item = []

            # 重新分配B
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

    # 在线更新，添加车站
    def add(self, p, f):
        for h in self.h:
            if h == p:
                return
        if random.uniform(0, 1) <= 1.0 / f:
            self.h.append(p)

    # 在线更新，删除车站
    def remove(self, p, n, e, f):
        if random.uniform(0, 1) <= max(0, 1.0 / f - n / e / f):
            self.h = [_ for _ in self.h if _ != p]



if __name__ == '__main__':
    r = Region()
    # k = input()
    k = 5
    result, b =  r.select(int(k))

    # 输出格式(x,y,z) 充电站的纵横坐标，预期的太阳能收获量
    # 接下来一行输出多个这样的站点，代表附近的cluster

    for i in range(len(result)):
        r = result[i]
        print('充电站', r)
        print('附属的clusters:')
        for j in range(len(b[i])):
            print(b[i][j], end=' ')
        print('\n')