from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

# Getting the data for each flight
sheet_data = data_manager.get_destination_data()

ORIGIN_CITY_IATA = "IL"

# Filling the IATA codes for the flights
if sheet_data[0]["iataCode"] == "":
    # Listing all the cities without an IATA code
    city_names = [row["city"] for row in sheet_data]
    # Getting the IATA code for those cities
    data_manager.city_codes = flight_search.get_destination_codes(city_names)
    # Updating the Google sheet
    data_manager.update_destination_codes()
    # Updating the data
    sheet_data = data_manager.get_destination_data()

destinations = {
    data["iataCode"]: {
        "id": data["id"],
        "city": data["city"],
        "price": data["lowestPrice"]
    } for data in sheet_data}

# Getting the time we want to check
tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

for destination_code in destinations:
    # Search for flights from Israel to all the cities in the Google sheet from tomorrow and six months from now
    flight = flight_search.check_flights(ORIGIN_CITY_IATA, destination_code, from_time=tomorrow,
                                         to_time=six_month_from_today)
    if flight.stop_overs > 0:
        print(f"{flight.destination_city}: {flight.price}₪, date: {flight.out_date} - {flight.return_date}\n"
              f"{flight.stop_overs} stopovers: {flight.origin_airport} to {flight.stopover_airport},"
              f"via {flight.stopover_airline} airline\n{flight.stopover_airport} to {flight.destination_airport},"
              f" via {flight.airline} airline\n")
    else:
        print(f"{flight.destination_city}: {flight.price}₪, date: {flight.out_date} - {flight.return_date}\n"
              f"direct flight: {flight.origin_airport} to {flight.destination_airport}, via {flight.airline} airline\n")

    # If there aren't any flights to the destination we don't want the program to crash, so we allow it to continue
    if flight is None:
        continue
    # If we found a cheaper price from the one in the Google sheet we will notify about it
    if flight.price < destinations[destination_code]["price"]:
        users = data_manager.get_customer_emails()
        emails = [row["email"] for row in users]
        names = [row["firstName"] for row in users]
        # The message on the cheap flight
        message = f"Low price alert! Only {flight.price}₪ to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}."
        if flight.stop_overs > 0:
            # Adding the numbers of stopovers to the message if there are such
            message += f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."

        notification_manager.send_emails(emails, message)
