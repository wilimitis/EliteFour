import boto3
import csv
import json

ONLINE = False
VERBOSE = False

def build_put_nature(nature, description):
    return {
        'PutRequest': {
            'Item': {
                'nature': {
                    'S': nature
                },
                'description': {
                    'S': description
                }
            }
        }
    }

def parse_nature(row):
    return build_put_nature(row[0], row[1])

def build_put_pokemon(pokemon):
    return {
        'PutRequest': {
            'Item': {
                'name': {
                    'S': pokemon['name']
                },
                'height': {
                    'S': pokemon['height']
                },
                'weight': {
                    'S': pokemon['weight']
                }
            }
        }
    }

def write_batch(client, table, items, batch):
    print "batch {0} size {1}".format(batch, len(items))
    request_items = {}
    request_items[table] = items
    if ONLINE is True:
        client.batch_write_item(RequestItems = request_items)
    if VERBOSE is True:
        print(request_items)

def upload(client, table, csv_location, parse):
    items = []
    batch = 1
    count = 0

    with open(csv_location) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            item = parse(row)
            items.append(item)
            count += 1

            if count % 25 == 0:
                write_batch(client, table, items, batch)
                batch += 1
                items = []

    write_batch(client, table, items, batch)

def run():

    with open('../../access/aws-sdk_config.json') as access_file:
        access_data = json.load(access_file)

    client = boto3.client(
        'dynamodb',
        region_name = access_data['region'],
        aws_access_key_id = access_data['accessKeyId'],
        aws_secret_access_key = access_data['secretAccessKey']
    )

    #upload(client, 'EliteFour-Natures', '../../../data/natures.csv', parse_nature)

    upload(client, 'EliteFour-Pokemon', '../../data/clean/pokemon_clean.csv', build_put_pokemon)

run()
