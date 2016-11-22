#!/usr/bin/env python3

import random
from operator import itemgetter
from matplotlib import pyplot as plt
import sys


class GeneticAlgorithm(object):
    def __init__(self, genetics):
        self.genetics = genetics
        pass

    def run(self):
        """
        Run method represents core of genetic algorithm :
        randomly initialize population(t)
        determine fitness of population(t)
        repeat
            select parents from population(t)
            perform crossover on parents creating population(t+1)
            perform mutation of population(t+1)
            determine fitness of population(t+1)
            until best individual is good enough
        :return:
        """
        population = self.genetics.get_initial_population()
        while True:
            # calculate fitness for every individual
            # generate tuple[ fitness , list_individual] and create list for population
            fitness_population = [(self.genetics.fitness(ch),  ch) for ch in population]
            if self.genetics.check_stop(fitness_population):
                self.genetics.plot_result()
                break
            population = self.next_population(fitness_population)
        return population

    def next_population(self, fits):
        parents_generator = self.genetics.parents(fits)
        size = len(fits)
        next_pop_l = []
        save_best = self.genetics.save_best

        # save best of previous population ( as professor sad save the einstein )
        sorted_fits = sorted(fits, key=itemgetter(0))
        for i in range(1, save_best+1):
            next_pop_l.append(sorted_fits[-i][1])

        while len(next_pop_l) < size:
            parents = next(parents_generator)
            cross = random.random() < self.genetics.get_probability_crossover()
            children = self.genetics.crossover(parents) if cross else parents
            if random.random() < self.genetics.get_probability_mutation():
                for ch in children:
                    mutate = random.random() < self.genetics.get_probability_mutation()
                    next_pop_l.append(self.genetics.mutation(ch) if mutate else ch)
                    pass
                pass
            pass
        return next_pop_l[0:size]
        pass
    pass


class GuessText:
    def __init__(self, target_text, limit=1000, size=250, prob_crossover=0.9, prob_mutation=0.1, save_best=5):
        """
        :param target_text:     text that algorithm should guess
        :param limit:           how many generations should be
        :param size:            size of population
        :param prob_crossover:  probability of crossover
        :param prob_mutation:   probability of mutation
        """
        self.target = self.text2chromo(target_text)
        self.counter = 0

        self.limit = limit
        self.size = size
        self.prob_crossover = prob_crossover
        self.prob_mutation = prob_mutation
        self.save_best = save_best

        self.fitness_best = []
        self.fitness_worst = []
        self.fitness_average = []
        # pass

    def get_probability_crossover(self):
        return self.prob_crossover

    def get_probability_mutation(self):
        return self.prob_mutation

    def get_initial_population(self):
        # generate initial population, returns list of self.size
        return [self.random_chromo() for j in range(self.size)]

    def fitness(self, chromo):
        # larger is better, matched == 0
        return -sum(abs(c - t) for c, t in zip(chromo, self.target))

    def check_stop(self, fits_populations):
        self.counter += 1

        best_match = list(sorted(fits_populations))[-1]
        best_fitness = best_match[0]
        best_individual = best_match[1]

        fits = [f for f, ch in fits_populations]

        best = max(fits)
        worst = min(fits)
        average = sum(fits) / len(fits)

        if self.counter % 1 == 0:
           
            self.fitness_best.append((self.counter, best))
            self.fitness_worst.append((self.counter,  worst))
            self.fitness_average.append((self.counter, average))

            if self.counter % 10 == 0:
                print("[G %3d] score=(%4d, %4d, %4d): %r" % (self.counter, best, average, worst, self.chromo2text(best_individual)))
                pass
            pass

        if best_fitness == 0:
            print("[G %3d] score=(%4d, %4d, %4d): %r" % (self.counter, best, average, worst, self.chromo2text(best_individual)))
            return True
        return self.counter >= self.limit

    def parents(self, fits_populations):
        while True:
            best_1 = self.tournament(fits_populations)
            best_2 = self.tournament(fits_populations)
            yield (best_1, best_2)
            pass
        pass

    def tournament(self, fits_populations):
        rand_1_fitness, rand_1 = self.select_random(fits_populations)
        rand_2_fitness, rand_2 = self.select_random(fits_populations)
        if rand_1_fitness > rand_2_fitness:
            return rand_1
        else:
            return rand_2

    def crossover(self, parents):
        parent1, parent2 = parents

        index1 = random.randint(1, len(self.target) - 2)
        index2 = random.randint(1, len(self.target) - 2)

        if index1 > index2:
            index1, index2 = index2, index1

        child1 = parent1[:index1] + parent2[index1:index2] + parent1[index2:]
        child2 = parent2[:index1] + parent1[index1:index2] + parent2[index2:]

        return child1, child2

    def mutation(self, chromosome):
        index = random.randint(0, len(self.target) - 1)
        vary = random.randint(-5, 5)
        mutated = list(chromosome)
        mutated[index] += vary
        return mutated

    def select_random(self, fits_populations):
        return fits_populations[random.randint(0, len(fits_populations) - 1)]

    def text2chromo(self, text):
        return [ord(ch) for ch in text]

    def chromo2text(self, chromo):
        return "".join(chr(max(1, min(ch, 255))) for ch in chromo)

    def random_chromo(self):
        return [random.randint(1, 255) for i in range(len(self.target))]

    def plot_result(self):
        points = [f for f, ch in self.fitness_best]
        fitness_best = [seq[1] for seq in self.fitness_best]
        fitness_worst = [seq[1] for seq in self.fitness_worst]
        fitness_average = [seq[1] for seq in self.fitness_average]

        plt.plot(points, fitness_best, color='g', label='Best')
        plt.plot(points, fitness_average, linestyle='--', color='b', label='Average')
        plt.plot(points, fitness_worst, color='r', label='Worst')

        plt.xlabel("Population")
        plt.ylabel("distance from optimum")
        plt.title('Genetic Algorithm')

        plt.legend()
        plt.show()
        pass
    pass

if __name__ == "__main__":

    target_text = "Hello world"
    limit = 1000
    size = 250
    prob_crossover = 0.9
    prob_mutation = 0.1
    save_best = 5

    if len(sys.argv) > 1:
        target_text = sys.argv[1]
        pass

    GeneticAlgorithm(GuessText(target_text, limit, size, prob_crossover, prob_mutation, save_best)).run()
    pass
