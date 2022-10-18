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


# Початкова популяція
B = [[]] * 100
for i in range(100):
    t = []
    t.append(to_binary(random.randint(-15, -5)))
    t.append(to_binary(random.randint(-3, 3)))
    B[i] = t


def crossover(first, second):
    return [[first[0], second[1]], [second[0], first[1]]]


def mutation(ind):
    print('-------------------------------------------------------------mutation------------------------------------')
    r = random.randint(0, 15)
    result = [[], []]

    if r >= 8:
        r -= 8
        temp = list(ind[1])
        if temp[r] == '0':
            temp[r] = '1'
        else:
            temp[r] = '0'
        result[0] = ind[0]
        result[1] = ''.join(temp)
        if int(''.join(temp), 2) < -3 or int(''.join(temp), 2) > 3:
            return mutation(ind)
    else:
        temp = list(ind[0])
        if temp[r] == '0':
            temp[r] = '1'
        else:
            temp[r] = '0'
        result[0] = ''.join(temp)
        result[1] = ind[1]
        if int(''.join(temp), 2) < -15 or int(''.join(temp), 2) > -5:
            return mutation(ind)

    return result


def invers(ind):
    r = random.randint(0, 1)
    ind[r] = ind[r][::-1]
    return ind


fit = [0 for i in range(len(B))]
population = [i for i in B]


def search_min(fit):
    min_index1 = fit.index(min(fit))
    temp = min(fit)
    fit[min_index1] = max(fit)
    min_index2 = fit.index(min(fit))
    fit[min_index1] = temp
    return [min_index1, min_index2]


def search_max(fit):
    max_index1 = fit.index(max(fit))
    temp = max(fit)
    fit[max_index1] = min(fit)
    max_index2 = fit.index(max(fit))
    fit[max_index1] = temp
    return [max_index1, max_index2]


start_time = time.time()
for i in range(1):
    fullfit = 0
    for j in range(len(B)):
        # fit[j] = matias(int(population[j][0], 2), int(population[j][1], 2))
        # fit[j] = shaffer2(int(population[j][0], 2), int(population[j][1], 2))
        fit[j] = bukin6(int(population[j][0], 2), int(population[j][1], 2))
        fullfit += fit[j]

    fullfit /= len(B)

    # Для мінімізації
    best1, best2 = search_min(fit)
    worst1, worst2 = search_max(fit)
    # Для максимізації
    # best1, best2 = search_max(fit)
    # worst1, worst2 = search_min(fit)

    # print(i, 'Fullfit:', fullfit, '\nBest:', population[best1], population[best2],
    #       matias(int(population[best1][0], 2), int(population[best1][1], 2)), '\nWorst:', population[worst1],
    #       population[worst2], matias(int(population[worst1][0], 2), int(population[worst1][1], 2)), '\n')
    # print(i, 'Fullfit:', fullfit, '\nBest:', population[best1], population[best2],
    #       shaffer2(int(population[best1][0], 2), int(population[best1][1], 2)), '\nWorst:', population[worst1],
    #       population[worst2], shaffer2(int(population[worst1][0], 2), int(population[worst1][1], 2)), '\n')
    print(i, 'Fullfit:', fullfit, '\nBest:', population[best1], population[best2],
          bukin6(int(population[best1][0], 2), int(population[best1][1], 2)), '\nWorst:', population[worst1],
          population[worst2], bukin6(int(population[worst1][0], 2), int(population[worst1][1], 2)), '\n')

    population.sort(key=bukin6)
    new_individs = crossover(population[best1], population[best2])

    temp = random.randint(1, 2000)
    if temp <= 10:
        new_individs[0] = mutation(new_individs[0])
    elif temp >= 1991:
        new_individs[1] = mutation(new_individs[1])
    temp = random.randint(1, 100)
    if temp <= 0:
        new_individs[0] = invers(new_individs[0])
    elif temp >= 101:
        new_individs[1] = invers(new_individs[1])

    population[worst1] = new_individs[0]
    population[worst2] = new_individs[1]

    if fullfit == 0:
        break

print("Time: %s seconds" % (time.time() - start_time))
