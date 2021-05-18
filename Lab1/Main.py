import math
import numpy as np
import time

from corpus import get_dict
from metrics import Metrics


def dist_hemming(seq1, seq2):
    if seq1 == seq2:
        return 0
    ml = max(len(seq1), len(seq2))
    ml_check = seq1.ljust(ml)
    ml_word = seq2.ljust(ml)
    dist = 0
    for i in range(ml):
        if ml_check[i] != ml_word[i]:
            dist = dist + 1
    return dist


def alg_hemming(check, dictionary, min_percentage):
    nested_list = []
    dist_list = []
    for word in dictionary:
        dist = dist_hemming(check, word)
        nested_list.append({'word': word, 'dist': dist})
        dist_list.append(dist)

    max_dist = max(nested_list, key=lambda x: x['dist'])['dist']
    for i in range(len(nested_list)):
        nested_list[i]['percentage'] = round(100 * (max_dist - nested_list[i]['dist']) / max_dist, 2)

    sorted_list = sorted(nested_list, key=lambda x: x['percentage'], reverse=True)
    if min_percentage is None:
        return sorted_list
    filter_list = filter(lambda x: x['percentage'] >= min_percentage, sorted_list)
    result_list = list(filter_list)
    return result_list, Metrics.get_mse(dist_list, result_list[0]['dist']), Metrics.get_std(dist_list)


def dist_jaro(seq1, seq2):
    if seq1 == seq2:
        return 1

    ml = max(len(seq1), len(seq2))
    seq1 = seq1.ljust(ml)
    seq2 = seq2.ljust(ml)

    len1 = len(seq1)
    len2 = len(seq2)

    h = math.floor(max(len1, len2) / 2 - 1)
    m = 0

    hash_s1 = [0] * len1
    hash_s2 = [0] * len2

    for i in range(len1):
        for j in range(max(0, i - h), min(len2, i + h + 1)):
            if seq1[i] == seq2[j] and hash_s2[j] == 0:
                hash_s1[i] = 1
                hash_s2[j] = 1
                m += 1
                break

    if m == 0:
        return 0

    t = 0
    point = 0

    for i in range(len1):
        if hash_s1[i]:
            while hash_s2[point] == 0:
                point += 1
            if seq1[i] != seq2[point]:
                point += 1
                t += 1
    t = t // 2

    return (m / len1 + m / len2 + (m - t + 1) / m) / 3


def alg_jaro(check, dictionary, min_percentage):
    nested_list = []
    dist_list = []
    for word in dictionary:
        dist = dist_jaro(check, word)
        nested_list.append({'word': word, 'dist': dist})
        dist_list.append(dist)
    for i in range(len(nested_list)):
        nested_list[i]['percentage'] = round(100 * nested_list[i]['dist'], 2)

    sorted_list = sorted(nested_list, key=lambda x: x['percentage'], reverse=True)
    if min_percentage is None:
        return sorted_list
    filter_list = filter(lambda x: x['percentage'] >= min_percentage, sorted_list)
    result_list = list(filter_list)
    return result_list, Metrics.get_mse(dist_list, result_list[0]['dist']), Metrics.get_std(dist_list)


def dist_levenshtein(seq1, seq2):
    if seq1 == seq2:
        return 0
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros((size_x, size_y))
    for x in range(size_x):
        matrix[x, 0] = x
    for y in range(size_y):
        matrix[0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x - 1] == seq2[y - 1]:
                matrix[x, y] = min(matrix[x - 1, y] + 1, matrix[x - 1, y - 1], matrix[x, y - 1] + 1)
            else:
                matrix[x, y] = min(matrix[x - 1, y] + 1, matrix[x - 1, y - 1] + 1, matrix[x, y - 1] + 1)
    # print(matrix)
    return matrix[size_x - 1, size_y - 1]


def alg_levenshtein(check, dictionary, min_percentage):
    nested_list = []
    dist_list = []
    for word in dictionary:
        dist = dist_levenshtein(check, word)
        nested_list.append({'word': word, 'dist': dist})
        dist_list.append(dist)

    max_dist = max(nested_list, key=lambda x: x['dist'])['dist']
    for i in range(len(nested_list)):
        nested_list[i]['percentage'] = round(100 * (max_dist - nested_list[i]['dist']) / max_dist, 2)

    sorted_list = sorted(nested_list, key=lambda x: x['percentage'], reverse=True)
    if min_percentage is None:
        return sorted_list
    filter_list = filter(lambda x: x['percentage'] >= min_percentage, sorted_list)
    result_list = list(filter_list)
    return result_list, Metrics.get_mse(dist_list, result_list[0]['dist']), Metrics.get_std(dist_list)


dict = get_dict()
print("Число слов в словаре:", len(dict))
print("Метрики: Среднеквадратическая ошибка (чем ближе к 0 тем лучше модель), Среднеквадратическое отклонение")

check_word = "вместо"

print("Проверяем слово:", check_word, "\n")

print("Алгоритм Хемминга:")
start_time = time.time()
result, mse, std = alg_hemming(check_word, dict, 90)
print("Время выполнения:", round(time.time() - start_time, 3), "сек.")
print("Среднеквадратическая ошибка:", mse)
print("Среднеквадратическое отклонение:", std)
for r in result:
    print(r)

print("\n")

print("Алгоритм Джаро:")
start_time = time.time()
result, mse, std = alg_jaro(check_word, dict, 80)
print("Время выполнения:", round(time.time() - start_time, 3), "сек.")
print("Среднеквадратическая ошибка:", mse)
print("Среднеквадратическое отклонение:", std)
for r in result:
    print(r)

print("\n")

print("Алгоритм Левенштейна:")
start_time = time.time()
result, mse, std = alg_levenshtein(check_word, dict, 90)
print("Время выполнения:", round(time.time() - start_time, 3), "сек.")
print("Среднеквадратическая ошибка:", mse)
print("Среднеквадратическое отклонение:", std)
for r in result:
    print(r)
