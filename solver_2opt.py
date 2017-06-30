#!/usr/bin/env python3

import sys
import math
import numpy as np

from common import print_solution, read_input

cities = read_input(sys.argv[1])
N = len(cities)

#-----ここから-----greedy

def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

dist = [[0] * N for i in range(N)]
for i in range(N):
    for j in range(N):
        dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

def solve(cities):
    N = len(cities)

    current_city = 0
    unvisited_cities = set(range(1, N))
    solution = [current_city]

    def distance_from_current_city(to):
        return dist[current_city][to]

    while unvisited_cities:
        next_city = min(unvisited_cities, key=distance_from_current_city)
        unvisited_cities.remove(next_city)
        solution.append(next_city)
        current_city = next_city
    return solution

#-----ここまで-----greedy




#-----ここから-----2opt 局所探索

def calculate_path_length(solution, dist):
    """Calculate total distance traveled for given visit order"""
    path_length = 0
    for i in range(N):
        j = (i + 1)% N
        path_length += dist[solution[i]][solution[j]]
    return path_length


def calculate_2opt_exchange_cost(solution, i, j, dist):
    """Calculate the difference of cost by applying given 2-opt exchange"""
    N = len(solution)
    a, b = solution[i], solution[(i + 1) % N]
    c, d = solution[j], solution[(j + 1) % N]

    cost_before = dist[a][b] + dist[c][d]
    cost_after = dist[a][c] + dist[b][d]####
    return cost_after - cost_before


def apply_2opt_exchange(solution, i, j):
    """Apply 2-opt exhanging on visit order"""

    tmp = solution[i + 1: j + 1]
    tmp.reverse()
    solution[i + 1: j + 1] = tmp

    return solution

def improve_with_2opt(solution, dist):
    """Check all 2-opt neighbors and improve the visit order"""
    cost_diff_best = 0.0
    i_best, j_best = None, None

    for i in range(0, N - 2):
        for j in range(i + 2, N):
            if i == 0 and j == N - 1:
                continue

            cost_diff = calculate_2opt_exchange_cost(
                solution, i, j, dist)

            if cost_diff < cost_diff_best:
                cost_diff_best = cost_diff
                i_best, j_best = i, j

    if cost_diff_best < 0.0:
        solution_new = apply_2opt_exchange(solution, i_best, j_best)
        return solution_new
    else:
        return None


def local_search(solution, dist, improve_func):
    """Main procedure of local search"""
    cost_total = calculate_path_length(solution, dist)

    while True:
        improved = improve_func(solution, dist)
        if not improved:
            break

        solution = improved

    return solution




#-----ここまで-----局所探索

if __name__ == '__main__':
    assert len(sys.argv) > 1
    solution = solve(read_input(sys.argv[1]))
    # 適当に初期解を生成
    total_distance = calculate_path_length(solution, dist) #solutionのpath length
    print('初期解のpath length= {}'.format(total_distance))

    # 近傍を計算
    improved = local_search(solution, dist, improve_with_2opt)
    total_distance = calculate_path_length(improved, dist)  #improvedのpath length
    print('2-opt適用後のpath length = {}'.format(total_distance))
    print_solution(solution)
