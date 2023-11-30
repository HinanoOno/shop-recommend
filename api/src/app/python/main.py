import requests
import json
import sys

def search_hotpepper(keyword):
    URL = 'http://webservice.recruit.co.jp/hotpepper/gourmet/v1/'
    API_KEY = '18ab40f6701bc7aa'

    params = {
        'key': API_KEY,
        'keyword': keyword,
        'format': 'json'
    }

    response = requests.get(URL, params=params)

    if response.status_code == 200:
        data = response.json()
        dataset = []

        for shop in data['results']['shop']:
            shop_data = {
                'id': shop['id'],
                'name': shop['name'],
                'address': shop['address'],
                'logo_image': shop['logo_image'],
                'genre': shop['genre']['name'],
                'url': shop['urls']['pc'],
                'photo': shop['photo']['pc']
                # その他の必要な属性を追加
            }
            dataset.append(shop_data)

        # データセットをJSON形式で表示
        print(json.dumps(dataset))
    else:
        print(f'Error {response.status_code} - {response.text}')

if __name__ == "__main__":
    keyword = sys.argv[1] if len(sys.argv) > 1 else '俺のフレンチ'

    # 検索関数を呼び出し
    search_hotpepper(keyword)
