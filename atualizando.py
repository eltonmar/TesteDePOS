import requests
import openpyxl

def get_tokens():
    url = "https://api.userede.com.br/redelabs/oauth/token"
    body = {
        "grant_type": "password",
        "username": "elton.marinho@bagaggio.com.br",
        "password": ":5@A9hPr9-Po"
    }

    headers = {
        "Authorization": "Basic N2I3OWIyNjUtNjFjMi00YmJiLThlNmItZGE2NDNjMDliMThiOjI3bWJXMnpDeFE=",
    }

    response = requests.post(url, data=body, headers=headers)

    if response.status_code == 200:
        data = response.json()
        access_token = data.get("access_token", "")
        refresh_token = data.get("refresh_token", "")
        return access_token, refresh_token
    else:
        print("Falha na obtenção do token. Status code:", response.status_code)
        return None, None


def refresh_access_token(refresh_token):
    url = "https://api.userede.com.br/redelabs/oauth/token"
    body = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    headers = {
        "Authorization": "Basic N2I3OWIyNjUtNjFjMi00YmJiLThlNmItZGE2NDNjMDliMThiOjI3bWJXMnpDeFE="
    }

    response = requests.post(url, data=body, headers=headers)

    if response.status_code == 200:
        data = response.json()
        access_token = data.get("access_token", "")
        new_refresh_token = data.get("refresh_token", "")
        return access_token, new_refresh_token
    else:
        print("Falha na atualização do token. Status code:", response.status_code)
        return None, None

def fetch_sales_transactions(access_token, refresh_token, start_date, end_date, company_numbers, worksheet):
    url = "https://api.userede.com.br/redelabs/merchant-statement/v2/sales"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    row_number = 2
    for company_number in company_numbers:
        params = {
            "startDate": start_date,
            "endDate": end_date,
            "parentCompanyNumber": company_number,
            "subsidiaries": company_number,
            "size": 100,
            "pageKey": None
        }

        while True:
            response = requests.get(url, params=params, headers=headers)

            if response.status_code == 401:
                print("Access token expirado, atualizando o token...")
                access_token, refresh_token = refresh_access_token(refresh_token)
                if access_token:
                    headers["Authorization"] = f"Bearer {access_token}"
                    continue
                else:
                    print(f"Falha ao atualizar o token para {company_number}.")
                    break

            if response.status_code == 200:
                data = response.json()

                if 'content' in data and 'transactions' in data['content']:
                    transactions = data['content']['transactions']

                    for transaction in transactions:
                        filtered_data = process_transaction(transaction)

                        write_transaction_to_excel(worksheet, filtered_data, row_number)
                        row_number += 1

                    if 'cursor' in data and data['cursor'].get('hasNextKey', False):
                        next_key = data['cursor'].get('nextKey', None)
                        params['pageKey'] = next_key
                    else:
                        break
                else:
                    break
            else:
                print(f"Erro na requisição para {company_number}: {response.status_code}")
                break

def process_transaction(transaction):
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
        'companyNumber': transaction.get('merchant', {}).get('companyNumber', 'N/A'),
        'documentName': transaction.get('merchant', {}).get('documentName', 'N/A'),
        'modalityType': transaction.get('modality', {}).get('type', 'N/A')
    }
    return filtered_data


def write_transaction_to_excel(worksheet, transaction_data, row):
    worksheet[f'A{row}'] = transaction_data['movementDate']
    worksheet[f'B{row}'] = transaction_data['authorizationCode']
    worksheet[f'C{row}'] = transaction_data['captureType']
    worksheet[f'D{row}'] = transaction_data['netAmount']
    worksheet[f'E{row}'] = transaction_data['amount']
    worksheet[f'F{row}'] = transaction_data['status']
    worksheet[f'G{row}'] = transaction_data['tid']
    worksheet[f'H{row}'] = transaction_data['saleDate']
    worksheet[f'I{row}'] = transaction_data['saleHour']
    worksheet[f'J{row}'] = transaction_data['nsu']
    worksheet[f'K{row}'] = transaction_data['device']
    worksheet[f'L{row}'] = transaction_data['deviceType']
    worksheet[f'M{row}'] = transaction_data['mdrFee']
    worksheet[f'N{row}'] = transaction_data['mdrAmount']
    worksheet[f'O{row}'] = transaction_data['cardNumber']
    worksheet[f'P{row}'] = transaction_data['tokenNumber']
    worksheet[f'Q{row}'] = transaction_data['companyNumber']
    worksheet[f'R{row}'] = transaction_data['documentName']
    worksheet[f'S{row}'] = transaction_data['modalityType']


# Obter tokens

access_token, refresh_token = get_tokens()

