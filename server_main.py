import logging
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, executor, types  # default imports

from structures import DeleteDict

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


def auth_user(func):  # decorator from authentication
    async def authentication(message):
        if message['from']['id'] != ID_ADMIN:
            return await message.reply('доступ закрыт', reply=False)

        return await func(message)

    return authentication


@dp.message_handler(commands=['start'])
@auth_user
async def welcome(message: types.message) -> None:
    '''welcome message'''
    try:
        await message.answer('Приветствую тебя , я бот который проводит учет финансов \n'
                             'Введи или нажми на команды если не понятно введи /help \n'
                             'Добавить расход : 250 такси \n'
                             'Статистика на сегодня: /today \n'
                             'Стастистика за месяц : /month \n', reply=False)

        await  message.answer('Узнать последние внесенные расходы: /expenses \n'
                              'Установить бюджет на месяц или изменить его : /budjet\n'
                              'Удалить все данные о покупках : /delete_all \n', reply=False)

        await  message.answer(
            'Узнать баланс: /balance\n'
            'Удалить определенную покупку: /del\n'
            'Узнать статистку за год: /year\n'
            'Дата зарплаты /databal', reply=False)

    except:
        raise exceptions.FatalError(await message.answer('Произошла неизвестная ошибка'))


@dp.message_handler(commands=['help'])
@auth_user
async def print_help(message: types.message) -> None:
    '''help to bot'''
    try:
        await message.answer('Для того чтобы добавить расходы введите например : \n250 такси\n'
                             'Для того чтобы пользоваться командами нужно их в точности набрать\n'
                             'При наборе команды: /budjet надо набрать размер бюджета на месяц\n'
                             'Например:/budjet 100000'
                             'Чтобы удалить покупку надо просмотреть /expenses и нажать определенный /del'
                             'Чтобы указать число поступления зарплаты: /databall число , \n'
                             'Напрмер: /databall 20', reply=False)
    except:
        raise exceptions.FatalError(await message.answer('Произошла неизвестная ошибка'))


@dp.message_handler(commands=['today'])
@auth_user
async def print_today_statistic(message: types.message) -> None:
    answer_database = expenses.get_statistic_today()
    try:
        if answer_database.message is not None:
            await message.answer('На сегодня зартачено : ' + str(answer_database.message) + ' рублей')

        else:
            await message.answer('На сегодня зартачено : ' + str(0) + ' рублей')

    except:
        raise exceptions.ErrorToDataBase(await message.answer('Произошли какие-то неполадки с базой данных'))


@dp.message_handler(commands=['month'])
@auth_user
async def print_month_statistic(message: types.message):
    try:
        answer_database = expenses.get_statistic_month()
        if answer_database.message is not None:
            await message.answer('За месяц затрачено ' + str(answer_database.message) + ' руб')

        else:
            await message.answer('За месяц затрачено ' + str(0) + ' руб')

    except:
        raise exceptions.ErrorToDataBase(await message.answer('Произошли какие-то неполадки с базой данных'))


@dp.message_handler(commands=['year'])
@auth_user
async def print_year_statistic(message: types.message):
    try:
        answer_database = expenses.get_statistic_year()
        if answer_database.message is not None:
            await message.answer('За год затрачено ' + str(answer_database.message) + ' руб')

        else:
            await message.answer('За год затрачено ' + str(0) + ' руб')

    except:
        raise exceptions.ErrorToDataBase(await message.answer('Произошли какие-то неполадки с базой данных'))


@dp.message_handler(commands=['expenses'])
@auth_user
async def print_expenses(message: types.message) -> None:
    if DICTIONARY_LIST is None:
        await message.answer('Список недавних покупок пуст')  # if expenses list clear to not have error

    DICTIONARY_LIST[:] = []  # clear list

    answer_database = expenses.out_expenses()
    cnt = 0
    for i in answer_database:
        cnt += 1
        DICTIONARY_LIST.append(DeleteDict(name='/del' + str(cnt),
                                          expenses=f'{i.name}:{i.amount}:{i.date}'))  # split ':'
        try:
            await message.answer(f'{i.name}: {i.amount}руб {i.date} года' + '  ' + 'Удалить:' + ' ' + '/del' + str(cnt))
        except:
            raise exceptions.ErrorToDataBase(await message.answer('Произошли какие-то неполадки с базой данных'))


