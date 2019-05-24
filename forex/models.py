import datetime, dateutil

from marshmallow import Schema, fields, pprint

from forex import db

# table classes

class Currency(db.Model):

    __tablename__ = 'currencies'

    currency_id          = db.Column(db.Integer, primary_key=True)
    h10_id               = db.Column(db.String(25), unique=True)
    country_name         = db.Column(db.String(25))
    short_name           = db.Column(db.String(10))
    flag_image_file_name = db.Column(db.String(64))
    currency_name        = db.Column(db.String(20))
    currency_code        = db.Column(db.String(3))
    rates                = db.relationship('Rate', back_populates='currency')

    def __repr__(self):
        return ("<Currency({0.currency_id}, {0.h10_id}, {0.country_name}, "
                "{0.short_name}, {0.flag_image_file_name}, {0.currency_name}, "
                "{0.currency_code})>").format(self)


class Rate(db.Model):

    __tablename__ = 'exchange_rates'

    rate_id     = db.Column(db.Integer, primary_key=True)
    currency_id = db.Column(db.Integer, db.ForeignKey('currencies.currency_id'))
    rate_date   = db.Column(db.Date)
    per_dollar  = db.Column(db.Float)
    currency    = db.relationship('Currency', back_populates='rates')

# serialization classes

class CurrencySchema(Schema):
    class Meta:
        fields = ('currency_name', 'short_name', 'currency_code', 'country_name')

class RateSchema(Schema):
    rate = fields.Number()

    class Meta:
        fields = ('rate_date', 'rate')

class RateHistorySchema(Schema):
    base = fields.Nested(CurrencySchema)
    target = fields.Nested(CurrencySchema)
    rate_history = fields.Nested(RateSchema, many=True)

class LatestRateSchema(Schema):
    rate = fields.Number()
    class Meta:
        fields = (
            'country_name', 'short_name', 'flag_image_file_name',
            'currency_name', 'currency_code', 'rate_date', 'rate'
        )

# subqueries

def currency_id_subq(currency_code):
    return db.session.query(
        Currency.currency_id
    ).filter(Currency.currency_code==currency_code).subquery()

def latest_date_subq():
    return db.session.query(
        db.func.max(Rate.rate_date)
    ).subquery()

# query functions

def get_currency(code):
    return db.session.query(
        Currency
    ).filter(Currency.currency_code==code).one()

def get_rate_history(target, base='USD', start=None, end=None):
    
    if end is None:
        end = datetime.datetime.now()
    
    if start is None:
        start = end - dateutil.relativedelta.relativedelta(months=24)

    base_rate = db.aliased(Rate, name='base_rate')
    target_rate = db.aliased(Rate, name='target_rate')

    rate_history = db.session.query(
        target_rate.rate_date,
        (target_rate.per_dollar/base_rate.per_dollar).label('rate')
    ).join(
        base_rate, base_rate.rate_date==target_rate.rate_date
    ).filter(
        target_rate.currency_id==currency_id_subq(target),
        base_rate.currency_id==currency_id_subq(base),
        target_rate.rate_date>=start
    ).order_by(target_rate.rate_date)

    return rate_history.all()


def get_latest_rates(target_rate='EUR', base_rate='USD'):

    base_rate = db.aliased(Rate, name='base_rate')
    target_rate = db.aliased(Rate, name='target_rate')

    latest_rates = db.session.query(
        Currency.country_name,
        Currency.short_name,
        Currency.currency_name,
        Currency.currency_code,
        Currency.flag_image_file_name,
        target_rate.rate_date,
        (target_rate.per_dollar/base_rate.per_dollar).label('rate')
    ).join(
        base_rate, base_rate.rate_date==target_rate.rate_date
    ).join(
        Currency, Currency.currency_id==target_rate.currency_id
    ).filter(
        base_rate.currency_id==currency_id_subq('USD'),
        target_rate.rate_date==latest_date_subq(),
    ).order_by(Currency.country_name)
    
    return latest_rates.all()
