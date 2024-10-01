import requests

url = "https://api.userede.com.br/redelabs/merchant-statement/v2/sales"

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
            96618710, 96570059, 96620382, 96570857, 96570059, 96733675, 96781009, 96781122,
            96781742, 96781955, 96822074, 96878169, 96877944, 96943769

        ]

startdate = "2024-09-30"
enddate = "2024-09-30"

access_token = "eyJraWQiOiI4ZDk0OTg1Ny00MTVmLTRiODEtYjZmNC05OTZhNDY0ODUzMDciLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJodHRwczovL3JsNy1wcmQtYXBpLnVzZXJlZGVjbG91ZC5jb20uYnIvb2F1dGgvdjIiLCJpYXQiOjE3Mjc3OTk3MjQsIm5iZiI6MTcyNzc5OTcyNCwiYXVkIjoiaHR0cHM6Ly9ybDctcHJkLWFwaS51c2VyZWRlY2xvdWQuY29tLmJyL29hdXRoL3YyIiwiZXhwIjoxNzI3ODAxMTY0LCJhcHAiOiIzMzA1MDI0NjAwMDEyN18xMjczN18wMSIsInZlciI6IjEuMCIsIm9yZyI6ImM4ZmIxYTZhLTA4ZTMtNDVlMC05NWExLTg3NDViYmI3ZWI4YyIsInNjb3BlIjoibWVyY2hhbnQtc3RhdGVtZW50IGZlYXR1cmVfbWVyY2hhbnRfc3RhdGVtZW50IiwiY2VsbCI6IjAiLCJjaG5sIjoiMCIsImNpZCI6IjdiNzliMjY1LTYxYzItNGJiYi04ZTZiLWRhNjQzYzA5YjE4YiIsInVzaWQiOiIxMjczNzQ0Zi0xYWYyLTQyZTYtODEyMi00MjIyZDBlMjlkZDEifQ.YA-LDIMMa6Cd0VVd3iTGgBdSlQB68qyDnEZAiuV4zaOGay6l3QZ0X4mIjvIG7ZsL9CMS3Qc2ifhRvdegjXHKfddwaoIyTP2ilr7adMPVthS-oDJxQxEQy7VB91Z5GxhRpFYaxf-AZAfMmEupXRC04IyuTbyyh5RYPR9vRufO5dnszyVpbuvlKXmNd6zWfaR9HpGZi_5LGv4StHrtQHapFZseFWk0w3wTRjmRQCO9Z2HCVDsfc5FmFhGhqPqvOhz9dqg5uxQb4LWUkmFcHnfuMkDMt0rQLdQDXM_Z7skFuMyjkZ3mXLNWM9Jj7F0lLeC0njMbEH21KPa_J3DqKY98LA"


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
        "subsidiaries": companyNumber,
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
