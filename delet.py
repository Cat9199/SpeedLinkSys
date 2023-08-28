codes = [
    'ECS21510496',
    'ECS21511792',
    'ECS21511793',
    'ECS21511794',
    'ECS21511795',
    'ECS21511796',
    'ECS21511797',
    'ECS21511798',
    'ECS21511799',
    'ECS21511800',
    'ECS21511801',
    'ECS21511802',
    'ECS21512057'

]

reqUrl = "https://vsoftapi.com-eg.net/api/ClientUsers/V6/CancelShipment"
import requests
import json
headersList = {
        "CompanyID": "191307",
        "AccessToken": "C4DF9C2F-D297-48D4-88FF-C36E66C0B773",
        "Language": "en",
        "Content-Type": "application/json" 
}
for x in codes:
    payload = {
        "awb": x
    }
    response = requests.post(reqUrl, json=payload, headers=headersList)
    print(response.text)