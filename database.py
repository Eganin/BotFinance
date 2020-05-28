from typing import NamedTuple
import sqlalchemy
from structures import MessageStatistic


class DataBase(object):
    def __init__(self) -> None:
        self.engine = sqlalchemy.create_engine('postgresql+psycopg2://postgres:Zaharin0479@localhost:5432/costproject')
        self.connection = self.engine.connect()
        self.trans = self.connection.begin()  # tranzaction

    def insert(self, data: NamedTuple) -> None:
        try:
            self.connection.execute('INSERT INTO expenses (name_ , amount , data_create , raw_text)'
                                    'VALUES (%s , %s ,%s , %s)', (data.name, data.amount, data.data,
                                                                  data.text))
            self.trans.commit()
        except Exception as e:
            print(e)
            self.trans.rollback()

    def insert_budjet(self, data: int) -> None:
        try:
            self.connection.execute('TRUNCATE  TABLE budjet ;')
            self.connection.execute('INSERT INTO budjet (budjet_limit_month)'
                                    'VALUES (%s);', (data))

            self.trans.commit()

        except Exception as e:
            print(e)
            self.trans.rollback()

    def fetchall(self, number_output: int = 10) -> tuple:
        try:
            fetchall = self.connection.execute('SELECT name_ , amount , data_create FROM expenses LIMIT %s',
                                               (number_output))
            self.trans.commit()
            return fetchall

        except Exception as e:
            print(e)
            self.trans.rollback()

    def delete_all(self):
        try:
            self.connection.execute('TRUNCATE TABLE expenses;')

            self.connection.execute('TRUNCATE TABLE budjet;')

            self.trans.commit()

        except Exception as e:
            print(e)
            self.trans.rollback()

    def delete_one(self, delete_item):
        try:
            self.connection.execute('DELETE FROM expenses WHERE name_ = %s AND amount = %s AND data_create = %s;',
                                    (delete_item.products, delete_item.price, delete_item.date))

            self.trans.commit()
        except Exception as e:
            print(e)
            self.trans.rollback()

    def check_balance(self) -> tuple:
        data = []
        try:
            balance = self.connection.execute('SELECT * FROM budjet;')
            for i in balance:
                print(i)
                data.append(i)

            print(data)
            return data[-1]


        except Exception as e:
            print(e)
            self.trans.rollback()

    def get_today(self, date):
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
