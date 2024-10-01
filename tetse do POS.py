import requests

url = "https://api.userede.com.br/redelabs/merchant-statement/v2/sales"

companyNumbers = [84417072]
subsidiaries = companyNumbers

startdate = "2024-09-10"
enddate = "2024-09-10"

access_token = "eyJraWQiOiI4ZDk0OTg1Ny00MTVmLTRiODEtYjZmNC05OTZhNDY0ODUzMDciLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJodHRwczovL3JsNy1wcmQtYXBpLnVzZXJlZGVjbG91ZC5jb20uYnIvb2F1dGgvdjIiLCJpYXQiOjE3Mjc3MzEyODUsIm5iZiI6MTcyNzczMTI4NSwiYXVkIjoiaHR0cHM6Ly9ybDctcHJkLWFwaS51c2VyZWRlY2xvdWQuY29tLmJyL29hdXRoL3YyIiwiZXhwIjoxNzI3NzMyNzI1LCJhcHAiOiIzMzA1MDI0NjAwMDEyN18xMjczN18wMSIsInZlciI6IjEuMCIsIm9yZyI6ImM4ZmIxYTZhLTA4ZTMtNDVlMC05NWExLTg3NDViYmI3ZWI4YyIsInNjb3BlIjoibWVyY2hhbnQtc3RhdGVtZW50IGZlYXR1cmVfbWVyY2hhbnRfc3RhdGVtZW50IiwiY2VsbCI6IjAiLCJjaG5sIjoiMCIsImNpZCI6IjdiNzliMjY1LTYxYzItNGJiYi04ZTZiLWRhNjQzYzA5YjE4YiIsInVzaWQiOiIxMjczNzQ0Zi0xYWYyLTQyZTYtODEyMi00MjIyZDBlMjlkZDEifQ.mijeMRDRGGUl7FO1Wz5Bq1ishMBRxBFn1dCNPRD0MqPUbNIrQnEHSx4D3HnMH-TC2E5IcYDqwgBqz5GkcTlMH1XCoQ9kpZllUwlgs-HMGeIRdT-up8wf83hTwn8hBEAFvOTqSCPkI9NAdeVVhESP6cZy1hrFXm7Y4TfGA8VS1oNRjOm_CM-lQFrAJGn8qFQoE4pPAS5gu64rWDUys6mouRz7z2ncicRsrUli3xxpBv_kfPc3EiC3iRcqqo07HWNAMFtJWQJFJXeGdbX7I02e9cHQebKYMfR8wyRUI3mhU-TVlmGhQCwslT8Ze81f6j0Ah5xwf2ZEnpWdbqmaViVZnw"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}"
}

all_transactions = []

for companyNumber in companyNumbers:
    params = {
        "startDate": startdate,
        "endDate": enddate,
        "parentCompanyNumber": companyNumber,
        "subsidiaries": [companyNumber],
        "size": 100
    }

    nextKey = None
    hasNextKey = True  # Inicialmente, assumimos que haverá uma próxima página

    while hasNextKey:
        if nextKey:
            params["pageKey"] = nextKey

        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            dados = response.json()

            if 'content' in dados and 'transactions' in dados['content']:
                transactions = dados['content']['transactions']
                all_transactions.extend(transactions)

                print(f"Transações recebidas nesta página: {len(transactions)} para o CompanyNumber {companyNumber}")

                # Verifica se há uma chave 'pageKey' para continuar a paginação
                nextKey = dados['content'].get('nextKey', None)
                hasNextKey = dados.get('hasNextKey', False)  # Verifica se 'hasNextKey' é True para continuar

                if not nextKey:
                    print(f"Chave 'nextKey' não encontrada. Finalizando iteração para o CompanyNumber {companyNumber}.")
                    break
            else:
                print(f"A chave 'transactions' não foi encontrada dentro de 'content' para o CompanyNumber {companyNumber}.")
                break
        else:
            print(f"Erro na requisição para {companyNumber}: {response.status_code}")
            break

# Filtrando os dados para cada transação
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
