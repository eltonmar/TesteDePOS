import requests

url = "https://api.userede.com.br/redelabs/merchant-statement/v2/sales"

companyNumbers = [86819747]
subsidiaries = companyNumbers

startdate = "2024-09-25"
enddate = "2024-09-25"

access_token = "eyJraWQiOiI4ZDk0OTg1Ny00MTVmLTRiODEtYjZmNC05OTZhNDY0ODUzMDciLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJodHRwczovL3JsNy1wcmQtYXBpLnVzZXJlZGVjbG91ZC5jb20uYnIvb2F1dGgvdjIiLCJpYXQiOjE3MjczODU2ODQsIm5iZiI6MTcyNzM4NTY4NCwiYXVkIjoiaHR0cHM6Ly9ybDctcHJkLWFwaS51c2VyZWRlY2xvdWQuY29tLmJyL29hdXRoL3YyIiwiZXhwIjoxNzI3Mzg3MTI0LCJhcHAiOiIzMzA1MDI0NjAwMDEyN18xMjczN18wMSIsInZlciI6IjEuMCIsIm9yZyI6ImM4ZmIxYTZhLTA4ZTMtNDVlMC05NWExLTg3NDViYmI3ZWI4YyIsInNjb3BlIjoibWVyY2hhbnQtc3RhdGVtZW50IGZlYXR1cmVfbWVyY2hhbnRfc3RhdGVtZW50IiwiY2VsbCI6IjAiLCJjaG5sIjoiMCIsImNpZCI6IjdiNzliMjY1LTYxYzItNGJiYi04ZTZiLWRhNjQzYzA5YjE4YiIsInVzaWQiOiIxMjczNzQ0Zi0xYWYyLTQyZTYtODEyMi00MjIyZDBlMjlkZDEifQ.A5t0WgTvRcOsDzc0El6AnPtg6KddbSlI8TZFqGZ-4QfLdyCJK3C2q4Tsi8ZORlRb7tYlbpJKTw0w5NCwPrLciVJpggh5l2bifiAaxqH-XHbM1Yw1LnpiHJPR6x0e48gLhlNeI3Ant1lncUdBSp2LhE2RP5kPonzpP_1Qj2MUIxwE8ybF2PnXBJ-0W70C8Fy6UbEIizcD9bE0t6g8TnKxgorf-PDtUAFsMh25f0use5feVQ6SacvMrk4uoUcPwqcwJ15fL1k9T3C0bywMpDIK5lcH9CCp0ESWUxSGgFCwJKnfXYClqnNfjlonmaeBehnE6tllZ_x0TiYraaehsA_lNQ"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}"
}

params = {
    "startDate": startdate,
    "endDate": enddate,
    "parentCompanyNumber": companyNumbers,
    "subsidiaries": subsidiaries,
    "page": 1,
    "size": 100
}

all_transactions = []

while True:
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:

        dados = response.json()

        if 'content' in dados and 'transactions' in dados['content']:
            transactions = dados['content']['transactions']
            all_transactions.extend(transactions)

            if len(transactions) < params["size"]:
                break
            else:
                params["page"] += 1
        else:
            print("A chave 'transactions' não foi encontrada dentro de 'content'.")
            break
    else:
        print(f"Erro na requisição para {companyNumbers}: {response.status_code}")
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
