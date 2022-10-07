from logger import logger
from datetime import date

tpl_zero_qty = '''
    with zero_qty as (
    SELECT CAST(count(*) AS float) AS cnt 
    FROM Sales WHERE Qty < 1 AND [Date] = '{formatted_date}' 
    ),
    total as (
    SELECT CAST(count(*) AS float) AS cnt 
    FROM Sales where [Date] = '{formatted_date}' 
    )
    SELECT 100 - (SELECT cnt FROM zero_qty) / (SELECT cnt FROM total) * 100
'''

tpl_empty_cat = '''
    with empty_cat as (
    SELECT CAST(count(*) AS float) AS cnt 
    FROM Sales WHERE Category IS NULL AND [Date] = '{formatted_date}' 
    ),
    total as (
    SELECT CAST(count(*) AS float) AS cnt 
    FROM Sales where [Date] = '{formatted_date}' 
    )
    SELECT 100 - (SELECT cnt FROM empty_cat) / (SELECT cnt FROM total) * 100
'''

tpl_premium = '''
    SELECT COUNT(*) FROM Sales s WHERE Category = 'ювелирные изделия' AND ClientPremium = 1 AND [Date] = '{formatted_date}'
'''

tpl_food = '''
    SELECT COUNT(*) FROM Sales s WHERE Category = 'Еда' AND [Date] = '{formatted_date}'
'''


class ValidatorBase:

    def __init__(self, date_of_interest: date):
        self.date_of_interest = date_of_interest

    def query(self) -> str:
        # Должен возвращать sql запрос, необходимый
        # для проведения проверки на дату date_of_interest
        raise NotImplementedError

    @staticmethod
    def validate(rule, value, message):
        if rule(value):
            logger.info(message)
        else:
            logger.warning(message)


class ValidateQty(ValidatorBase):

    def __init__(self, date_of_interest):
        super(ValidateQty, self).__init__(date_of_interest)

    def query(self) -> str:
        formatted_date = self.date_of_interest.strftime('%Y%m%d')
        return tpl_zero_qty.format(formatted_date=formatted_date)


class ValidateCategory(ValidatorBase):

    def __init__(self, date_of_interest):
        super(ValidateCategory, self).__init__(date_of_interest)

    def query(self) -> str:
        formatted_date = self.date_of_interest.strftime('%Y%m%d')
        return tpl_empty_cat.format(formatted_date=formatted_date)


class ValidatePremium(ValidatorBase):

    def __init__(self, date_of_interest):
        super(ValidatePremium, self).__init__(date_of_interest)

    def query(self) -> str:
        formatted_date = self.date_of_interest.strftime('%Y%m%d')
        return tpl_premium.format(formatted_date=formatted_date)


class ValidateFood(ValidatorBase):

    def __init__(self, date_of_interest):
        super(ValidateFood, self).__init__(date_of_interest)

    def query(self) -> str:
        formatted_date = self.date_of_interest.strftime('%Y%m%d')
        return tpl_food.format(formatted_date=formatted_date)
