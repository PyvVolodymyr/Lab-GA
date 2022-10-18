import math
import random
import numpy
import time


# Тестові функції для оптимізації
def bukin6(x, y):
    return 100 * math.sqrt(abs(y - 0.01 * x * x)) + 0.01 * abs(x + 10)


def matias(x, y):
    return 0.26 * (x * x + y * y) - 0.48 * x * y


def shaffer2(x, y):
    return 0.5 + (math.sin(x * x - y * y) ** 2 - 0.5) / (1 + 0.001 * (x * x + y * y)) ** 2


# Початкова популяція
population = [[]] * 20
for i in range(len(population)):
    population[i] = [random.randint(-15, -5), random.randint(-3, 3)]


# Приведення до бінарного вигляду
def to_binary(n):
    n = bin(n)

    if n[0] == '-':
        n = n[3:]
        if len(n) // 8 == 0:
            n = '0' * (8 - len(n)) + n
        elif len(n) % 8 != 0:
            while len(n) % 8 != 0:
                n = '0' + n
        return '-' + n
    else:
        n = n[2:]
        if len(n) // 8 == 0:
            n = '0' * (8 - len(n)) + n
        elif len(n) % 8 != 0:
            while len(n) % 8 != 0:
                n = '0' + n
        return n


def crossover(first, second):
    parent1 = parent2 = [[], []]
    parent1[0] = to_binary(first[0])
    parent1[1] = to_binary(first[1])
    parent2[0] = to_binary(second[0])
    parent2[1] = to_binary(second[1])

    child1 = child2 = [[], []]
    child1[0] = parent1[0][:-4] + parent2[0][-4:]
    child1[1] = parent1[1][:-4] + parent2[1][-4:]

    child2[0] = parent2[0][:-4] + parent1[0][-4:]
    child2[1] = parent2[1][:-4] + parent1[1][-4:]

    child1 = [int(child1[0], 2), int(child1[1], 2)]
    child2 = [int(child2[0], 2), int(child2[1], 2)]

    return child1, child2


def mutation(ind):
    r = random.randint(0, 15)
    result = [list(to_binary(ind[0])), list(to_binary(ind[1]))]

    if r <= 7:
        if result[0][-r] == '0':
            result[0][-r] = '1'
        else:
            result[0][-r] = '0'
    else:
        r -= 8
        if result[1][-r] == '0':
            result[1][-r] = '1'
        else:
            result[1][-r] = '0'

    result[0] = int(''.join(result[0]), 2)
    result[1] = int(''.join(result[1]), 2)

    try:
        if result[0] <= -15 or result[0] >= -5 or result[1] <= -3 or result[1] >= 3:
            result = mutation(ind)
    except Exception as ex:
        print('Mutation failed', ex)
        return ind

    return result


start_time = time.time()
for i in range(100000):
    fullfit = 0
    for j in range(len(population)):
        fullfit += bukin6(population[0][0], population[0][1])
    fullfit /= len(population)
    print(i, population, '\nFullfit:', fullfit, '\n')

    population.sort(key=lambda a: bukin6(a[0], a[1]))

    new_population = []
    for j in range(0, len(population), 2):
        new_ind = crossover(population[j], population[j + 1])
        new_population.append(new_ind[0])
        if len(new_population) >= len(population):
            break
        new_population.append(new_ind[1])
        if len(new_population) >= len(population):
            break
        new_population.append(population[j])
        if len(new_population) >= len(population):
            break
        new_population.append(population[j + 1])
        if len(new_population) >= len(population):
            break

    mutation_chance = random.randint(1, 100)
    if mutation_chance <= 20:
        random_ind = random.randint(0, len(new_population) - 1)
        print('Start:', random_ind, new_population[random_ind], bukin6(new_population[random_ind][0], new_population[random_ind][1]), '\n', new_population)
        new_population[random_ind] = mutation(new_population[random_ind])
        print('Mutation:', random_ind, new_population[random_ind], bukin6(new_population[random_ind][0], new_population[random_ind][1]))

    population = new_population


print("Time: %s seconds" % (time.time() - start_time))

