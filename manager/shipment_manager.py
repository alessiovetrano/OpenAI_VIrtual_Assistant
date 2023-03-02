import re
from manager.tts_manager import speak
import requests
from bs4 import BeautifulSoup

'''PER PROVARE FUNZIONAMENTO

020460289787 --> bartolini
IC829I289998 | 1C7321I034635 | 1P73C50591948 --> POSTE ITALIANE/SDA

'''

class ShipmentManager:
    def get_carrier(self):
        tracking_number = '1P73C50591948'
        carrier = None
        if tracking_number.startswith('1Z'):  # FUNZIONA
            carrier = 'UPS'
        elif tracking_number.startswith('JD'):
            carrier = 'DHL'
        elif re.match(r'^[A-Za-z]{2}[0-9]{9}[A-Za-z]{2}$', tracking_number):
            carrier = 'FedEx'
        elif re.match(r'^[0-9]{13}$', tracking_number):
            carrier = 'GLS'
        elif re.match(r'^[0-9]{9}$', tracking_number) or re.match(r'^[0-9]{12}$', tracking_number):  # FUNZIONA
            carrier = 'Bartolini'
            # print("OK")
            self.get_bartolini_tracking_info(tracking_number)
        elif re.match(r'^IT[0-9]{10}$', tracking_number):  # FUNZIONA
            carrier = 'Amazon'
        #elif re.match(r'^IC[A-Z0-9]{10}$', tracking_number) or re.match(r'^1[C|P][0-9A-Z]{11}$',tracking_number):
        elif re.match(r'^[1|I][C|P][0-9A-Z]{10}[0-9]*$', tracking_number):  # FUNZIONA
            carrier = 'Poste Italiane/SDA'
            self.get_poste_tracking_info(tracking_number)
        print(carrier)

    def get_bartolini_tracking_info(self, tracking_code):
        url = "https://vas.brt.it/vas/sped_det_show.htm?nspediz={}&AnnoSpedizione=2023".format(tracking_code)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', {'class': 'table_stato_dati'})
        tracking_data = []
        rows = table.tbody.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [col.text.strip() for col in cols]
            tracking_data.append(cols)
        latest_tracking_info = tracking_data[1]
        speak("Data: {}, Ora: {}, Luogo: {}, Stato: {}".format(
            latest_tracking_info[0], latest_tracking_info[1], latest_tracking_info[2], latest_tracking_info[3]))

    def get_poste_tracking_info(self, tracking_code):
        url = f"https://www.poste.it/cerca/index.html#/risultati-spedizioni/{tracking_code}"

        response = requests.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')
        print(soup)
        tracking_data = soup.find('div', {'class': 'tracking-data'})

        tracking_info = []
        for item in tracking_data.find_all('div', {'class': 'tracking-row'}):
            time = item.find('div', {'class': 'tracking-time'}).text.strip()
            location = item.find('div', {'class': 'tracking-city'}).text.strip()
            status = item.find('div', {'class': 'tracking-description'}).text.strip()
            tracking_info.append([time, location, status])

        for info in tracking_info:
            print("Data e ora: {}\nLuogo: {}\nStato: {}\n".format(info[0], info[1], info[2]))
