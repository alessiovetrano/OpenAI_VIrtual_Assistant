import re

class ShipmentManager:
    def get_carrier(self):
        tracking_number = '02046028'
        carrier = None
        if tracking_number.startswith('1Z'): #FUNZIONA
            carrier = 'UPS'
        elif tracking_number.startswith('JD'):
            carrier = 'DHL'
        elif re.match(r'^[A-Za-z]{2}[0-9]{9}[A-Za-z]{2}$',tracking_number):
            carrier = 'FedEx'
        elif re.match(r'^[0-9]{13}$',tracking_number):
            carrier = 'GLS'
        elif re.match(r'^[0-9]{9}$',tracking_number) or re.match(r'^[0-9]{12}$', tracking_number): #FUNZIONA
            carrier = 'Bartolini'
        elif re.match(r'^IT[0-9]{10}$', tracking_number): #FUNZIONA
            carrier = 'Amazon'
        elif re.match(r'^1[C|P][0-9A-Z][A-Z0-9]{4}[A-Z][0-9]{5}$', tracking_number) or re.match(r'^IC[A-Z0-9]{7}$',tracking_number): #non riesco a trovare pattern. Codici SDA/Poste esempio:'IC829I289998','1C7321I034635','1P73C50591948'
            carrier = 'Poste Italiane/SDA'
        print(carrier)

