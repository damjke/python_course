import sys
import pymssql
from classes import ValidatePremium, ValidateQty, ValidateCategory, ValidateFood
from pymssql import Connection, Cursor
from datetime import datetime


class RepositorySql:

    def __init__(self, server: str, database: str, user: str, password: str):
        self.server = server
        self.database = database
        self.user = user
        self.password = password

    def execute(self, sql: str):

        connection: Connection
        with pymssql.connect(
                server=self.server,
                database=self.database,
                user=self.user,
                password=self.password
        ) as connection:

            cursor: Cursor
            with connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchone()

        return result


if __name__ == '__main__':

    if len(sys.argv) < 2:
        raise TypeError(f'Error param value format. Need \'YYYYMMDD\'')

    try:
        arg = sys.argv[1]
        date_of_interest = datetime.strptime(arg, '%Y%m%d')
    except ValueError as e:
        print(f'Error param value format {sys.argv[1]}. Need \'YYYYMMDD\'')
        raise

    repository = RepositorySql('yand.dyndns.org', 'MyDb', 'northwind', 'northwind')

    validate_qty = ValidateQty(date_of_interest)
    validate_premium = ValidatePremium(date_of_interest)
    validate_category = ValidateCategory(date_of_interest)
    validate_food = ValidateFood(date_of_interest)

    value = repository.execute(validate_qty.query())[0]
    validate_qty.validate(lambda x: x > 98, value, f'Процент заполненения qty: {value}')

    value = repository.execute(validate_premium.query())[0]
    validate_premium.validate(lambda x: x > 0, value, f'Были премиум покупки: {bool(value)}')

    value = repository.execute(validate_category.query())[0]
    validate_category.validate(lambda x: x > 95, value, f'Процент заполненения категории: {value}')

    value = repository.execute(validate_food.query())[0]
    validate_food.validate(lambda x: x>0, value, f'Были покупки из категории еда: {bool(value)}')
