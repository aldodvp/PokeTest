import os
from Google import Create_Service
from datetime import datetime
import requests

poks = [
    ['ID', 'Name', 'URL', 'TimeStamp']
]

def pokedex(url='https://pokeapi.co/api/v2/pokemon/', offset=0):
    args = {'offset': offset} if offset else {}
  
    response = requests.get(url, params=args)
    if response.status_code == 200:
    
        payload = response.json()
        results = payload.get('results', [])

        if results:
            for pokemon in results:
                url = pokemon ['url']
                temp = url.split("/")
                id= temp[6]
                name = pokemon['name']
                timestamp = (datetime.now().strftime('%Y-%m-%d - %H:%M:%S'))
                poks.append([id,name,url,timestamp])
                print(id, name, url, timestamp )

        next = input("Next page? [Y/N]")
        if next == ('y'):
            pokedex(offset=offset+20)
 
if __name__ == '__main__':
    url =  'https://pokeapi.co/api/v2/pokemon/'
    pokedex()
    CLIENT_SECRET_FILE = 'client_secret.json'
    API_NAME = 'sheets'
    API_VERSION = 'v4'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    spreadsheet_id = '1jrdWy6kOHzz9gjEuqgJFUnpnYnDb19-zB77XWbMOpeg'


    cell_range_insert = 'A1'
    value_range_body = {
        'majorDimension': 'ROWS',
        'values': poks
    }
    
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        valueInputOption='USER_ENTERED',
        range=cell_range_insert,
        body=value_range_body
    ).execute()
