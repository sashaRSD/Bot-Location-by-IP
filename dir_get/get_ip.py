from bs4 import BeautifulSoup
from dir_bot import create_bot
import requests


def scraping(option='IP'):
    try:
        response = requests.get(url='https://iplogger.org/ru/logger/TEUT3HZqZ4Fq/').text
        soup = BeautifulSoup(response, 'lxml')
        if option == 'IP':
            ip = soup.find('div', class_='ip-address').text
            os = soup.find('div', class_='platform').text
            brow = soup.find('div', class_='browser').text
            dataIP = {
                '[IP]': ip,
                '[OS]': os,
                '[Browser]': brow,
            }
            return dataIP
        elif option == 'Time':
            return soup.find('div', class_='ip-time')
        else:
            print('Error name scraping...')
    except requests.exceptions.ConnectionError:
        print('[!] Data loading error!')
        return



def get_info_by_ip(dataIP):
    try:
        response = requests.get(url=f'https://ipinfo.io/{dataIP["[IP]"]}/json').json()
        dataAPI = {
            '[Organization]': response.get('org'),
            '[Country]': f"{response.get('country')}",
            '[Region]': response.get('region'),
            '[City]': response.get('city'),
            '[Zip]': response.get('postal'),
            '[Сoordinates]': f"{response.get('loc')}",
        }
        return dataAPI
    except requests.exceptions.ConnectionError:
        print('[!] Data loading error!')
        return


def get_location(lat, lon):
    try:
        response = requests.get(url=f'https://eu1.locationiq.com/v1/reverse.php?key={create_bot.config["TOKEN"]["token_api_local"]}&'
                                    f'lat={lat}&lon={lon}&format=json').json()
        dataAdr = {
            '[Address]': f"{response['address'].get('postcode')}, "
                         f"{response['address'].get('country')}, "
                         f"{response['address'].get('region')}, "
                         f"{response['address'].get('state')}, "
                         f"{response['address'].get('city')}, "
                         f"{response['address'].get('city_district')},  "
                         f"{response['address'].get('road')}"
        }
        return dataAdr
    except requests.exceptions.ConnectionError:
        print('[!] Data loading error!')
        return


def get_data(dataIP):
    if not dataIP:
        dataIP = scraping()
    dataAPI = get_info_by_ip(dataIP)
    lat, lon = None, None
    if dataAPI['[Сoordinates]'] == 'None':
        dataAdr = {}
    else:
        lat = dataAPI['[Сoordinates]'].split(',')[0]
        lon = dataAPI['[Сoordinates]'].split(',')[1]
        dataAdr = get_location(lat, lon)

    data = dataIP | dataAPI | dataAdr
    info = ''
    for k, v in data.items():
        if k == "[Organization]" or k == "[Address]":
            info += '\n'
        info += f'{k} : {v}\n'
    return [info, lat, lon]
