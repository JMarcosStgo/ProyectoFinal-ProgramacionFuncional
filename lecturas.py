
import csv
from typing import Any, Callable, Generator


def read_csv1(name_file: str) -> Callable:
    def value_return(n: int) -> Generator:
        with open(name_file, encoding='utf-8') as file_csv:
            data = csv.reader(file_csv, delimiter=',')
            next(data)
            for line in data:
                if line[n] != '' and n == 4:
                    yield int(line[n])
                if line[n] != '' and n == 2 or n == 6:
                    yield line[n]
    return value_return


def read_csv2(name_file: str) -> Generator:
    with open(name_file, encoding='utf-8') as file_csv:
        data = csv.reader(file_csv, delimiter=',')
        next(data)
        for line in data:
            if line[9] != '':
                yield (line[0], int(line[9]))


def read_csv_tuple(name_file: str) -> Generator:
    with open(name_file, encoding='utf-8') as file_csv:
        data = csv.reader(file_csv, delimiter=',')
        next(data)
        for line in data:
            if line[4] != '':
                yield (line[0], int(line[4]))


def read_csv3(name_file: str) -> Generator:
    with open(name_file, encoding='utf-8') as file_csv:
        data = csv.reader(file_csv, delimiter=',')
        next(data)
        for line in data:
            if line[1] != '':
                yield line[1].split('.')[1]


def read_stop_words(x: str) -> list:
    return [line.rstrip() for line in open(x, "r", encoding='utf-8')]


def read_csv5(stop_words: list) -> Generator:
    with open('companies2.csv', encoding='utf-8') as file_csv:
        data = csv.reader(file_csv, delimiter=',')
        next(data)
        for line in data:
            if line[0] != '':
                yield filter(lambda x: x not in stop_words, line[0].split(" "))


def composite_function(f, g):
    return lambda x: f(g(x))


def read_csv_monada(name_file: str) -> dict:
    list_data = dict()
    with open(name_file, encoding='utf-8') as file_csv:
        data = csv.reader(file_csv, delimiter=',')
        headers = next(data)
        for x in data:
            iterador = *zip(headers, x),
            list_data[iterador[0][1]] = iterador[1:]
    return list_data


def read_csv_set(name_file: str) -> list:
    list_data = list()
    with open(name_file, encoding='utf-8') as file_csv:
        data = csv.reader(file_csv, delimiter=',')
        headers = next(data)
        for x in data:
            iterador = *zip(headers, x),
            list_data.append({key: value for key, value in iterador})
    return list_data
