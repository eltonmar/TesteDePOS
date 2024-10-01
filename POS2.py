import requests

url = "https://api.userede.com.br/redelabs/merchant-statement/v2/sales"

companyNumbers = [
    95587632,
    84417072
]

startdate = "2024-07-28"
enddate = "2024-07-28"

access_token = "eyJraWQiOiI4ZDk0OTg1Ny00MTVmLTRiODEtYjZmNC05OTZhNDY0ODUzMDciLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJodHRwczovL3JsNy1wcmQtYXBpLnVzZXJlZGVjbG91ZC5jb20uYnIvb2F1dGgvdjIiLCJpYXQiOjE3Mjc3OTM1MjcsIm5iZiI6MTcyNzc5MzUyNywiYXVkIjoiaHR0cHM6Ly9ybDctcHJkLWFwaS51c2VyZWRlY2xvdWQuY29tLmJyL29hdXRoL3YyIiwiZXhwIjoxNzI3Nzk0OTY3LCJhcHAiOiIzMzA1MDI0NjAwMDEyN18xMjczN18wMSIsInZlciI6IjEuMCIsIm9yZyI6ImM4ZmIxYTZhLTA4ZTMtNDVlMC05NWExLTg3NDViYmI3ZWI4YyIsInNjb3BlIjoibWVyY2hhbnQtc3RhdGVtZW50IGZlYXR1cmVfbWVyY2hhbnRfc3RhdGVtZW50IiwiY2VsbCI6IjAiLCJjaG5sIjoiMCIsImNpZCI6IjdiNzliMjY1LTYxYzItNGJiYi04ZTZiLWRhNjQzYzA5YjE4YiIsInVzaWQiOiIxMjczNzQ0Zi0xYWYyLTQyZTYtODEyMi00MjIyZDBlMjlkZDEifQ.qi4aYkKIRQzYYlmIAQBtbRVl0fuPmZh2l85VamVnpC7OoRqpGVX7HONmVNjvQ-ZgmOth1l3yhXbEmmYPmJX-Zdyl27g3HY6wBHu_uACTKNoOh4Aq1M3S4MkoN8CRtUm49NZ8ou_0Us7R3nSwMsuTc7rUurE19nBAQt02f6MQvupuoEtfQ6bglQzbu6TjCl0HgZpYGuvroXPXnzVi-kxgwUGZEnUQhN9uzGpqLGBWwvnaQJEer3jyuxj8NJVNgS0-md7GTXLWE7Sz0Yip4aLQsNp0V-tot5V1GwZMlk8k39m3JOVQ4C7-QyTgG_3u7VKXhQqLx-iiwF6d1TM5F8amQQ"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}"
}

all_transactions = []

for companyNumber in companyNumbers:
    # Atualize os parâmetros com o companyNumber atual
    params = {
        "startDate": startdate,
        "endDate": enddate,
        "parentCompanyNumber": companyNumber,  # Use apenas um companyNumber por vez
        "subsidiaries": companyNumber,         # Use apenas um companyNumber por vez
        "size": 100,
        "pageKey": None
    }

    while True:
        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            dados = response.json()

            if 'content' in dados and 'transactions' in dados['content']:
                transactions = dados['content']['transactions']
                all_transactions.extend(transactions)

                # Verifica se existe o cursor com hasNextKey igual a True
                if 'cursor' in dados and dados['cursor'].get('hasNextKey', False):
                    next_key = dados['cursor'].get('nextKey', None)
                    if next_key:
                        params['pageKey'] = next_key
                    else:
                        break
                else:
                    break
            else:
                break
        else:
            print(f"Erro na requisição para {companyNumber}: {response.status_code}")
            break


for transaction in all_transactions:
    filtered_data = {
        'movementDate': transaction.get('movementDate', 'N/A'),
        'authorizationCode': transaction.get('authorizationCode', 'N/A'),
        'captureType': transaction.get('captureType', 'N/A'),
        'netAmount': transaction.get('netAmount', 0),
        'amount': transaction.get('amount', 0),
        'status': transaction.get('status', 'N/A'),
        'tid': transaction.get('tid', 0),
        'saleDate': transaction.get('saleDate', 'N/A'),
        'saleHour': transaction.get('saleHour', 'N/A'),
        'nsu': transaction.get('nsu', 'N/A'),
        'device': transaction.get('device', 'N/A'),
        'deviceType': transaction.get('deviceType', 'N/A'),
        'mdrFee': transaction.get('mdrFee', 0),
        'mdrAmount': transaction.get('mdrAmount', 0),
        'netAmount': transaction.get('netAmount', 0),
        'cardNumber': transaction.get('cardNumber', 'N/A'),
        'tokenNumber': transaction.get('tokenNumber', 'N/A'),
        'merchant': {
            'companyNumber': transaction.get('merchant', {}).get('companyNumber', 'N/A'),
            'documentNumber': transaction.get('merchant', {}).get('documentNumber', 'N/A'),
            'documentName': transaction.get('merchant', {}).get('documentName', 'N/A')
        },
        'modality': {
            'type': transaction.get('modality', {}).get('type', 'N/A'),
        }
    }

    print(filtered_data)
