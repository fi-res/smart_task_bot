from abc import ABC, abstractmethod
from collections import defaultdict


class Staff(ABC):
    def __init__(self, name: str, tasks: list[dict]):
        self.name = name
        self.reasons: dict[str, int] = defaultdict(int)
        self.solves: dict[str, int] = defaultdict(int)
        self.feed(tasks)

    def _feed_reasons_and_solves(self, tasks: list[dict]):
        for task in tasks:
            if task["appeal_reason"]:
                self.reasons[task["appeal_reason"]] += 1
            if task["solve"]:
                self.solves[task["solve"]] += 1

    def _format_reasons(self):
        return "\n".join((f" - {k}: {v}" for k, v in self.reasons.items()))

    def _format_solves(self):
        return "\n".join((f" - {k}: {v}" for k, v in self.solves.items()))

    @abstractmethod
    def _feed_counters(self, tasks: list[dict]): ...

    def feed(self, tasks: list[dict]):
        self._feed_reasons_and_solves(tasks)
        self._feed_counters(tasks)

    @abstractmethod
    def format(self) -> str | None: ...


class Installer(Staff):
    def __init__(self, name: str, tasks: list[dict]):
        self.completed_tasks = 0
        super().__init__(name, tasks)

    def _feed_counters(self, tasks: list[dict]):
        self.completed_tasks += len(tasks)

    def format(self) -> str | None:
        content = f"<b>{self.name}</b>"
        if self.completed_tasks:
            content += f"\nВыполнено заданий: {self.completed_tasks}"
        if self.reasons:
            content += f"\nПричины обращений:\n{self._format_reasons()}"
        if self.solves:
            content += f"\nРешения:\n{self._format_solves()}"

        if content.count("\n") > 0:
            return content


class Operator(Staff):
    def __init__(self, name: str, tasks: list[dict]):
        self.appeals = 0
        self.connections = 0
        self.repairs = 0
        self.magistral_repairs = 0
        self.mitris_repairs = 0
        super().__init__(name, tasks)

    def _feed_counters(self, tasks: list[dict]):
        for task in tasks:
            match task["type"]["id"]:
                case 44:
                    self.appeals += 1
                case 28 | 26:
                    self.connections += 1
                case 37:
                    self.repairs += 1
                case 38:
                    self.magistral_repairs += 1
                case 64:
                    self.mitris_repairs += 1

    def format(self) -> str | None:
        content = f"<b>{self.name}</b>"
        if self.appeals:
            content += f"\nСоздано обращений: {self.appeals}"
        if self.connections:
            content += f"\nСоздано заявок на подключение: {self.connections}"
        if self.repairs:
            content += f"\nСоздано заявок на ремонт: {self.repairs}"
        if self.magistral_repairs:
            content += f"\nСоздано заявок на магистральный ремонт: {self.magistral_repairs}"
        if self.mitris_repairs:
            content += f"\nСоздано заявок на ремонт Mitris: {self.mitris_repairs}"
        if self.reasons:
            content += f"\nПричины обращений:\n{self._format_reasons()}"
        if self.solves:
            content += f"\nРешения:\n{self._format_solves()}"

        if content.count("\n") > 0:
            return content


def format_installer_tasks(tasks: list[dict]) -> str:
    objects: dict[str, list[dict]] = defaultdict(list)

    for task in tasks:
        for employee in task["employees"]:
            objects[employee["name"]].append(task)
        for division in task["divisions"]:
            objects[division["name"]].append(task)

    content = []
    for installer in [Installer(name, tasks) for name, tasks in objects.items()]:
        content.append(installer.format())

    return "\n\n".join([c for c in content if c]) or "Сегодня не было выполнено ни одного задания"


def format_operator_tasks(tasks: list[dict]) -> str:
    objects: dict[str, list[dict]] = defaultdict(list)

    for task in tasks:
        objects[task["author"]["name"]].append(task)

    content = []
    for operator in [Operator(name, tasks) for name, tasks in objects.items()]:
        content.append(operator.format())

    return "\n\n".join([c for c in content if c]) or "За эту смену не было выполнено ни одного задания"
