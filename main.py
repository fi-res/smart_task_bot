from asyncio import run
from datetime import datetime, time
from json import loads
from os import getenv
from zoneinfo import ZoneInfo

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv
from scheduler.asyncio import Scheduler

from format import format_installer_tasks, format_operator_tasks

load_dotenv()

from api import get_installer_tasks, get_operator_tasks  # noqa # i need to load dotenv

bot = Bot(getenv("BOT_TOKEN", ""), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
bishkek = ZoneInfo("Asia/Bishkek")

INSTALLERS_GROUP_ID = int(getenv("INSTALLERS_GROUP_ID", 0))
OPERATORS_GROUP_ID = int(getenv("OPERATORS_GROUP_ID", 0))

MORNING_SHIFT_OPERATORS = list(map(int, loads(getenv("MORNING_SHIFT_OPERATORS", "[]"))))
NIGHT_SHIFT_OPERATORS = list(map(int, loads(getenv("NIGHT_SHIFT_OPERATORS", "[]"))))
INSTALLERS = list(map(int, loads(getenv("INSTALLERS", "[]"))))

DAY_START = time.fromisoformat(getenv("DAY_START", "")).replace(tzinfo=bishkek)
DAY_END = time.fromisoformat(getenv("DAY_END", "")).replace(tzinfo=bishkek)
NIGHT_START = time.fromisoformat(getenv("NIGHT_START", "")).replace(tzinfo=bishkek)
NIGHT_END = time.fromisoformat(getenv("NIGHT_END", "")).replace(tzinfo=bishkek)
MORNING_START = time.fromisoformat(getenv("MORNING_START", "")).replace(tzinfo=bishkek)
MORNING_END = time.fromisoformat(getenv("MORNING_END", "")).replace(tzinfo=bishkek)


async def installer_report():
    print("make installer report")
    await bot.send_message(
        INSTALLERS_GROUP_ID, "<b>Отчет по работе монтажников</b>\n" + format_installer_tasks(get_installer_tasks(DAY_START, DAY_END))
    )
    print("sent report")


async def operator_morning_report():
    print("make operator morning report")
    await bot.send_message(
        OPERATORS_GROUP_ID,
        "<b>Отчет по работе операторов <i>(1 смена)</i></b>\n"
        + format_operator_tasks(get_operator_tasks(MORNING_SHIFT_OPERATORS, MORNING_START, MORNING_END))
    )
    print("sent report")


async def operator_night_report():
    print("make operator night report")
    await bot.send_message(
        OPERATORS_GROUP_ID,
        "<b>Отчет по работе операторов <i>(2 смена)</i></b>\n"
        + format_operator_tasks(get_operator_tasks(NIGHT_SHIFT_OPERATORS, NIGHT_START, NIGHT_END, next_day=True))
    )
    print("sent report")


@dp.message(Command("report"))
async def report(message: Message):
    if message.chat.id == OPERATORS_GROUP_ID:
        if MORNING_START < datetime.now(tz=bishkek).time() < MORNING_END:
            await operator_morning_report()
        else:
            await operator_night_report()

    elif message.chat.id == INSTALLERS_GROUP_ID:
        await installer_report()

    else:
        await message.answer("Команда должна быть отпарвлена в группе монтажников или колл-центра")


async def main():
    schedule = Scheduler(tzinfo=ZoneInfo("Asia/Bishkek"))
    schedule.daily(DAY_END, installer_report)
    schedule.daily(MORNING_END, operator_morning_report)
    schedule.daily(NIGHT_END, operator_night_report)

    print("start polling")
    await dp.start_polling(bot)


if __name__ == "__main__":
    run(main())
