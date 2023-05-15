from pulp import *
from random import choice, randrange


def generate_data(base_vacancies, offices, number_candidates):
    candidates = []
    for vacancy in base_vacancies.keys():
        for i in range(number_candidates):
            candidates.append(vacancy + "_" + str(i + 1))

    vacancies = []
    for vacancy in base_vacancies.keys():
        for office in offices:
            vacancies.append(vacancy.upper() + "_" + office)

    matrix = {}
    for vacancy in vacancies:
        for candidate in candidates:
            if vacancy.lower().split("_")[0] == candidate.lower().split("_")[0]:
                base_salary = base_vacancies.get(vacancy.lower().split("_")[0])
                salary_aspiration = choice(["UP", "DOWN", "BASE"])
                if salary_aspiration == "BASE":
                    matrix[vacancy, candidate] = base_salary
                elif salary_aspiration == "UP":
                    matrix[vacancy, candidate] = base_salary + randrange(5000)
                elif salary_aspiration == "DOWN":
                    matrix[vacancy, candidate] = base_salary - randrange(5000)

    return candidates, vacancies, matrix


def run_simplex_method(matrix, vacancies, workers):
    model = pulp.LpProblem("OfficeEmploymentProblem", LpMinimize)
    variables = {}
    for (vacancy, worker) in matrix:
        var_name = "x_" + vacancy + "_" + worker
        variables[vacancy, worker] = pulp.LpVariable(var_name, cat=LpBinary)
    lst_mult = [matrix[key] * var for key, var in variables.items()]
    obj_expression = pulp.lpSum(lst_mult)
    model.setObjective(obj_expression)

    # Ограничение: Все вакансии должны быть заполнены
    for v in vacancies:
        constraint_name = f"{v}_sat_constraint"
        lst_vars = []
        for w in workers:
            if (v, w) in variables:
                lst_vars.append(variables[v, w])
        model += pulp.lpSum(lst_vars) == 1, constraint_name

    # Ограничение: Один сотрудник может устроиться только на одну вакансию
    for w in workers:
        constraint_name = f"{w}_vl_constraint"
        lst_vars = []
        for v in vacancies:
            if (v, w) in variables:
                lst_vars.append(variables[v, w])
        model += pulp.lpSum(lst_vars) <= 1, constraint_name

    model.writeLP("OfficeEmploymentProblem.lp")
    model.solve()
    return model, variables
