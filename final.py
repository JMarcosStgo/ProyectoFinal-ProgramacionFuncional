import csv
from ctypes import Union, cast
import functools
import math
import operator
import pprint
import random
import time
from typing import Any, Callable, Generator, Iterable, List, Mapping, Optional
import lecturas
from pymonad.tools import curry  # type: ignore
from oslash import Just, Nothing  # type: ignore


def exercise1(name_file: str) -> dict:
    """
        Cuál es la media actual de trabajadores de las empresas
    """
    data_generator = lecturas.read_csv1(name_file)(4)
    dictionary = {'promedio':  [0, 0]}
    while True:
        try:
            item_generator = next(data_generator)
            dictionary.update({'promedio': [
                              1+dictionary['promedio'][0], dictionary['promedio'][1]+item_generator]})
        except:
            break
    return dictionary


def exercise_tuplas(data: tuple) -> tuple:
    """
        obtener la empresa con más y menos trabajores y devolver el resultado en una tupla
    """
    min_ = min(data, key=lambda ele: ele[1])
    max_ = max(data, key=lambda ele: ele[1])
    return (("Empresa con menos trabajadores", {min_}), ("Empresa con más trabajadores", {max_}))


def exercise_tuplas_var(data: tuple) -> tuple:
    """
        Obtener la varianza de el numero de trabajadores de una muestra de x empresas, tomando la media calculada en el ejercicio anterior,
        retornar el resultado en una tupla
    """
    data_generator = *lecturas.read_csv_tuple(data[0]),
    muestra = random.sample(data_generator, data[2])
    res = map(lambda x: (x[1]-data[1])**2, muestra)
    var = functools.reduce(operator.add, res)/data[2]-1
    return ("El resultado de la varianza es", var)


def exercise2(name_file: str) -> list:
    """
        Encontrar las 10 empresas más actuales y antiguas desde su fundación
    """
    data_generator = lecturas.read_csv2(name_file)
    data_sort = sorted(data_generator, key=lambda year: year[1])
    return data_sort[len(data_sort)-10:] + data_sort[:10]
    # return functools.reduce(operator.add,sum(,[]))


def exercise3(name_file: str) -> dict:
    """
        Cuáles son los dominios web que más usan las empresas
    """
    data_generate = lecturas.read_csv3(name_file)
    dictionary = dict()
    for x in data_generate:
        if x not in dictionary:
            dictionary[x] = 1
        else:
            dictionary.update({x: dictionary[x]+1})
    dictionary_sorted = {key: value for key, value in sorted(
        dictionary.items(), key=lambda frecuencia: frecuencia[1], reverse=True)}
    return dictionary_sorted


def exercise4(name_file: str) -> dict:
    """
        las industrias con más empresas
    """
    data_generator = lecturas.read_csv1(name_file)(2)
    dictionary = dict()
    while True:
        try:
            insustry_data = next(data_generator)
            if insustry_data not in dictionary:
                dictionary[insustry_data] = 1
            else:
                dictionary.update(
                    {insustry_data: dictionary[insustry_data]+1})
        except:
            break
    return {key: value for key, value in sorted(dictionary.items(), key=lambda elemento: elemento[1], reverse=True)}


def exercise5(name_file_sw: str, min_frecuencia: int) -> dict:
    """
        Cuál es la palabra más repetida en el nombre de las compañías, con una frecuencia minima de n
    """
    composicion = lecturas.composite_function(
        lecturas.read_csv5, lecturas.read_stop_words)
    data_generator = composicion(name_file_sw)  # lecturas.read_csv5(name_file)
    dictionary = dict()
    while True:
        try:
            company_data = *next(data_generator),
            for item in company_data:
                if item not in dictionary:
                    dictionary[item] = 1
                else:
                    dictionary.update({item: dictionary[item]+1})
        except:
            break
    return {key: value for key, value in sorted(
        dictionary.items(), key=lambda elemento: elemento[1], reverse=True) if value > min_frecuencia}


def read_csv(name_file: str) -> Generator:
    with open(name_file, encoding="utf-8") as csvfile:
        data = csv.reader(csvfile, delimiter=',')
        headers = next(data)
        for x in data:
            yield zip(headers, x)


