from csp import Region
from csp import get_pos


# 获得Region r的pos处的太阳能收获量
def get_solar(r, pos):
    return  r.g[pos].s


# 返回路径和预计的太阳能收获量
def get_routing(start, end, r):
    dp = [[0 for i in range(r.width)] for j in range(r.height)]
    path = [[0 for i in range(r.width)] for j in range(r.height)]
    sx, sy = get_pos(start)   # 开始的坐标
    ex, ey = get_pos(end)     # 结束的坐标

    route = []
    dp[sx][sy] = get_solar(r, start)

    # path的值的含义(表示上个格子是如何到达这个格子的)
    # 1:up 2:right 3:down 4:left

    if sx > ex:
        if sy > ey:
            for i in range(sx, ex - 1, -1):
                for j in range(sy, ey - 1, -1):
                    if j - 1 >= 0:
                        dp_left = dp[i][j] + get_solar(r, i * r.width + j - 1)
                        if dp_left > dp[i][j - 1]:
                            dp[i][j - 1] = dp_left
                            path[i][j - 1] = 4
                    if i - 1 >= 0:
                        dp_up = dp[i][j] + get_solar(r, (i - 1) * r.width + j)
                        if dp_up > dp[i - 1][j]:
                            dp[i - 1][j] = dp_up
                            path[i - 1][j] = 1

        else:
            for i in range(sx, ex - 1, -1):
                for j in range(sy, ey + 1):
                    if j + 1 < r.width:
                        dp_right = dp[i][j] + get_solar(r, i * r.width + j + 1)
                        if dp_right > dp[i][j + 1]:
                            dp[i][j + 1] = dp_right
                            path[i][j + 1] = 2
                    if i - 1 >= 0:
                        dp_up = dp[i][j] + get_solar(r, (i - 1) * r.width + j)
                        if dp_up > dp[i - 1][j]:
                            dp[i - 1][j] = dp_up
                            path[i - 1][j] = 1

    else:
        if sy > ey:
            for i in range(sx, ex + 1):
                for j in range(sy, ey - 1, -1):
                    if j - 1 >= 0:
                        dp_left = dp[i][j] + get_solar(r, i * r.width + j - 1)
                        if dp_left > dp[i][j - 1]:
                            dp[i][j - 1] = dp_left
                            path[i][j - 1] = 4
                    if i + 1 < r.height:
                        dp_down = dp[i][j] + get_solar(r, (i + 1) * r.width + j)
                        if dp_down > dp[i + 1][j]:
                            dp[i + 1][j] = dp_down
                            path[i + 1][j] = 3
        else:
            for i in range(sx, ex + 1):
                for j in range(sy, ey + 1):
                    if j + 1 < r.width:
                        dp_right = dp[i][j] + get_solar(r, i * r.width + j + 1)
                        if dp_right > dp[i][j + 1]:
                            dp[i][j + 1] = dp_right
                            path[i][j + 1] = 2
                    if i + 1 < r.height:
                        dp_down = dp[i][j] + get_solar(r, (i + 1) * r.width + j)
                        if dp_down > dp[i + 1][j]:
                            dp[i + 1][j] = dp_down
                            path[i + 1][j] = 3

    for i in range(min(sx, ex), max(sx, ex) + 1):
        for j in range(min(sy, ey), max(sy, ey) + 1):
            print(round(get_solar(r, i * r.width + j), 2), end=' ')
        print('\n')

    # 回溯，获得最佳路径
    route = [[ex, ey]]
    now_x = ex
    now_y = ey
    while now_x != sx or now_y != sy:
        if path[now_x][now_y] == 1:
            now_x += 1
        elif path[now_x][now_y] == 2:
            now_y -= 1
        elif path[now_x][now_y] == 3:
            now_x -= 1
        else:
            now_y += 1
        route.append([now_x, now_y])

    return list(reversed(route)), dp[ex][ey]


if __name__ == '__main__':
    r = Region()
    start = int(input())
    end = int(input())
    # start = 1
    # end = 1
    route, sum_solar = get_routing(start, end, r)
    for _ in route:
        print(_[0], _[1])
    print(sum_solar)