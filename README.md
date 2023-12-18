# Flight Price Tracker
Authored by Adam Shay

## Description
This Python project tracks flight prices and notifies users when there's a significant price drop for their desired destinations.
The program utilizes the Tequila API for flight data and Google Sheets via the Sheety API for data storage.

## Project Components
### 1. data_manager.py
* **DataManager Class:** Handles communication with the Sheety API to retrieve and update flight prices and user data.

### 2. flight_search.py
* **FlightSearch Class:** Utilizes the Tequila API to get IATA codes for city names and search for available flights between two locations.

### 3. notification_manager.py
* **NotificationManager Class:** Sends notifications to users via email and SMS using the Twilio API. **Requires Twilio account credentials**.

### 4. flight_data.py
* **FlightData Class:** Represents the data structure for flight information, including price, origin, destination, dates, and stopover details.

### 5. main.py
* **The main script:**
  * Retrieves destination data from Google Sheets.
  * Checks for missing IATA codes and updates them using the Tequila API.
  * Searches for flights from the specified origin city to each destination within the next six months.
  * Notifies users via email if a cheaper flight is found.

## How to Use
1. Set up a Google Sheet with destination data and user information.
2. Obtain API keys for Tequila and Twilio and set them as environment variables.
3. Run the main.py script to check for flight prices and notify users of potential savings.

## Environment Variables
* TEQUILA_API_KEY: API key for the Tequila API.
* TWILIO_SID: Twilio account SID.
* TWILIO_AUTH_TOKEN: Twilio authentication token.
* TWILIO_VIRTUAL_NUMBER: Twilio virtual phone number.
* TWILIO_VERIFIED_NUMBER: User's verified phone number.
* MY_EMAIL: Sender's email address for sending notifications.
* MY_PASSWORD: Sender's email password.

**Note:** This project is designed for educational purposes and may require additional configuration for production use. Use responsibly and be mindful of API usage limits.
