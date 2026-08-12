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


def _format_field(title: str, object: dict, field: str):
    res = "".join([f"\n - {field}: {field_count}" for field, field_count in object.get(field, {}).items()])
    if res:
        return title + ": " + res


def format_installer_tasks(tasks: list[dict]):
    divisions_count, divisions = _format("divisions", tasks)
    employees_count, employees = _format("employees", tasks)

    def _get_fields(object):
        return divisions.get(object, employees.get(object, {}))

    content = ""
    for object, count in dict(Counter(divisions_count + employees_count)).items():
        object_content = f"<b>{object}</b>\nВыполнено заданий: {count}"

        reasons = _format_field("Причины обращений", _get_fields(object), "reasons")
        if reasons:
            object_content += "\n" + reasons

        solves = _format_field("Решения", _get_fields(object), "solves")
        if solves:
            object_content += "\n" + solves

        content += "\n\n" + object_content

    return content or "Сегодня не было выполнено ни одного задания"


def format_operator_tasks(tasks: list[dict]):
    employees_count, employees = _format("employees", tasks)

    content = ""
    for object, count in dict(Counter(employees_count)).items():
        object_content = f"<b>{object}</b>\nСоздано обращений: {count}"

        reasons = _format_field("Виды обращений", employees.get(object, {}), "reasons")
        if reasons:
            object_content += "\n" + reasons

        solves = _format_field("Решения", employees.get(object, {}), "solves")
        if solves:
            object_content += "\n" + solves

        content += "\n\n" + object_content

    return content or "За эту смену не было выполнено ни одного задания"
