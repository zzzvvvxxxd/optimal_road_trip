#! /usr/bin/env python2.7
# coding=utf-8
__author__ = 'bulu_dog'

"""
article:
    http://www.randalolson.com/2015/03/08/computing-the-optimal-road-trip-across-the-u-s/
    http://blog.chinaunix.net/uid-27105712-id-3886077.html
"""
from itertools import combinations
import pandas as pd
import pickle as pl
import numpy as np
import random
import time
import csv
from select_util import topN, round_robin

waypoint_distances = {}
all_waypoints = set()

#"""
#TSP-point.csv
city = []
waypoint_data = pd.read_csv("../data/TSP-point.csv", sep=",")
for i, row in waypoint_data.iterrows():
    all_waypoints.update([row.city])
    for j, _row in waypoint_data.iterrows():
        waypoint_distances[frozenset([row.city, _row.city])] = ((row.x - _row.x)**2 + (row.y - _row.y)**2)**0.5
#"""

"""
#Google Map data
waypoint_data = pd.read_csv("../data/my-waypoints-dist-dur.tsv", sep="\t")

for i, row in waypoint_data.iterrows():
    waypoint_distances[frozenset([row.waypoint1, row.waypoint2])] = row.distance_m
    #waypoint_durations[frozenset([row.waypoint1, row.waypoint2])] = row.duration_s
    all_waypoints.update([row.waypoint1, row.waypoint2])
"""

#适度值评估函数
#评估可行解
def compute_fitness(solution):
    """
        comput_fitness()
        返回特定解的fitness,此处fitness设置为total distance
        遗传算法更加亲睐距离更短的solution
    """
    solution_fitness = 0.0
    for index in range(len(solution)):
        waypoint1 = solution[index - 1]
        waypoint2 = solution[index]
        solution_fitness += waypoint_distances[frozenset([waypoint1, waypoint2])]
    return solution_fitness

def generate_random_agent():
    """
    生成随机solution
    shuffle(all_waypoints)
    """
    new_random_agent = list(all_waypoints)
    random.shuffle(new_random_agent)
    return tuple(new_random_agent)

#变异规则1
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

#变异规则2
def shuffle_mutation(agent_genome):
    agent_genome = list(agent_genome)

    start_index = random.randint(0, len(agent_genome) - 1)
    length = random.randint(2, 20)
    genome_subset = agent_genome[start_index:start_index + length]
    agent_genome = agent_genome[:start_index] + agent_genome[start_index + length:]

    insert_index = random.randint(0, len(agent_genome) + len(genome_subset) - 1)
    agent_genome = agent_genome[:insert_index] + genome_subset + agent_genome[insert_index:]

    return tuple(agent_genome)


def generate_random_population(pop_size):
    random_population = []
    for agent in range(pop_size):
        random_population.append(generate_random_agent())
    return random_population


def run_genetic_algorithm(generations=5000, population_size=100, selector = topN):
    """
        Genetic Algorithm.
    """
    population = generate_random_population(population_size)
    for generation in range(generations):
        #计算该generation的fitness
        population_fitness = {}
        for agent_genome in population:          #会有重复
            if agent_genome in population_fitness:
                continue
            population_fitness[agent_genome] = compute_fitness(agent_genome)

        #top 10
        new_population = []
        for rank, agent_genome in selector(population_fitness, N=100):
            if (generation % 1000 == 0 or generation == generations - 1) and rank == 0:
                print "Generation %d best: %d | Unique genomes: %d" % (generation,
                                                                       population_fitness[agent_genome],
                                                                       len(population_fitness))
                print agent_genome

            #append到new population，然后用这10个seeds，generate出90个后代
            new_population.append(agent_genome)

            #单点变异 -> 2 offspring
            for offspring in range(2):
                new_population.append(mutate_agent(agent_genome, 3))
            #两点变异 -> 7 offspring
            for offspring in range(7):
                new_population.append(shuffle_mutation(agent_genome))


        #for i in range(len(population))[::-1]:
            #del population[i]
        population = new_population
        #print population

start = time.time()
run_genetic_algorithm(generations=5000, population_size=1000, selector=round_robin)
end = time.time()
print end - start
