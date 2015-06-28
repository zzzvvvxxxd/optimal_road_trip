#! /usr/bin/env python2.7
# coding=utf-8
__author__ = 'bulu_dog'

"""
article:
    http://www.randalolson.com/2015/03/08/computing-the-optimal-road-trip-across-the-u-s/
    http://blog.chinaunix.net/uid-27105712-id-3886077.html
"""
import pandas as pd
import numpy as np
import random

waypoint_distances = {}
waypoint_durations = {}
all_waypoints = set()

waypoint_distance = pd.read_csv("../data/my-waypoints-dist-dur.tsv", sep="\t")

for i, row in waypoint_distance:
    waypoint_distances[frozenset([row.waypoint1, row.waypoint2])] = row.distance_m
    waypoint_durations[frozenset([row.waypoint1, row.waypoint2])] = row.duration_s
    all_waypoints.update([row.waypoint1, row.waypoint2])


#适度值评估函数
#评估可行解
def comput_fitness(solution):
    """
        comput_fitness()
        返回特定解的fitness,此处fitness设置为total distance
        遗传算法更加亲睐距离更短的solution
    """
    solution_fitness = 0.0
    for index in range(len(solution)):
        waypoint1 = solution[index - 1]
        waypoint2 = solution[index]
        solution_fitness += waypoint_distance[frozenset([waypoint1, waypoint2])]
    return solution_fitness

def generate_random_agent():
    """
    生成随机solution
    """
    new_random_agent = list(all_waypoints)
    random.shuffle(new_random_agent)
    return tuple(new_random_agent)

#交叉运算规则
def mutate_agent(agent_genome, max_mutations = 3):
    agent_genome = list(agent_genome)
    num_mutations = random.randint(1, max_mutations)

    for mutation in range(num_mutations):
        swap_index1 = random.randint(0, len(agent_genome) - 1)
        swap_index2 = swap_index1
        #单点交换，确保交换基因位置不同，随机1-3次
        while swap_index1 == swap_index2:
            swap_index2 = random.randint(0, len(agent_genome) - 1)
        agent_genome[swap_index1], agent_genome[swap_index2] = agent_genome[swap_index2], agent_genome[swap_index1]
    return tuple(agent_genome)

def shuffle_mutation(agent_genome):
    """
        Applies a single shuffle mutation to the given road trip.

        A shuffle mutation takes a random sub-section of the road trip
        and moves it to another location in the road trip.
    """

    agent_genome = list(agent_genome)

    start_index = random.randint(0, len(agent_genome) - 1)
    length = random.randint(2, 20)
    #length ?= start_index 则不变异?
    genome_subset = agent_genome[start_index:start_index + length]
    agent_genome = agent_genome[:start_index] + agent_genome[start_index + length:]

    insert_index = random.randint(0, len(agent_genome) + len(genome_subset) - 1)
    agent_genome = agent_genome[:insert_index] + genome_subset + agent_genome[insert_index:]

    return tuple(agent_genome)