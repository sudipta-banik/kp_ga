import random

import numpy as np


class Cell:
    def __init__(self, benefit=0, volume=0):
        self.benefit = benefit
        self.volume = volume


sack_volume = 995
number_of_items = 100
# Cell { Benefit , Volume }
items = []

fl = open("dataset.txt", "r")
while 1:
    line = fl.readline()
    if not line:
        break
    line = line.split()

    # print(line)
    items.append(Cell(int(line[0]), int(line[1])))


def random_in_range(left, right):
    return int((right - left) * random.random() + left)


def get_random_bit():
    x = [1, 0]
    return random.choice(x)
    # return np.floor(np.random.random() * 2)


def get_gnome(length):
    return [get_random_bit() for _ in range(length)]


def random_mutated_copy(_gnome):
    x = np.copy(_gnome.chromosome)
    for _ in range(int(0.15 * number_of_items)):
        p = int(random.random() * len(x))
        x[p] = 1 - x[p]
    return Gnome(x)


def crossover(parent1, parent2):
    pr1 = int(np.floor(random.random() * number_of_items))
    pr2 = int(np.floor(random.random() * number_of_items))
    if pr2 == pr1:
        if pr2 < number_of_items - 1:
            pr2 += 1
        elif pr2 > 0:
            pr2 -= 1
    x = random.random() * 2
    child_chromosome1 = []
    child_chromosome2 = []

    child_chromosome1[:pr1] = parent1.chromosome[:pr1]
    child_chromosome1[pr1:pr2] = parent2.chromosome[pr1:pr2]
    child_chromosome1[pr2:] = parent1.chromosome[pr2:]

    child_chromosome2[:pr1] = parent2.chromosome[:pr1]
    child_chromosome2[pr1:pr2] = parent1.chromosome[pr1:pr2]
    child_chromosome2[pr2:] = parent2.chromosome[pr2:]
    return Gnome(child_chromosome1), Gnome(child_chromosome2)


def calc_vol(_gnome):
    vol = 0
    chrmsm = _gnome.chromosome
    for i in range(number_of_items):
        if chrmsm[i] == 1:
            vol += items[i].volume
    return vol


def calc_fitness(chromosome):
    length = number_of_items
    gnome_fitness = 0
    satisfied = False

    while not satisfied:
        gnome_fitness = 0
        gnome_volume = 0
        for i, isSet in zip(range(number_of_items), chromosome):
            if isSet == 1:
                gnome_fitness += items[i].benefit
                gnome_volume += items[i].volume
        if gnome_volume <= sack_volume:
            satisfied = True
        else:
            p = 0
            while chromosome[p] == 0:
                p = int(random.random() * length) % length
            chromosome[p] = 0

    return gnome_fitness


class Gnome:
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = calc_fitness(chromosome)


if __name__ == '__main__':

    print(number_of_items)

    population_size = 400

    generation = 0

    population = []
    [population.append(Gnome(get_gnome(number_of_items))) for _ in range(population_size)]
    genx = int(input("Enter Generations to iterate "))

    # trying to get rid of local optimum
    stuck_local = 0
    stuck_global = 0

    pre_fitness = population[0].fitness

    while generation < int(genx):
        population = sorted(population, key=lambda x: x.fitness, reverse=True)

        new_generation = []
        # top_10% are elite ones
        s = int((population_size * 0.1))
        new_generation.extend(population[:s])

        # crossover
        s = int((0.3 * population_size))
        for _ in range(s):
            new_generation.extend(crossover(population[random_in_range(0, population_size / 2)],
                                            population[random_in_range(population_size / 2, population_size - 1)]))

        s = int((population_size * 0.15))
        for z in range(s):
            new_generation.append(random_mutated_copy(population[z]))
            new_generation.append(random_mutated_copy(population[population_size - 1 - z]))

        population = new_generation

        if population[0].fitness == pre_fitness:
            stuck_local += 1
            # stuck_global +=1
            if stuck_local == 5:
                stuck_local = 0
                population.append(random_mutated_copy(population[0]))
                population.pop(0)
        pre_fitness = population[0].fitness

        generation += 1
        print("generation_", generation, population[0].fitness, "volume ", calc_vol(population[0]))
