import requests
import json
import WazeRouteCalculator
import logging

class WazeManager:
    def get_traffico_info(self):
        logger = logging.getLogger('WazeRouteCalculator.WazeRouteCalculator')
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        logger.addHandler(handler)

        from_address = 'Piazza Carlo III, Napoli, NA'
        to_address = 'Via Toledo, Napoli, NA'
        region = 'EU'
        route = WazeRouteCalculator.WazeRouteCalculator(from_address, to_address,region)
        route_info = route.calc_route_info()
        print(f"Il tempo per percorre la distanza di {route_info[1]} kilometri attualmente tra {from_address} e {to_address} è di {route_info[0]} minuti") #DA RIVEDERE, FUNZIONA SOLO IN ITALIA