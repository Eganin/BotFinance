from typing import NamedTuple
import sqlalchemy
from structures import MessageStatistic
from dotenv import load_dotenv
import os


class DataBase(object):
    load_dotenv()  # load .env

    def __init__(self) -> None:
        self.path_engine = os.getenv("POSTGRES_ENGINE")
        self.engine = sqlalchemy.create_engine(self.path_engine)
        self.connection = self.engine.connect()
        self.trans = self.connection.begin()  # tranzaction

    def insert(self, data: NamedTuple) -> None:  # insert table expenses
        try:
            self.connection.execute('INSERT INTO expenses (name_ , amount , data_create , raw_text)'
                                    'VALUES (%s , %s ,%s , %s)', (data.name, data.amount, data.data,
                                                                  data.text))
            self.trans.commit()
        except Exception as e:
            print(e)
            self.trans.rollback()

    def insert_budjet(self, data: int) -> None:  # insert table budjet
        try:
            self.connection.execute('TRUNCATE  TABLE budjet ;')
            self.connection.execute('INSERT INTO budjet (budjet_limit_month , budjet_limit_month_default)'
                                    'VALUES (%s , %s);', (data, data))

            self.trans.commit()

        except Exception as e:
            print(e)
            self.trans.rollback()

    def fetchall(self, number_output: int = 10) -> tuple:  # return expenses result
        try:
            fetchall = self.connection.execute('SELECT name_ , amount , data_create FROM expenses LIMIT %s',
                                               (number_output))
            self.trans.commit()
            return fetchall

        except Exception as e:
            print(e)
            self.trans.rollback()

    def delete_all(self):  # all truncate
        try:
            self.connection.execute('TRUNCATE TABLE expenses RESTART IDENTITY;')

            self.connection.execute('TRUNCATE TABLE budjet RESTART IDENTITY;')

            self.trans.commit()

        except Exception as e:
            print(e)
            self.trans.rollback()

    def delete_one(self, delete_item):  # delete one item
        try:
            self.connection.execute('DELETE FROM expenses WHERE name_ = %s AND amount = %s AND data_create = %s;',
                                    (delete_item.products, delete_item.price, delete_item.date))

            self.trans.commit()
        except Exception as e:
            print(e)
            self.trans.rollback()

    def check_balance(self) -> tuple:  # check balance to db from a month
        data = []
        try:
            balance = self.connection.execute('SELECT * FROM budjet;')
            for i in balance:
                data.append(i)

            return data[-1]


        except Exception as e:
            print(e)
            self.trans.rollback()

    def get_today(self, date):  # return statistic from today
        try:
            date_statistic = self.connection.execute(
                'SELECT SUM(amount),data_create FROM expenses GROUP BY data_create;'
            )

            for i in date_statistic:
                r = MessageStatistic(amount=i[0], date=i[1])
                if str(r.date) == str(date):
                    return i[0]
            self.trans.commit()

        except Exception as e:
            print(e)
            self.trans.rollback()

    def get_statistic(self, date) -> str:
        try:
            month_statistic = self.connection.execute(
                "SELECT SUM(amount) FROM expenses WHERE DATE (data_create) >= %s;", (date))
            for i in month_statistic:
                return i[0]

            self.trans.commit()

        except Exception as e:
            print(e)
            self.trans.rollback()

    def take_away_balance(self, amount):
        data = []
        try:
            balance = self.connection.execute('SELECT * FROM budjet;')
            for i in balance:
                data.append(i)

            self.connection.execute('INSERT INTO budjet (budjet_limit_month) VALUES (%s);',
                                    (int(data[-1][-1]) - int(amount)))

            self.trans.commit()


        except Exception as e:
            print(e)
            self.trans.rollback()

    def get_default_balance(self):
        try:
            default_balance = self.connection.execute('SELECT budjet_limit_month_default FROM budjet WHERE id=1;')
            for i in default_balance:
                return i[0]


        except Exception as e:
            print(e)
            self.trans.rollback()

    def init_db(self):
        pass

    def check_db(self):
        pass
