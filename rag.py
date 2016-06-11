#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import random
import math
import time
import pp


# Wypisuje instrukcję do programu
def usage():
    with open('usage.txt') as f:
        read_data = f.read()
    f.close()
    print(read_data)


# Przygotowuje parametry wejściowe do uruchomienia programu
# TODO: usunąć standardowe parametry
def parse_parameters():
    parser = argparse.ArgumentParser()
    # wymagane argumenty
    parser.add_argument('-f', type=str, choices=["f1", "f2"], help="funkcja: f1 albo f2")
    parser.add_argument('-o', type=int, default=20, help="liczba osobników > 0")
    parser.add_argument('-p', type=int, default=10, help="liczba pokoleń > 0")
    parser.add_argument('-w', type=str, default="wlp", choices=["wlp", "wlr", "wd"], help="sposób wyboru: wlp, wlr, wd")
    parser.add_argument("-m", type=float, default=0.25, help="współczynnik mutacji <0,1>")
    parser.add_argument("-k", type=float, default=0.25, help="współczynnik krzyżowania <0,1>")
    parser.add_argument("-t", type=int, default=1, help="liczba wątków")
    parser.add_argument("-x", type=str, default=None, help="serwer np: 192.169.0.1:1234")
    # opcjonalne argumenty
    parser.add_argument('-s', type=str, choices=["lin", "pot", "log"], help="sposób skalowania: lin, pot, log")
    parser.add_argument('-n', type=str, help="nazwa pliku do zapisania informacji o przebiegu generacji")
    return parser.parse_args()


# Wylosuj osobnika
def rand_specimen(f):
    if f == 'f1' or f == 'f2':
        a = random.uniform(0, 1)
        b = random.uniform(0, 1)
        c = random.uniform(0, 1)
        return [a, b, c]


# Skaluje liczbę <0,1> do <min,max>
def scale(number, minimum, maximum):
    return number * (maximum - minimum) + minimum


# Skalowanie jednego osobnika
def scale_specimen(specimen, scale_min, scale_max):
    scaled_specimen = [None] * len(specimen)
    for i in range(len(specimen)):
        scaled_specimen[i] = scale(specimen[i], scale_min[i], scale_max[i])
    return scaled_specimen


# Zwróć dolne granice argumentów funkcji
def get_scale_min(f):
    if f == 'f1':
        return [-5, -15, 10]
    if f == 'f2':
        return [-5, -2, -3]


# Zwróć górne granice argumentów funkcji
def get_scale_max(f):
    if f == 'f1':
        return [10, 18, 7]
    if f == 'f2':
        return [10, 4, 7]


# Oblicza funkcję celu
def objective_function(f_args, f, scale_min, scale_max):
    time.sleep(0.01)
    if f == "f1":
        a = scale(f_args[0], scale_min[0], scale_max[0])
        b = scale(f_args[1], scale_min[1], scale_max[1])
        c = scale(f_args[2], scale_min[2], scale_max[2])
        return 4 * a + 6 * c - 15 * pow(a, 2) - 20 * pow(b, 2) - 6 * pow(a, 3) - 70
    if f == "f2":
        a = scale(f_args[0], scale_min[0], scale_max[0])
        b = scale(f_args[1], scale_min[1], scale_max[1])
        c = scale(f_args[2], scale_min[2], scale_max[2])
        return 4 * math.cos(a) + 6 * math.cos(c) - 20 * pow(b, 2) + 3 * pow(a, 3) - 70


# Oblicza wyniki (funkcję celu) dla osobników. (Przetwarzanie równoległe)
def calculate_results_parallel(specimens, args, scale_min, scale_max):
    res = [None] * args.o

    if args.x is None:
        ppservers = ()
    else:
        ppservers = (args.x,)
    job_server = pp.Server(args.t, ppservers=ppservers)

    jobs = []
    for i in range(len(res)):
        jobs.append(
            job_server.submit(objective_function, (specimens[i], args.f, scale_min, scale_max),
                              (scale,), ('math', 'time',)))

    i = 0
    for job in jobs:
        res[i] = job()
        i += 1

    return res