@dp.message_handler(commands=['budjet'])
@auth_user
async def add_budjet_month(message: types.message) -> None:
    price_month = int(message.text.split()[1])
    message_db = expenses.add_budjet_month(price_month)
    try:
        await message.answer(message_db.message)
    except:
        raise exceptions.NoCorrectMessage(await message.answer('Вы неправилно ввели данные'))


@dp.message_handler(commands=['delete_all'])
@auth_user
async def delete_all(message: types.message) -> None:
    try:
        answer_database = expenses.delete_all()
        await message.answer(answer_database.message)
        await  message.answer('не забудьте потом добавить дату зарплаты\n с помощью команды /databal')
    except:
        raise exceptions.ErrorToDataBase(await message.answer('Произошли какие-то неполадки с базой данных'))


@dp.message_handler(commands=['balance'])
@auth_user
async def balance(message: types.message) -> None:
    answer_database = expenses.check_to_balance()
    try:
        await message.answer(f'На месяц: {answer_database.month} руб\n')

    except:
        await message.answer(f'На месяц: 0 руб\nВы ничего не вводили')
        raise exceptions.NullBalance(await message.answer('Баланс чист или отсутсвует'))


@dp.message_handler(commands=['databal'])
@auth_user
async def auto_balance(message: types.message) -> None:
    await message.answer('Число обновления баланса добавлено')
    data_balance = int(message.text.split()[1])
    expenses.check_replenishment_balance(expenses.replenishment_balance_date(data_balance))


@dp.message_handler(lambda message: message.text.startswith('/del'))
@auth_user
async def del_expenses(message: types.message) -> None:
    for i in DICTIONARY_LIST:
        if i['name'] == message.text:
            try:
                answer_databse = expenses.delete_expense(i['expenses'])
                print('delete item to database ')
                await message.answer(answer_databse.message)

            except:
                raise exceptions.NoCorrectMessage(await message.answer('Вы неправильно ввели данные'))


@dp.message_handler(lambda message: message)  # other message , message to add expenses
async def add_expenses(message: types.message) -> None:
    '''add to new expenses'''
    try:
        ratio = expenses.ratio_balance()
        print(ratio)
        expenses.check_balance_repleh()
        answer_database = expenses.check_to_balance()
        if answer_database.month <= 0:
            await message.answer('У вас закончился баланс , вы не можете делать покупки')

        else:
            if ratio <= 20.0:
                await message.answer('У вас мало денег следите за балансом')

        try:
            message_user = expenses.add_expense(message.text)
            await message.answer(
                'Добвалена покупка :' + '\n' + 'Название :' + str(message_user.name) + '\n' + 'Стоимость : ' + str(
                    message_user.amount) + 'руб' + '\n' + 'Дата :' + str(
                    message_user.data) + '\n' + 'Текст сообщения:' + str(message_user.text) + '\n')

        except:
            raise exceptions.NoCorrectMessage(await message.answer('Вы неправильно ввели данные'))

    except:
        try:
            message_user = expenses.add_expense(message.text)
            await message.answer(
                'Добвалена покупка :' + '\n' + 'Название :' + str(message_user.name) + '\n' + 'Стоимость : ' + str(
                    message_user.amount) + 'руб' + '\n' + 'Дата :' + str(
                    message_user.data) + '\n' + 'Текст сообщения:' + str(message_user.text) + '\n')

        except:
            raise exceptions.NoCorrectMessage(await message.answer('Вы неправильно ввели данные'))


if __name__ == '__main__':  # start bot
    executor.start_polling(dp, skip_updates=True)  # skip errors
