from __future__ import print_function

import os
from datetime import datetime
from urllib2 import urlopen
import boto3
try:
    import simplejson as json
except:
    import json

BASE_URL = "https://api.guildwars2.com/v2/"
GEMS_TO_COINS = "commerce/exchange/gems?quantity="
COINS_TO_GEMS = "commerce/exchange/coins?quantity="
client = boto3.client('cloudwatch')
TIME = datetime.now()
G2C = [10, 50, 100, 500, 1000]
C2G = [1000000, 500000, 1000000, 5000000, 10000000]

def post_cloudwatch_data(metric, dimension_name, dimension_value, data):
    namespace = "gw2Currency"
    metric_data = [{
        'MetricName': metric,
        'Dimensions': [
        {
            'Name': dimension_name,
            'Value': str(dimension_value)
        }
        ],
        'Timestamp': TIME,
        'Value': data
    }]
    response = client.put_metric_data(Namespace=namespace, MetricData=metric_data)
    return response

def call_api(uri):
    """ Call api and return json """
    response = urlopen(uri)
    return json.loads(response.read())


def get_gw2_gold_to_gems(coins):
    uri = BASE_URL + COINS_TO_GEMS + str(coins)
    return call_api(uri)['coins_per_gem']


def get_gw2_gems_to_gold(gems):
    uri = BASE_URL + GEMS_TO_COINS + str(gems)
    return call_api(uri)['coins_per_gem']


def lambda_handler(event, context):
    for dimension in G2C:
        response = post_cloudwatch_data('coins_gems_to_coins', "Coins", dimension, get_gw2_gems_to_gold(dimension))
        print(response)
    for dimension in C2G:
        response = post_cloudwatch_data('coins_coins_to_gems', "Coins", dimension, get_gw2_gold_to_gems(dimension))
        print(response)

if __name__ == "__main__":
    lambda_handler(1,2)
