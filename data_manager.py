import requests

SHEETY_PRICES_ENDPOINT = "https://api.sheety.co/b5ebc804d910419c17568c2c4b736374/flightDeals/prices"
SHEETY_USERS_ENDPOINT = "https://api.sheety.co/b5ebc804d910419c17568c2c4b736374/flightDeals/users"


class DataManager:

    def __init__(self):
        self.customer_data = None
        self.destination_data = {}

    def get_destination_data(self):
        # Get all the data in the sheet and return it to the main.py.
        response = requests.get(url=SHEETY_PRICES_ENDPOINT)
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_destination_codes(self):
        # Updating the city code in the Google sheet
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}", json=new_data)
            print(response.text)

    def get_customer_emails(self):  # For use in repl.it
        customers_endpoint = SHEETY_USERS_ENDPOINT
        response = requests.get(customers_endpoint)
        data = response.json()
        self.customer_data = data["users"]
        return self.customer_data
