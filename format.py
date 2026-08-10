from collections import Counter


def _format(object_type: str, tasks: list[dict]):
    objects_count = []
    objects = {}
    for task in tasks:
        objects_count.extend([object["name"] for object in task[object_type]])
        for object in task[object_type]:
            if task["appeal_reason"]:
                objects.setdefault(object["name"], {}).setdefault("reasons", {}).setdefault(task["appeal_reason"], 0)
                objects[object["name"]]["reasons"][task["appeal_reason"]] += 1  # cant change value of setdefaulted field inline

            if task["solve"]:
                objects.setdefault(object["name"], {}).setdefault("solves", {}).setdefault(task["solve"], 0)
                objects[object["name"]]["solves"][task["solve"]] += 1

    return objects_count, objects


def format_installer_tasks(tasks: list[dict]):
    divisions_count, divisions = _format("divisions", tasks)

    return "\n".join(
        [
            f"""
<b>{division}</b>:
Выполнено заданий: {count}
Причины обращений: {"".join([f"\n - {reason}: {reason_count}" for reason, reason_count in divisions.get(division, {}).get("reasons", {}).items()]) or "-"}
Решения: {"".join([f"\n - {solve}: {solve_count}" for solve, solve_count in divisions.get(division, {}).get("solves", {}).items()]) or "-"}
"""
            for division, count in dict(Counter(divisions_count)).items()
        ]
    )


def format_operator_tasks(tasks: list[dict]):
    employees_count, employees = _format("employees", tasks)

    return "\n".join(
        [
            f"""
<b>{employee}</b>:
Создано обращений: {count}
Виды обращений: {"".join([f"\n - {reason}: {reason_count}" for reason, reason_count in employees.get(employee, {}).get("reasons", {}).items()]) or "-"}
Решения: {"".join([f"\n - {solve}: {solve_count}" for solve, solve_count in employees.get(employee, {}).get("solves", {}).items()]) or "-"}
"""
            for employee, count in dict(Counter(employees_count)).items()
        ]
    )
