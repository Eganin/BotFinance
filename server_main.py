import logging
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, executor, types  # default imports

from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

import expenses
import exceptions

load_dotenv()  # load .env

# constant
API_TOKEN = str(os.getenv('TG_TOKEN'))  # load api in .env
ID_ADMIN = int(os.getenv('ADMIN_ID'))

DICTIONARY_LIST = []

# configure logging
logging.basicConfig(level=logging.INFO)

# init a bot and dispatcher
bot = Bot(token=API_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)


class DeleteMessage(StatesGroup):
    message = State()


def auth_user(func):
    async def authentication(message):
        if message['from']['id'] != ID_ADMIN:
            return await message.reply('доступ закрыт', reply=False)

        return await func(message)

    return authentication


@dp.message_handler(commands=['start'])
@auth_user
async def welcome(message: types.message) -> None:
    '''welcome message'''
    await message.answer('Приветствую тебя , я бот который проводит учет финансов \n'
                         'Введи или нажми на команды если не понятно введи /help \n'
                         'Добавить расход : 250 такси \n'
                         'Статистика на сегодня: /today \n'
                         'Стастистика за месяц : /month \n'
                         'Узнать последние внесенные расходы: /expenses \n'
                         'Категории различных затрат : /categories \n'
                         'Установить бюджет на месяц или изменить его : /budget'
                         'Удалить все данные о покупках : /delete_all \n'
                         'Удалить определенную покупку : /delete_one'
                         'Изменить бюджет на месяц : /budjet_month'
                         'Изменить бюджет на год : /budjet_year', reply=False)


@dp.message_handler(commands=['help'])
@auth_user
async def print_help(message: types.message) -> None:
    '''help to bot'''
    await message.answer('Для того чтобы добавить расходы введите например : \n250 такси')


@dp.message_handler(commands=['today'])
@auth_user
async def print_today_statistic(message: types.message) -> None:
    print('today')


@dp.message_handler(commands=['month'])
@auth_user
async def print_month_statistic(message: types.message):
    print('month')


@dp.message_handler(commands=['expenses'])
@auth_user
async def print_expenses(message: types.message) -> None:
    DICTIONARY_LIST[:] = []  # clear list
    answer_database = expenses.out_expenses()
    cnt = 0
    for i in answer_database:
        cnt += 1
        DICTIONARY_LIST.append(expenses.DeleteDict(name='/del' + str(cnt),
                                                   expenses=f'{i.name}:{i.amount}:{i.date}'))  # split ':'
        await message.answer(f'{i.name}: {i.amount}руб {i.date} года' + ' ' + '/del' + str(cnt))


@dp.message_handler(commands=['budjet_month'])
@auth_user
async def add_budjet_month(message: types.message) -> None:
    price_month = int(message.text.split()[1])
    message_db = expenses.add_budjet_month(price_month)
    await message.answer(message_db.message)


@dp.message_handler(commands=['delete_all'])
@auth_user
async def delete_all(message: types.message) -> None:
    answer_database = expenses.delete_all()
    await message.answer(answer_database.message)


@dp.message_handler(commands=['balance'])
@auth_user
async def balance(message: types.message) -> None:
    answer_database = expenses.check_to_balance()
    print(answer_database)
    try:
        await message.answer(f'На месяц: {answer_database.month} руб\n')

    except:
        await message.answer(f'На месяц: 0 руб\nВы ничего не вводили')


@dp.message_handler(lambda message: message.text.startswith('/del'))
@auth_user
async def del_expenses(message: types.message) -> None:
    for i in DICTIONARY_LIST:
        if i['name'] == message.text:
            answer_databse = expenses.delete_expense(i['expenses'])
            print('delete item to database ')
            await message.answer(answer_databse.message)


@dp.message_handler(lambda message: message)  # other message , message to add expenses
@auth_user
async def add_expenses(message: types.message) -> None:
    '''add to new expenses'''
    message_user = expenses.add_expense(message.text)
    await message.answer(
        'Добвалена покупка :' + '\n' + 'Название :' + str(message_user.name) + '\n' + 'Название : ' + str(
            message_user.amount) + '\n' + 'Дата :' + str(
            message_user.data) + '\n' + 'Текст сообщения:' + str(message_user.text) + '\n')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
