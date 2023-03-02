import re
from manager.tts_manager import speak
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession

'''PER PROVARE FUNZIONAMENTO
020460289787 --> bartolini
IC829I289998 | 1C7321I034635 | 1P73C50591948 --> POSTE ITALIANE/SDA
'''
class ShipmentManager:
    def get_carrier(self):
        tracking_number = 'M5630206303'
        carrier = None
        if tracking_number.startswith('1Z'):  # FUNZIONA
            carrier = 'UPS'
        elif tracking_number.startswith('JD'):
            carrier = 'DHL'
        elif re.match(r'^[A-Za-z]{2}[0-9]{9}[A-Za-z]{2}$', tracking_number):
            carrier = 'FedEx'
        elif re.match(r'^M[0-9]{10}$', tracking_number):
            carrier = 'GLS'
            self.get_gls_tracking_info(tracking_number)
        elif re.match(r'^[0-9]{9}$', tracking_number) or re.match(r'^[0-9]{12}$', tracking_number):  # FUNZIONA
            carrier = 'Bartolini'
            self.get_bartolini_tracking_info(tracking_number)
        elif re.match(r'^IT[0-9]{10}$', tracking_number):  # FUNZIONA
            carrier = 'Amazon'
        elif re.match(r'^[1|I][C|P][0-9A-Z]{10}[0-9]*$', tracking_number):
            carrier = 'Poste Italiane'
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
        session = HTMLSession()
        url = f'https://www.poste.it/cerca/index.html#/risultati-spedizioni/{tracking_code}'
        response = session.get(url)
        response.html.render()
        html_content = response.html.html
        soup = BeautifulSoup(html_content, 'html.parser')
        tracking_info = []
        for td in soup.find_all("td"):
            for div in td.find_all("div"):
                text = div.text.strip()
                if re.match(r'\d{2}/\d{2}/\d{4} \d{2}.\d{2}', text):
                    ora = text
                elif text in ['In consegna', 'In transito', 'In lavorazione', 'Presa in carico', 'Partito dal Centro', 'Restituzione al mittente', 'Tracciatura non disponibile', 'Prodotto non registrato', 'consegnata']:
                    stato = text
                else:
                    luogo = text
                    string_track = f"Data e ora: {ora} | Stato: {stato} | Luogo: {luogo}"
                    tracking_info.append(string_track)
        print(tracking_info[-1])

    def get_gls_tracking_info(self, tracking_code):
        locpartenza = tracking_code[:2]
        url = 'https://www.gls-italy.com/index.php?option=com_gls&view=track_e_trace&mode=search&diretto=yes'
        params = {'locpartenza': locpartenza, 'numsped': tracking_code[2:]}
        response = requests.get(url, params=params)
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', {'id': 'esitoSpedizioneRS'})
        tracking_data = []
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            ora = cols[0].text.strip()
            luogo = cols[1].text.strip()
            stato = cols[2].text.strip()
            string_track = f"Data e ora: {ora} | Stato: {stato} | Luogo: {luogo} "
            tracking_data.append(string_track)
        tracking_data.pop(0)
        tracking_data.reverse()
        print(tracking_data[-1])