def CompaniesCountry(data: Generator) -> dict:
    """
        En qué país, región hay más empresas
    """
    coutrys = dict()
    for x in map(lambda x: (x[6][1]), filter(lambda x: len(x[6][1]) > 0, map(lambda x: [*x,], data))):
        if x not in coutrys:
            coutrys[x] = 1
        else:
            coutrys.update({x: 1 + coutrys.get(x)})
    return {key: val for key, val in sorted(coutrys.items(), key=lambda ele: ele[1], reverse=True)}


def Industry(data: Generator) -> dict:
    """
        Que industria tiene más empresas
    """
    industries = dict()
    for x in map(lambda x: (x[2][1]), filter(lambda x: len(x[2][1]) > 0, map(lambda x: [*x,], data))):
        if x not in industries:
            industries[x] = 1
        else:
            industries.update({x: 1 + industries.get(x)})
    industries = {key: val for key, val in sorted(
        industries.items(), key=lambda ele: ele[1], reverse=True)}
    return industries


def PercentIndustry(res4: dict, data: Generator) -> dict:
    """
        Porcentaje de empresas que pertenecen a cada industria
    """
    div = len(list(data))
    *map(lambda x: res4.update({x: operator.truediv((res4.get(x) * 100), div)}), res4),
    return res4


def CompaniesEmployers(data: Generator) -> None:
    """
        Encontrar la empresa más antigua y la más actual y comparar la cantidad de empleados 
    """
    industries = *map(lambda x: (x[0][1], x[4][1], x[9][1]), filter(
        lambda x: len(x[9][1]) > 0, map(lambda x: [*x,], data))),
    I1 = min(industries, key=lambda x: x[2])
    I2 = max(industries, key=lambda x: x[2])
    print(I1[0] + " es la compañia más antigua, fue fundada en el año",
          I1[2], "y cuenta con", I1[1], "empleados.")
    print("Por otro lado, " + I2[0] + " es la compañia más reciente, fundada en el año",
          I2[2], "con un número de empleados de", I2[1])


def MexicanCompanies(data: dict) -> None:
    """
        Cuántas compañias hay en México
    """
    print("En México existen", data['mexico'], "compañias")


def TecnologyCompanies(data: Generator) -> map:
    """
        Que empresas de tecnología hay en México para hacer un servicio social o prácticas profesionales.
    """
    mexicoComp = map(lambda x: (x[0][1], x[6][1], x[7][1]), filter(
        lambda x: x[6][1] == 'mexico' and x[2][1] == 'information technology and services', map(lambda x: [*x,], data)))
    return mexicoComp


@curry(2)
def exercise5_with_curry(name_file_sw: str, min_frecuencia: int) -> dict:
    """
        Cuál es la palabra más repetida en el nombre de las compañías, con una frecuencia minima de n
    """
    composicion = lecturas.composite_function(
        lecturas.read_csv5, lecturas.read_stop_words)
    data_generator = composicion(name_file_sw)  # lecturas.read_csv5(name_file)
    dictionary = dict()
    while True:
        try:
            company_data = *next(data_generator),
            for item in company_data:
                if item not in dictionary:
                    dictionary[item] = 1
                else:
                    dictionary.update({item: dictionary[item]+1})
        except:
            break
    return {key: value for key, value in sorted(
        dictionary.items(), key=lambda elemento: elemento[1], reverse=True) if value > min_frecuencia}


def exercise6(name_file: str) -> None:
    """
        Que posición ocupa México con respecto a la cantidad de empresas por país

    """
    data_generator = lecturas.read_csv1(name_file)(6)
    dictionary = {'': [0, 0]}
    while True:
        try:
            country_data = next(data_generator)
            if country_data not in dictionary:
                dictionary[country_data] = [
                    1, len(dictionary)]  # frecuencia-index
            else:
                dictionary.update({country_data: [dictionary[country_data][
                                  0]+1, dictionary[country_data][1]]})
        except:
            break
    print("México ocupa la posición número ", dictionary['mexico']
          [1], " con ", dictionary['mexico'][0], " empresas")


def exercise_monada(name_file: str, search_name: str) -> tuple:
    """
      Obtener los nombres de las empresas y realizar una busqueda de coincidencias, si encuentra coincidencias retorna la información
      de la empresa sino devuelve nothing
    """
    data = lecturas.read_csv_monada(name_file)
    half= lambda x: Just(x) if (x in data.keys()) else Nothing()
    res = half(search_name)
    if res == Nothing():
        return (res)
    else:
        return (res, data[search_name])


def exercise_funtor_app(var: tuple):
    """
        Obtener la desviación estándar de el ejercicio donde se obtiene la varianza de la cantidad de empleados
    """
    a = Just(var[1])
    f = Just(lambda x: math.sqrt(x))
    return f.apply(a)


