#! /usr/bin/env python2.7
# coding=utf-8
from __future__ import division
__author__ = 'bulu_dog'
import sys
import random
import pickle as pl

def topN(fitness_dict, N=10):
    """
         返回fitness最高的N个个体
         param fitness_dict: {(c1, c2):fitness, (c1,c3):fitness}
    """
    return enumerate(sorted(fitness_dict, key=fitness_dict.get)[:N])

output = open('fitness.pkl', 'rb')
population_fitness = pl.load(output)

#参考：http://blog.csdn.net/v_july_v/article/details/6132775
def round_robin(fitness_dict, N=10):
    """
         轮盘赌算法，返回10个个体，用于繁衍下一代
    """
    sum = 0.0
    sorted_list = sorted(fitness_dict, key=fitness_dict.get)
    min = fitness_dict[sorted_list[0]]
    max = fitness_dict[sorted_list[-1]]
    for key,value in fitness_dict.items():
        sum += (max - value)
    P = dict(fitness_dict)
    #计算每个个体被选中的概率
    for key,value in P.items():
        P[key] = (max - value) / sum    #real fitness function
    temp = 0

    #计算累计概率
    for key, value in P.items():
        P[key] = value + temp
        temp = P[key]
    seed = []
    for i in range(N):
        r = random.uniform(0, 1)
        temp = 0
        for key,value in P.items():
            if r > temp and r <= value:
                seed.append((key,fitness_dict[key]))
                #print fitness_dict[key]
                break
            temp = value

    seed.sort(key=lambda x:x[1])

    for i in range(len(seed)):
        seed[i] = seed[i][0]
    return enumerate(seed)



round_robin(population_fitness)