from typing import NamedTuple, Dict
import datetime


class Message(NamedTuple):  # object to message user
    amount: int
    category_text: str


class Expenses(NamedTuple):  # object to expenses user
    name: str
    amount: int
    data: str
    text: str


class MessageUser(NamedTuple):
    message: str


class MessageExpense(NamedTuple):
    name: str
    amount: int
    date: datetime.date


class DeleteItem(NamedTuple):
    products: str
    price: int
    date: str


class BalanceMessage(NamedTuple):
    month: int


class MessageStatistic(NamedTuple):
    amount: int
    date: datetime.date


class DeleteDict(Dict):
    name: str
    expenses: str
