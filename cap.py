import random
import csp
from csp import Region

# 论文中提到的大数减去d值
def cap_d(x1, y1, x2, y2):
    return 100000 - csp.d(x1, y1, x2, y2)

def solve(r):
    req = []
    # 随机生成充电请求
    for g in r.g:
        for i in range(g.r):
            req.append([g.x, g.y, random.uniform(10, 20)])
    n = len(req)
    m = len(r.h)

    # 把路径数组和dp数组初始化为0
    path = [[0 for i in range(1000)] for i in range(1000)]
    dp = [[0 for i in range(1000)] for i in range(1000)]

    # vis[i]为1代表第i个充电请求已被满足
    vis = [0 for i in range(len(req))]
    result = []

    # 对于每个充电站点
    for i in range(m):

        n = len(req)

        s = int(r.g[r.h[i].id].s)
        x = r.g[r.h[i].id].x
        y = r.g[r.h[i].id].y    # 获得当前站点的坐标和太阳能量

        for j in range(n + 1):
            for k in range(s):
                dp[j][k] = path[j][k] = 0

        for j in range(n):
            if vis[j] == 1:

                for k in range(s):
                    dp[j + 1][k] = dp[j][k]
                continue

            for k in range(s):
                e = int(req[j][2])
                if e > k:
                    dp[j + 1][k] = dp[j][k]
                else:
                    dp[j + 1][k] = dp[j][k]
                    new_dp = dp[j][k - e] + cap_d(req[j][0], req[j][1], x, y)
                    if new_dp > dp[j][k]:
                        dp[j + 1][k] = new_dp
                        path[j + 1][k] = 1

        # 回溯，获得分配方案
        j = n
        k = s
        cars = []

        while j > 0 and k > 0:
            if path[j][k] == 1:
                vis[j - 1] = 1
                cars.append(req[j - 1])
                k -= int(req[j - 1][2])
            j -= 1

        # 删掉已分配的充电请求
        req = [req[_] for _ in range(n) if vis[_] == 0]
        result.append(cars)

    return result


if __name__ == '__main__':
    r = Region()
    k = 10

    r.select(k)
    result = solve(r)

    for i in range(len(result)):
        x = result[i]
        if len(x) == 0:
            continue
        print(r.h[i])
        for y in x:
            print(y, end=' ')
        print('\n')
