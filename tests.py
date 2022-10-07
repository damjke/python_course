from unittest import TestCase
from datetime import datetime
from classes import ValidatePremium, ValidateQty, ValidateCategory, ValidateFood


class TestValidatePremium(TestCase):

    def test_query(self):
        date_of_interest = datetime.strptime('20211010', '%Y%m%d')
        validate_qty = ValidateQty(date_of_interest)
        query = validate_qty.query()
        self.assertMultiLineEqual('''
    with zero_qty as (
    SELECT CAST(count(*) AS float) AS cnt 
    FROM Sales WHERE Qty < 1 AND [Date] = '20211010' 
    ),
    total as (
    SELECT CAST(count(*) AS float) AS cnt 
    FROM Sales where [Date] = '20211010' 
    )
    SELECT 100 - (SELECT cnt FROM zero_qty) / (SELECT cnt FROM total) * 100
'''.strip(), query.strip())

class TestValidateQty(TestCase):

    def test_query(self):
        date_of_interest = datetime.strptime('20211010', '%Y%m%d')
        validate_cat = ValidateCategory(date_of_interest)
        query = validate_cat.query()
        self.assertMultiLineEqual('''
    with empty_cat as (
    SELECT CAST(count(*) AS float) AS cnt 
    FROM Sales WHERE Category IS NULL AND [Date] = '20211010' 
    ),
    total as (
    SELECT CAST(count(*) AS float) AS cnt 
    FROM Sales where [Date] = '20211010' 
    )
    SELECT 100 - (SELECT cnt FROM empty_cat) / (SELECT cnt FROM total) * 100
'''.strip(), query.strip())


class TestValidateCategory(TestCase):

    def test_query(self):
        date_of_interest = datetime.strptime('20211010', '%Y%m%d')
        validate_prem = ValidatePremium(date_of_interest)
        query = validate_prem.query()
        self.assertMultiLineEqual('''
    SELECT COUNT(*) FROM Sales s WHERE Category = 'ювелирные изделия' AND ClientPremium = 1 AND [Date] = '20211010'
'''.strip(), query.strip())


class TestValidateFood(TestCase):

    def test_query(self):
        date_of_interest = datetime.strptime('20211010', '%Y%m%d')
        validate_food = ValidateFood(date_of_interest)
        query = validate_food.query()
        self.assertMultiLineEqual('''
    SELECT COUNT(*) FROM Sales s WHERE Category = 'Еда' AND [Date] = '20211010'
'''.strip(), query.strip())