# Oblicza wyniki (funkcję celu) dla osobników. (bez przetwarzania równoległego)
def calculate_results(specimens, args, scale_min, scale_max):
    res = [None] * arguments.o
    for actual_specimen in range(len(res)):
                res[actual_specimen] = objective_function(specimens[actual_specimen], args.f, scale_min, scale_max)
    return res


# obliczenie wyników przystosowania
def calculate_adaptation_function(results, minimum):
    for i in range(len(results)):
        results[i] = results[i] - minimum - 0.5 * minimum
    return results


# przeskaluj wyniki
def calculate_scale_function(args, results):
    if args.s is "lin":
        multiplying_factor = 1.5
        average = sum(results) / float(len(results))
        maximum = max(results)
        minimum = min(results)
        if minimum > (multiplying_factor * average - maximum)/(multiplying_factor - 1):
            a = ((multiplying_factor - 1) * average) / (maximum - average)
            b = average * ((maximum - multiplying_factor * average)/(maximum - average))
        else:
            a = average / (average - minimum)
            b = -minimum * (average/(average - minimum))
        for i in range(len(results)):
            results[i] = a * results[i] + b
            return results
    if args.s is "pot": #TODO skalowanie potęgowe
        return results
    if args.s is "log": #TODO skalowanie logarytmiczne
        return results


# Uruchomienie programu
def main(args):

        start_time = time.time()

        # inicjacja pliku do zapisu
        if args.n is not None:
            write_file = open(args.n, 'w')
            write_file.write("Parametry wywołania: " + str(args))

        # przygotowanie danych
        specimens = [None] * args.o
        best_specimen = None
        best_result = None
        scale_min = get_scale_min(args.f)
        scale_max = get_scale_max(args.f)

        # losowanie osobników
        for actual_specimen in range(len(specimens)):
            specimens[actual_specimen] = rand_specimen(args.f)

        # właściwy algorytm genetyczny, pętla po pokoleniach
        for actual_generation in range(1, args.p + 1):
            if args.n is not None:
                write_file.write("\nPokolenie: " + str(actual_generation))

            # obliczam funkcję celu
            if args.t > 1 and args.x is not None:
                results = calculate_results_parallel(specimens, args, scale_min, scale_max)
            else:
                results = calculate_results(specimens, args, scale_min, scale_max)

            # najlepsze wyniki generacji
            best_generation_result = min(results)
            best_generation_specimen = specimens[results.index(best_generation_result)]

            if args.n is not None:
                write_file.write("\n\tNajlepszy osobnik w pokoleniu: {0}\n\tNajlepszy wynik w pokoleniu: {1}\n".format(
                    str(scale_specimen(best_generation_specimen, scale_min, scale_max)), best_generation_result))

            # dodaję do globalnie najlepszych, jeżeli są lepsze
            if best_result is None:
                best_result = best_generation_result
                best_specimen = best_generation_specimen
            elif best_result > best_generation_result:
                best_result = best_generation_result
                best_specimen = best_generation_specimen

            # oblicz na funkcję przystosowania
            results = calculate_adaptation_function(results, best_generation_result)

            # oblicz na funkcję skalowania
            if args.s is not None:
                results = calculate_scale_function(args, results)



        # wypisanie informacji dla ostatecznych wyników
        if args.n is not None:
            write_file.write("Wyniki\n")
            write_file.write("\tNajlepszy osobnik: {0}\n\tNajlepszy wynik: {1}\n".format(
                str(scale_specimen(best_specimen, scale_min, scale_max)), best_result))
            write_file.write("Czas przetwarzania: " + str(time.time() - start_time))
        else:
            print("Wyniki")
            print("\tNajlepszy osobnik: {0}\n\tNajlepszy wynik: {1}".format(
                str(scale_specimen(best_specimen, scale_min, scale_max)), best_result))
            print "Czas przetwarzania: ", time.time() - start_time


if __name__ == '__main__':
    arguments = parse_parameters()
    if arguments.f is None:
        usage()
    else:
        main(arguments)

