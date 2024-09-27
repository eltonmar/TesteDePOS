import requests

url = "https://api.userede.com.br/redelabs/merchant-statement/v2/sales"

companyNumbers = [84417072]
subsidiaries = companyNumbers

startdate = "2024-09-10"
enddate = "2024-09-10"

access_token = "eyJraWQiOiI4ZDk0OTg1Ny00MTVmLTRiODEtYjZmNC05OTZhNDY0ODUzMDciLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJodHRwczovL3JsNy1wcmQtYXBpLnVzZXJlZGVjbG91ZC5jb20uYnIvb2F1dGgvdjIiLCJpYXQiOjE3Mjc0NjkxMjMsIm5iZiI6MTcyNzQ2OTEyMywiYXVkIjoiaHR0cHM6Ly9ybDctcHJkLWFwaS51c2VyZWRlY2xvdWQuY29tLmJyL29hdXRoL3YyIiwiZXhwIjoxNzI3NDcwNTYzLCJhcHAiOiIzMzA1MDI0NjAwMDEyN18xMjczN18wMSIsInZlciI6IjEuMCIsIm9yZyI6ImM4ZmIxYTZhLTA4ZTMtNDVlMC05NWExLTg3NDViYmI3ZWI4YyIsInNjb3BlIjoibWVyY2hhbnQtc3RhdGVtZW50IGZlYXR1cmVfbWVyY2hhbnRfc3RhdGVtZW50IiwiY2VsbCI6IjAiLCJjaG5sIjoiMCIsImNpZCI6IjdiNzliMjY1LTYxYzItNGJiYi04ZTZiLWRhNjQzYzA5YjE4YiIsInVzaWQiOiIxMjczNzQ0Zi0xYWYyLTQyZTYtODEyMi00MjIyZDBlMjlkZDEifQ.gNqNWVxEEFxUD_qphLK-1E1PJoDfORdruShJ2J7yIWNYTxV6b9AwQXQ8s6lSmFDKeSnG858srSF0_N2x9cqfqqkizqOnnmL7mT0tuEdCzvXE9MmKHLxrxPlDqNiaXUxNSxzTFikVoKknSFOG0zGrzCw5RDxKapuMgeEhETnDQmbybvAnWBOVZancxslNnmvifEtb-KdI2hzm24dWLNGIclBLTQgLqvqA7Y_vnp_3LZJ7OBAWwsEkQK-1FuwetONVFi7fyNDkLmZ1l5UxXbWStDPX793YjgNYkbIwDq6tlE4g1rdS99hzSOXEaJZ5-0LCf-yHrzAxdIxpJ52NoBTu4w"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}"
}

params = {
    "startDate": startdate,
    "endDate": enddate,
    "parentCompanyNumber": companyNumbers,
    "subsidiaries": subsidiaries,
    "size": 100
}

all_transactions = []
nextKey = ""


while True:

    if nextKey:
        params["pageKey"] = nextKey
    else:
        params.pop("pageKey", None)

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        dados = response.json()
        print(dados)
        if 'content' in dados and 'transactions' in dados['content']:
            transactions = dados['content']['transactions']
            all_transactions.extend(transactions)

            print(f"Transações recebidas nesta página: {len(transactions)}")

            if 'nextKey' in dados:
                nextKey = dados['nextKey']
                print(f"Próxima chave de paginação encontrada: {nextKey}")
            else:
                print("Chave 'nextKey' não foi encontrada. Finalizando iteração.")
                break

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


print(f"Total de transações: {len(all_transactions)}")

