from pulp import *
from simplex_method_work import run_simplex_method, generate_data
from operator import itemgetter


BASE_VACANCIES = {"junior": 40000, "middle": 60000, "senior": 80000, "team lead": 100000, "admin": 50000}
OFFICES = ["Office #1", "Office #2", "Office #3"]
NUMBER_CANDIDATES = 10
CITIES = {
    "Ульяновск": {"trend": "DOWN", "percent": 30},
    "Москва": {"trend": "UP", "percent": 50},
    "Краснодар": {"trend": "DOWN", "percent": 10},
    "Санкт-Петербург": {"trend": "UP", "percent": 30},
    "Казань": {"trend": "UP", "percent": 10},
}


def arrangement_in_city(city_name, salary_trend, percent):
    corrected_base_vacancies = {}
    for base_vacancy in BASE_VACANCIES:
        salary_changes = BASE_VACANCIES[base_vacancy] * (percent / 100)
        if salary_trend == "UP":
            corrected_base_vacancies[base_vacancy] = BASE_VACANCIES[base_vacancy] + salary_changes
        elif salary_trend == "DOWN":
            corrected_base_vacancies[base_vacancy] = BASE_VACANCIES[base_vacancy] - salary_changes

    data = generate_data(corrected_base_vacancies, OFFICES, NUMBER_CANDIDATES)
    candidates, vacancies, matrix = data[0], data[1], data[2]
    result = run_simplex_method(matrix, vacancies, candidates)
    model, variables = result[0], result[1]

    expenses = int(pulp.value(model.objective))

    print("----------" + city_name + "----------")
    print("----------Итоговая матрица:----------")
    for element in matrix:
        print(element[0] + ", " + element[1] + ": " + str(matrix.get(element)))
    print(f"Минимальные затраты для найма сотрудников в офисы = {expenses} руб.")
    for (vacancy, worker), var in dict(sorted(variables.items())).items():
        if int(var.varValue) > 0:
            print(f"- На вакансию {vacancy} назначен исполнитель {worker}, "
                  f"зарплата = {matrix[vacancy, worker]} руб.")
    print("----------------------------------------")

    return expenses


RESULTS = {}
for city in CITIES.keys():
    RESULTS[city] = arrangement_in_city(city, CITIES[city]["trend"], CITIES[city]["percent"])

for r in dict(sorted(RESULTS.items(), key=itemgetter(1))):
    print(f"Для обустройства в городе {r} необходимо потратить {RESULTS[r]} руб.")
