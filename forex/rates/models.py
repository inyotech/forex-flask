import datetime, dateutil

from marshmallow import Schema, fields, pprint

from forex import db

# table classes

class Currency(db.Model):

    __tablename__ = 'currencies'

    currency_id          = db.Column(db.Integer, autoincrement=True, primary_key=True)
    h10_id               = db.Column(db.String(25), nullable=False, unique=True)
    country_name         = db.Column(db.String(25), nullable=False)
    short_name           = db.Column(db.String(10), nullable=False)
    flag_image_file_name = db.Column(db.String(64), nullable=False)
    currency_name        = db.Column(db.String(20), nullable=False)
    currency_code        = db.Column(db.String(3), nullable=False)
    rates                = db.relationship('Rate', back_populates='currency')

    def __repr__(self):
        return ("<Currency({0.currency_id}, {0.h10_id}, {0.country_name}, "
                "{0.short_name}, {0.flag_image_file_name}, {0.currency_name}, "
                "{0.currency_code})>").format(self)


class Rate(db.Model):

    __tablename__ = 'exchange_rates'
    __table_args__ = (
        db.UniqueConstraint('currency_id', 'rate_date'),
    )

    rate_id     = db.Column(db.Integer, autoincrement=True, primary_key=True)
    currency_id = db.Column(db.Integer, db.ForeignKey('currencies.currency_id'), nullable=False)
    rate_date   = db.Column(db.Date, nullable=False)
    per_dollar  = db.Column(db.Float, nullable=False)
    currency    = db.relationship('Currency', back_populates='rates')

# serialization classes

class CurrencySchema(Schema):
    class Meta:
        fields = ('currency_name', 'short_name', 'currency_code', 'country_name', 'flag_image_file_name')

class CurrencyRateSchema(Schema):
    class Meta:
        fields = ('currency_name', 'short_name', 'currency_code', 'country_name',
                  'flag_image_file_name', 'rate', 'rate_date')

class RateSchema(Schema):
    class Meta:
        fields = ('rate_date', 'rate')

class RateHistorySchema(Schema):
    base = fields.Nested(CurrencySchema)
    target = fields.Nested(CurrencySchema)
    rate_history = fields.Nested(RateSchema, many=True)


class LatestRateSchema(Schema):
    base = fields.Nested(CurrencySchema)
    latest_rates = fields.Nested(CurrencyRateSchema, many=True)

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

def get_all_currencies():
    return db.session.query(
        Currency
    ).order_by(Currency.country_name)

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


def get_latest_rates(base_currency='EUR'):

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
        base_rate.currency_id==currency_id_subq(base_currency),
        target_rate.rate_date==latest_date_subq(),
    ).order_by(Currency.country_name)

    return latest_rates.all()
