# API endpoints providing historic foreign exchange rates

This application will provide exchange rates sourced from the [US
Federal Reserve](https://www.federalreserve.gov/).

Rates are downloaded periodically, preprocessed and stored for use by
the endpoints.  The following methods are provided:

An exchange rate viewing application that consumes this API is
available at
[https://github.com/inyotech/forex-vue](https://github.com/inyotech/forex-vue).

## Endpoints available

A listing of all available currencies and some meta-data

```
GET /currencies

{
    "data": [
        {
            "country_name": "Australia",
            "currency_code": "AUD",
            "currency_name": "Dollar",
            "short_name": "Austrailia"
        },
        {
            "country_name": "Brazil",
            "currency_code": "BRL",
            "currency_name": "Real",
            "short_name": "Brazil"
        },
        {
            "country_name": "Canada",
            "currency_code": "CAD",
            "currency_name": "Dollar",
            "short_name": "Canada"
        },
...
```

Latest exchange rates relative to a base currency specified by :currency_code:

```
GET /latest_rates/base/:currency_code:
```
```
/latest_rates/base/USD
{
    "data": {
        "base": {
            "country_name": "United States",
            "currency_code": "USD",
            "currency_name": "Dollar",
            "flag_image_file_name": "us-t.gif",
            "short_name": "US"
        },
        "latest_rates": [
            {
                "country_name": "Australia",
                "currency_code": "AUD",
                "currency_name": "Dollar",
                "flag_image_file_name": "as-t.gif",
                "rate": 1.4692918013517484,
                "rate_date": "2019-08-02",
                "short_name": "Austrailia"
            },
            {
                "country_name": "Brazil",
                "currency_code": "BRL",
                "currency_name": "Real",
                "flag_image_file_name": "br-t.gif",
                "rate": 3.8789,
                "rate_date": "2019-08-02",
                "short_name": "Brazil"
            },
            {
                "country_name": "Canada",
                "currency_code": "CAD",
                "currency_name": "Dollar",
                "flag_image_file_name": "ca-t.gif",
                "rate": 1.3217,
                "rate_date": "2019-08-02",
                "short_name": "Canada"
            },
...
```

Historic timeseries of exchange rates over the last :months: interval
for a specific :target_code: and :base_code: pair

```
GET /rate_history/base/:base_code:/target/:target_code:/months/:months:'
```
```
/rate_history/base/USD/target/EUR/months/6'
{
    "data": {
        "base": {
            "country_name": "United States",
            "currency_code": "USD",
            "currency_name": "Dollar",
            "flag_image_file_name": "us-t.gif",
            "short_name": "US"
        },
        "target": {
            "country_name": "European Monetary Union",
            "currency_code": "EUR",
            "currency_name": "Euro",
            "flag_image_file_name": "eu.gif",
            "short_name": "EU"
        },
        "rate_history": [
            {
                "rate": 0.8829242450997704,
                "rate_date": "2019-02-08"
            },
            {
                "rate": 0.8867606632969762,
                "rate_date": "2019-02-11"
            },
            {
                "rate": 0.8837044892188053,
                "rate_date": "2019-02-12"
            },
            {
                "rate": 0.885896527285613,
                "rate_date": "2019-02-13"
            },
...
```

## Implementation

This is a python3 code base using the
[Flask](https://palletsprojects.com/p/flask/) web framework.  Database
access is managed through [SQLAlchemy](https://www.sqlalchemy.org/)

## Installation

1. Clone this repository.

```
$ git clone https://github.com/inyotech/forex-flask
```

2. Create and activate a local python virtual environment for python
dependencies.

```
$ python3 -m venv venv

$ source venv/bin/activate
```

3. Install the required packages.

```
$ pip3 install -r requirements.txt
```

4. Configure the instance specific settings by copying the distributed
setitngs directory and editing the containe config.py file.

```
$ cp -r instance.dist/ instance
```

5. Initialize the databases and download historical exchange rates

```
$ FLASK_APP=forex flask init-db
$ FLASK_APP=forex flask load-currencies
$ FLASK_APP=forex flask load-rates
```
