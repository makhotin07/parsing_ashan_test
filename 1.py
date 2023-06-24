import requests
import pandas as pd
import json

URL = 'https://www.auchan.ru/catalog/moloko-syr-yayca/'
API = 'https://api.retailrocket.ru/api/2.0/recommendation/popular/5ecce55697a525075c900196/?&stockId=1&categoryIds=&categoryPaths=%D0%9C%D0%BE%D0%BB%D0%BE%D1%87%D0%BD%D1%8B%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D1%8B%2C%20%D1%8F%D0%B9%D1%86%D0%B0&session=6485e83fcd70f2a251a56a78&pvid=760676073426111&isDebug=false&format=json'
FILENAME = 'auchan-output'

headers = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
}


def parse(url, headers):
    response = requests.get(url, headers=headers)
    print(response)

    with open('auchan-initial-data.json', 'w', encoding='utf-8') as file:
        json.dump(response.json(), file)



def get_data(json_file):
    result_to_csv = {
        'product_id': [],
        'name': [],
        'link': [],
        'regular_price': [],
        'promo_price': [],
        'brand': [],
    }

    result_to_json = []

    with open(json_file, 'r', encoding='utf-8') as file:
        json_ = json.load(file)

    for data in json_:
        result_to_csv['product_id'].append(data['ItemId'])
        result_to_csv['name'].append(data['Name'])
        result_to_csv['link'].append(data['Url'])
        result_to_csv['regular_price'].append(data['OldPrice'])
        result_to_csv['promo_price'].append(data['Price'])
        result_to_csv['brand'].append(data['Vendor'])

        result_to_json.append({
            'product_id': data['ItemId'],
            'name': data['Name'],
            'link': data['Url'],
            'regular_price': data['OldPrice'],
            'promo_price': data['Price'],
            'brand': data['Vendor'],
        })

    return result_to_csv, result_to_json


def save_to_json(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


parse(API, headers)
products_to_csv, products_to_json = get_data('auchan-initial-data.json')

df = pd.DataFrame(products_to_csv)
df.to_csv(f'{FILENAME}.csv', index=False)
save_to_json(products_to_json, f'{FILENAME}.json')