import io, csv
import datetime, dateutil

from flask import Blueprint, request, jsonify, make_response
from forex.models import (
    Currency, CurrencySchema, LatestRateSchema, RateHistorySchema, 
    get_currency, get_latest_rates, get_rate_history
)

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/')
def index():
    return "api endpoint"


@api.route('/currencies')
def currencies():
    currencies = Currency.query.all()
    currencies_schema = CurrencySchema(many=True)
    result = currencies_schema.dump(currencies)
    return jsonify({'data': result.data})


@api.route('/latest_rates', methods=['GET'])
def latest_rates():
    latest_rates = get_latest_rates()
    latest_rates_schema = LatestRateSchema(many=True)
    result = latest_rates_schema.dump(latest_rates)
    return jsonify({'data': result.data})

@api.route('/rate_history/base/<base>/target/<target>/months/<int:months>', methods=['GET'])
def rate_history(base, target, months=24):

    start = datetime.datetime.now() - dateutil.relativedelta.relativedelta(months=months)
    data = {
        'target': get_currency(target),
        'base': get_currency(base),
        'rate_history': get_rate_history(target=target, base=base, start=start)
    }

    rate_history_schema = RateHistorySchema()
    result = rate_history_schema.dump(data)

    response_format = request.args.get('format', 'json')

    if response_format == 'csv':
        return form_csv_response(data)
    else:        
        return jsonify({'data': result.data})

def form_csv_response(response_data):

    buffer = io.StringIO()
    writer = csv.writer(buffer, quoting=csv.QUOTE_ALL)

    writer.writerow(['base_currency_code', 'base_country_name', 'base_currency_name'])
    writer.writerow([
        response_data['base'].currency_code,
        response_data['base'].country_name,
        response_data['base'].currency_name,
    ])

    writer.writerow([])

    writer.writerow(['target_currency_code', 'target_country_name', 'target_currency_name'])
    writer.writerow([
        response_data['target'].currency_code,
        response_data['target'].country_name,
        response_data['target'].currency_name,
    ])

    writer.writerow([])

    writer.writerow(['date', 'exchange_rate'])
    for rate in response_data['rate_history']:
        writer.writerow([
            rate.rate_date,
            rate.rate,
        ])

    buffer.seek(0)

    response = make_response(buffer.getvalue())
    response.headers['Content-type'] = 'text/csv'

    return response