companyNumbers = [
    3016412, 84232633, 84232668, 32143460, 3111628, 73938807, 32144024, 32144261,
    95515208, 75539098, 87805405, 73986313, 95400206, 32144890, 85788600, 32144970,
    32145128, 32145268, 92320384, 32145403, 32145454, 32145497, 32145586, 32145667,
    23816090, 84417072, 84232706, 33810311, 32145772, 84232749, 86819747, 84233052,
    84233079, 91494117, 84382104, 91289548, 84233117, 86006118, 86011553, 84233184,
    75538695, 95515216, 73887145, 86930168, 95515224, 75527073, 95515232, 73986461,
    88244296, 95515240, 75557487, 82370591, 87814773, 95515267, 73836281, 87815397,
    84232897, 86982109, 84232935, 195618, 86820052, 95102450, 95515275, 75539330,
    91590663, 95593543, 75539268, 89351746, 95515283, 75557584, 84233028, 82370680,
    82370702, 88244202, 88244440, 32145330, 82370583, 82370605, 75539527, 93419244,
    95515291, 75557614, 95515313, 82370664, 82370494, 75557525, 95593659, 75539535,
    83830200, 94959579, 83830030, 95207864, 82370648, 82370672, 94959455, 82370699,
    95006346, 82370737, 95367217, 82370753, 82370788, 82370621, 82370710, 82370745,
    82370923, 95207872, 82370800, 82370850, 95515321, 82370940, 95515330, 82370885,
    82370907, 83928731, 83928774, 83928790, 83928812, 83967460, 83885625, 84037857,
    84013842, 88244580, 88645940, 88646203, 88646351, 89162420, 89339622, 89322908,
    89912764, 89910354, 90246225, 91489520, 91808316, 91917697, 92069207, 92761860,
    92969992, 92953298, 93053827, 93530218, 95515356, 93569580, 93717393, 95515372,
    95515402, 95515410, 95515445, 95515496, 95515500, 95008292, 95515518, 95515526,
    95207880, 95515534, 95515542, 95515550, 94959331, 95008500, 95515569, 95515577,
    94959102, 95008845, 94959072, 94959056, 95012095, 94959013, 95207899, 95562052,
    95370234, 95703330, 95634380, 95562362, 95645063, 95944168, 95770941, 57040117,
    85544426, 58460560, 66359732, 85544388, 82445249, 95367225, 86891740, 73392642,
    72982217, 85485993, 82445222, 94764182, 82445265, 95400729, 85544680, 88450295,
    88437795, 88729222, 90104951, 90092147, 90086155, 91581869, 91861675, 91860849,
    92054668, 92175473, 92124410, 92117791, 92223389, 92414443, 94338442, 94003114,
    93889100, 94234906, 94090483, 94212732, 94572593, 94434107, 94378398, 94852804,
    94543828, 95400460, 94765774, 95071512, 95071431, 95593446, 95367160, 95587543,
    95587632, 95645403, 95425764, 95477756, 95743332, 95747761, 95817930, 95927549,
    95927409, 95946039, 95945652, 96106468, 95946179, 96009454, 96107375, 96194766,
    96216964, 96276134, 96276231, 96286130, 96286164, 96286202, 96286237, 96299843,
    96296941, 96310073, 96313510, 96299754, 96301058, 96439629, 96533641, 96533951,
    96292504, 96547863, 96533161, 96485183, 96533366, 96402725, 96402440, 96400420,
    96618710, 96570059, 96620382, 96570857, 96733675, 96781009, 96781122,
    96781742, 96781955, 96822074, 96878169, 96877944, 96943769
]


if access_token:
    start_date = "2024-10-15"
    end_date = "2024-10-15"

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Transações"

    headers = ['Data Movimentação', 'Código Autorização', 'Tipo Captura', 'Valor Líquido', 'Valor Total', 'Status',
               'TID', 'Data Venda', 'Hora Venda', 'NSU', 'Dispositivo', 'Tipo Dispositivo', 'Taxa MDR', 'Valor MDR',
               'Número Cartão', 'Número Token', 'Número Empresa', 'Nome Documento', 'Tipo Modalidade']

    for col_num, header in enumerate(headers, 1):
        sheet.cell(row=1, column=col_num, value=header)

    # Buscar transações de vendas
    fetch_sales_transactions(access_token, refresh_token, start_date, end_date, companyNumbers, sheet)

    workbook.save("C:\\Users\\BG-PROVISORIO\\Desktop\\Vendas\\Transações.xlsx")
    print("Transações foram salvas no arquivo 'transacoes_vendas.xlsx'.")
else:
    print("Não foi possível obter o token de acesso.")
