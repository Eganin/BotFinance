from typing import NamedTuple
import sqlalchemy


class DataBase(object):
    def __init__(self):
        self.engine = sqlalchemy.create_engine('postgresql+psycopg2://postgres:Zaharin0479@localhost:5432/costproject')
        self.connection = self.engine.connect()
        self.trans = self.connection.begin()  # tranzaction

    def insert(self, data: NamedTuple):
        try:
            self.connection.execute('INSERT INTO expenses (name_ , amount , data_create , raw_text)'
                                    'VALUES (%s , %s ,%s , %s)', (data.name, data.amount, data.data,
                                                                  data.text))
            self.trans.commit()
        except Exception as e:
            print(e)
            self.trans.rollback()

    def insert_budjet(self, data: NamedTuple):
        pass

    def fetchall(self, number_output=10) -> tuple:
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
