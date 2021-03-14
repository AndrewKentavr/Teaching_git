import requests
from globals import Globals
import sys


def getImage():
    Globals.params['spn'] = f'{Globals.delta},{Globals.delta}'
    Globals.params['ll'] = f'{Globals.longitude},{Globals.latitude}'
    response = requests.get(Globals.map_request, params=Globals.params)

    if not response:
        print("Ошибка выполнения запроса:")
        print(Globals.map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    # Запишем полученное изображение в файл.
    Globals.map_file = "map.png"
    with open(Globals.map_file, "wb") as file:
        file.write(response.content)


def geocoder_response(text):
    req = 'https://geocode-maps.yandex.ru/1.x/'
    geocoder_params = {'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
                       'geocode': text,
                       'format': 'json'}
    response = requests.get(req, params=geocoder_params)
    try:
        assert response
        json_response = response.json()
        print(json_response)
        try:
            cat_big = []
            root = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            cat = [float(element) for element in root["Point"]["pos"].split()]
            cat_big.append(cat)
            cat = root["metaDataProperty"]["GeocoderMetaData"]["AddressDetails"]["Country"]["AddressLine"]
            cat_big.append(cat)
            tola = root["metaDataProperty"]["GeocoderMetaData"]["AddressDetails"]["Country"]["AdministrativeArea"]
            tola_2 = tola['Locality']['Thoroughfare']['Premise']['PostalCode']['PostalCodeNumber']
            # вольная улица, дом 3
            print(tola_2)
            return cat_big
        except IndexError:
            pass
    except AssertionError:
        pass
