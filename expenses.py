from typing import List
import re
from exceptions import NoCorrectMessage
import datetime
import database
from structures import Message, MessageUser, Expenses, BalanceMessage, MessageExpense, DeleteItem


def get_datetime_today():  # get time to db
    return str(datetime.date.today())


def parsing_message(message_user: str) -> Message:  # parsing message user to add expenses
    'Parsing to message user'
    regexp_pattern = re.match(r"([\d ]+) (.*)", message_user)  # regexp to amount and name
    if not regexp_pattern or not regexp_pattern.group(0) \
            or not regexp_pattern.group(1) or not regexp_pattern.group(2):
        raise NoCorrectMessage('Ваше сообщение не слишком понятно , \n'
                               'Попробуйте написать в таком виде : \n'
                               'такси 250')

    else:
        amount = int(regexp_pattern.group(1).replace(' ', ''))
        category_text = regexp_pattern.group(2).strip().lower()
        return Message(amount=amount,
                       category_text=category_text)


def add_expense(expense: str) -> Expenses:  # add expense to db
    result_parsing = parsing_message(expense)
    data_today = get_datetime_today()
    expenses = Expenses(
        name=result_parsing.category_text,
        amount=result_parsing.amount,
        data=data_today,
        text=expense)

    database.DataBase().insert(expenses)

    return Expenses(name=result_parsing.category_text,
                    amount=result_parsing.amount,
                    data=data_today,
                    text=expense)


def delete_all() -> MessageUser:  # truncate table from  db
    try:
        database.DataBase().delete_all()
        return MessageUser(message='Все данные о покупках удалены')

    except:
        return MessageUser(message='Произошла ошибка')


def out_expenses() -> List[MessageExpense]:  # return last expenses default :10
    data_all = []
    try:
        tuple_expenses = database.DataBase().fetchall()
        for i in tuple_expenses:
            data_all.append(MessageExpense(name=i[0], amount=i[1], date=i[2]))
        return data_all


    except Exception as e:
        print(e)


def delete_expense(message_from_user: str) -> MessageUser:  # delete certain expense
    delete_item = message_from_user.split(':')
    print(delete_item)
    try:
        database.DataBase().delete_one(
            DeleteItem(products=str(delete_item[0]), price=int(delete_item[1]), date=str(delete_item[2])))

        return MessageUser(message='Удаление прощло успешно')
    except:
        pass


def add_budjet_month(price_month: int) -> MessageUser:  # add to db budjet user
    try:
        database.DataBase().insert_budjet(price_month)

        return MessageUser(message='Бюджет на месяц успешно изменен')
    except:
        pass


def check_to_balance() -> BalanceMessage:  # checking from db balance user
    try:
        answer_balance = database.DataBase().check_balance()
        return BalanceMessage(month=answer_balance[1], )

    except:
        pass


def get_statistic_today() -> MessageUser:  # return statistic today
    date_today = get_datetime_today()
    stat_number = database.DataBase().get_today(date_today)
    return MessageUser(message=stat_number)