def exercise_set1(name_file: str, country: str) -> set:
    """
        Obtener un conjunto del nombre de las empresas que sean de un pais
    """
    data = lecturas.read_csv_set(name_file)
    return {x['name'] for x in data if x['country'] == country}


def exercise_union(*set1: Any) -> set:
    """
        De n conjuntos de nombres de paises devolver un solo conjunto
    """
    return functools.reduce(set.union, set1)


def exercise_intersection(set1: set, set2: set) -> set:
    """
        Encontrar coincidecias de palabras en los nombres de las empresas de 2 paises
    """
    set1_data = map(lambda x: x.split(), set1)
    set2_data = map(lambda x: x.split(), set2)
    set2_data_sum: List[list]
    set1_data_sum: List[list]
    set1_data_sum = sum(set1_data, [])
    set2_data_sum = sum(set2_data, [])
    set11_data = {x for x in set1_data_sum}
    set22_data = {x for x in set2_data_sum}
    return set11_data.intersection(set22_data)


def exercise_diference(set1: set, set2: set) -> set:
    """
        obtener los elementos que estan en el conjunto uno  pero no en el conjunto dos
    """
    return set1.difference(set2)


def exercise_symmetric_difference(set1: set, set2: set) -> set:
    """
        conjunto de elementos que están ya sea en el primero o en el segundo conjunto, pero no en ambos.
    """
    return set1.symmetric_difference(set2)


def run():
    exe1 = exercise1("companies2.csv")
    print("promedio: ", exe1.get('promedio')[1]/exe1.get('promedio')[0])

    exe2 = exercise2("companies2.csv")
    print("las 10 empresas más actuales\n",exe2[0:10],"\nlas 10 empresas más antiguas\n",exe2[10:])

    exe3 = exercise3("companies2.csv")
    print(exe3)

    exe4 =  exercise4("companies2.csv")
    print(exe4)

    # funciones parciales

    # con curry
    exe5 = exercise5_with_curry("stopwords-en.txt")
    print("con curry\n", exe5(30))

    # con partial
    exe55 = functools.partial(exercise5, "stopwords-en.txt")
    print("con partial\n", exe55(1))

    exercise6("companies2.csv")

    monada_exercise = exercise_monada("companies2.csv", 'ibm',)
    print("Coincidencias de búsquedas: ", monada_exercise)

    exe_set = exercise_set1("companies2.csv", 'united states')
    print(exe_set)

    exe_intersection = exercise_intersection(exercise_set1("companies2.csv", 'united states'),exercise_set1("companies2.csv", 'china'))
    print(exe_intersection)

    exe_union = exercise_union(exercise_set1(
        "companies2.csv", 'united states'), exercise_set1("companies2.csv", 'china'), exercise_set1("companies2.csv", 'germany'))
    print(exe_union)

    exe_difference = exercise_diference(exercise_set1(
        "companies2.csv", 'united states'), exercise_set1("companies2.csv", 'china'))
    print(exe_difference)

    exe_simetric_difference = exercise_symmetric_difference(exercise_set1(
     "companies2.csv", 'united states'), exercise_set1("companies2.csv", 'china'))
    print(exe_simetric_difference)

    exe_tuplas_var = exercise_tuplas_var(("companies2.csv",13,30)) #inmutabilidad
    print(exe_tuplas_var)

    data_generator = *lecturas.read_csv_tuple("companies2.csv"),
    exe_tuples = exercise_tuplas(tuple(data_generator))
    print(exe_tuples)

    exe_functor_app = exercise_funtor_app(exe_tuplas_var)
    print(exe_functor_app)

    resCC = CompaniesCountry(read_csv("companies2.csv"))
    print("The country with the most companies in the world is the " + next(iter(resCC)) + " with",  next(iter(resCC.values())), "companies.")
    
    resInd = Industry(read_csv("companys2.csv"))
    print("The industry with the most companies in the world is the " + next(iter(resInd)) + " with",  next(iter(resInd.values())), "companies.")
    
    resPI = PercentIndustry(resInd, read_csv("companies2.csv"))
    print(resPI)
    
    CompaniesEmployers(read_csv("companies2.csv"))
    
    MexicanCompanies(resCC)
    
    resTC = TecnologyCompanies(read_csv("companies2.csv"))
    print(list(resTC))


if __name__ == '__main__':
    run()
