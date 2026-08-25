from datetime import datetime, time, timedelta
from os import getenv

from requests import Session

session = Session()
session.cookies.set("token", getenv("INSIDE_TOKEN"))


def get_installer_tasks(day_start: time, day_end: time):
    print(f"get installer tasks from {day_start} to {day_end}")
    return session.get(
        f"{getenv('API_URL', '')}/tasks",
        {
            "completed_at_from": datetime.now().replace(hour=day_start.hour, minute=day_start.minute, second=day_start.second).isoformat(),
            "completed_at_to": datetime.now().replace(hour=day_end.hour, minute=day_end.minute, second=day_end.second).isoformat(),
            "type": ",".join(map(str, [28, 29, 25, 26, 37, 60, 46]))
        },
        timeout=60
    ).json()


def get_operator_tasks(ids: list[int], shift_start: time, shift_end: time, next_day: bool = False):
    print(f"get operator tasks from {shift_start} to {shift_end} for {ids}")
    completed_at_to = datetime.now().replace(hour=shift_end.hour, minute=shift_end.minute, second=shift_end.second)
    if next_day:
        completed_at_to += timedelta(days=1)

    return session.get(
        f"{getenv('API_URL', '')}/tasks",
        {
            "completed_at_from": datetime.now().replace(hour=shift_start.hour, minute=shift_start.minute, second=shift_start.second).isoformat(),
            "completed_at_to": completed_at_to.isoformat(),
            "type": ",".join(map(str, [49, 43, 66, 44, 28, 26, 37, 64, 38])),
            "author_id": ",".join(map(str, ids))
        },
        timeout=60
    ).json()
