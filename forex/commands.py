import click
from flask.cli import with_appcontext

@click.command()
def test():
    print('test command')

@click.command(help='Initialize db')
@with_appcontext
def init_db():
    from forex import db
    db.create_all()

@click.command(help='Load all currency data')
@with_appcontext
def load_currencies():
    import csv
    from forex import db
    from forex.rates.models import Currency

    with open('currencies.csv') as f:

        reader = csv.DictReader(f, skipinitialspace=True)
        session = db.session()

        for row in reader:
            print('Adding currency record for %(country_name)s' % row)
            c = Currency(**row)
            session.add(c)

        session.commit()

@click.command(help='Download and load historic exchange rates')
@click.option('--start-date', type=click.DateTime(formats=['%Y-%m-%d']), help='Starting date (default 10 days before end)')
@click.option('--end-date', type=click.DateTime(formats=['%Y-%m-%d']), help='Ending date (default now)')
@with_appcontext
def load_rates(start_date, end_date):
    import datetime
    from forex import db
    from forex.rates.rate_downloader import Downloader
    from forex.rates.models import Currency, Rate

    if not end_date:
        end_date = datetime.datetime.now()

    if not start_date:
        start_date = end_date - datetime.timedelta(days=10)

    downloader = Downloader(start_date=start_date.date(), end_date=end_date.date())

    session = db.session()

    all_currencies = session.query(
        Currency.currency_id, Currency.h10_id
    ).all()

    currency_map = {}

    for currency in all_currencies:
        currency_map[currency.h10_id] = currency.currency_id

    for rate in downloader.iterate_rates():
        print(rate)
        currency_id = currency_map[rate['h10_id']]
        rate = Rate(currency_id=currency_id, per_dollar=rate['per_dollar'], rate_date=rate['rate_date'])
        session.add(rate)

    session.commit()
