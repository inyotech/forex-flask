#!/bin/bash

base=$(dirname $(readlink -f "$0"))/../

flask=${base}/venv/bin/flask

cd $base

export FLASK_APP=forex

$flask load-rates
$flask load-stories

