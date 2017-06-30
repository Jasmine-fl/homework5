#!/usr/bin/env python3
#coding:utf-8
import itertools

import sys
import math

from common import print_solution, read_input


cities = read_input(sys.argv[1])
N = len(cities)
min = 1374393.14 #Challenge6のrandomの結果

def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2  + (city1[1] - city2[1]) ** 2)

def calculate_path_length(order_list):
    path_length = 0
    for i in range(0,N):
        path_length += distance(cities[order_list[i]], cities[order_list[i+1]])
    path_length += distance(cities[order_list[N]], cities[0])
    return path_length

def list_all_orders_without_zero(N): #start:0, goal:0
    all_cities = range(1,N)
    all_orders_without_zero = list(itertools.permutations(all_cities))
    return all_orders_without_zero

if __name__ == '__main__':
    assert len(sys.argv) > 1
    all_orders_without_zero = list_all_orders_without_zero(N)

    for order in all_orders_without_zero:
        with_zero = [0] + list(order) + [0]
        path_length = calculate_path_length(with_zero)
        if (min > path_length):
            min = path_length
            best_solution = with_zero

    best_solution.pop() #最後の0を削除

    print("best solution is = {}, min path length = {}".format(best_solution, min))
    print_solution(best_solution)