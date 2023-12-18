import os
import requests
from flight_data import FlightData

TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
TEQUILA_API_KEY = os.getenv("TEQUILA_API_KEY")


class FlightSearch:

    def __init__(self):
        self.city_codes = []

    def get_destination_codes(self, city_name):
        # Getting the IATA code from the Tequila API
        location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        headers = {"apikey": TEQUILA_API_KEY}
        for city in city_name:
            # Passing required params
            query = {"term": city, "location_types": "city"}
            response = requests.get(url=location_endpoint, headers=headers, params=query)
            # From the request we will take the IATA code for the city provided
            results = response.json()["locations"]
            code = results[0]["code"]
            self.city_codes.append(code)
        return self.city_codes

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        headers = {"apikey": TEQUILA_API_KEY}
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            # The range for the outbound flight departure
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            # The range for the stay in the destination
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            # Get the cheapest flight for the destination
            "one_for_city": 1,
            # Only direct flights
            "max_stopovers": 0,
            "curr": "ILS"
        }

        response = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search", headers=headers, params=query)

        try:
            # We check if all the params are valid and then send them to be recorded
            data = response.json()["data"][0]
        except IndexError:
            # If the destination we want doesn't have a direct flight we will check again with 1 stopover
            query["max_stopovers"] = 1
            response = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search", headers=headers, params=query)
            data = response.json()["data"][0]

            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                airline=data["route"][0]["airline"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][2]["local_departure"].split("T")[0],
                stop_overs=1,
                via_city=data["route"][1]["cityTo"],
                stopover_airline=data["route"][1]["airline"],
                stopover_airport=data["route"][1]["flyTo"]
            )
            return flight_data
        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                airline=data["route"][0]["airline"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0]
            )
            return flight_data
