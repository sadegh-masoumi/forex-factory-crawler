import requests
import os

from bs4 import BeautifulSoup
from telegram import Telegram


def fetch_forex_factory_economic_calendar():
    url = 'https://www.forexfactory.com/calendar.php'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)

    print(f"{response.status_code} 🏁")

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        event_rows = soup.find_all('tr', class_='calendar__row')
        calendar_data = []
        # print(event_rows)
        for row in event_rows:
            try:
                event_time = row.find(
                    'td', class_='calendar__time').text.strip()
                event_currency = row.find(
                    'td', class_='calendar__currency').text.strip()
                event_impact = row.find(
                    'td', class_='calendar__impact').span['title']
                event_description = row.find(
                    'td', class_='calendar__event').text.strip()
                event_actual = row.find(
                    'td', class_='calendar__actual').text.strip()
                event_forecast = row.find(
                    'td', class_='calendar__forecast').text.strip()
                event_previous = row.find(
                    'td', class_='calendar__previous').text.strip()

                calendar_data.append({
                    'time': event_time,
                    'currency': event_currency,
                    'impact': event_impact,
                    'description': event_description,
                    'actual': event_actual,
                    'forecast': event_forecast,
                    'previous': event_previous,
                })
            except Exception as e:
                # print('Error ❌ ' + str(e ) + ' ' + str(row))
                pass

        return calendar_data
    else:
        print("Failed to fetch data from Forex Factory.")
        return None


if __name__ == "__main__":
    from pathlib import Path
    # create a Path object with the path to the file
    path = Path('./.env')
    
    if not path.is_file():
        raise Exception('.env File Does not Exist. ❌')
    
    token = os.getenv('BOT_TOKEN')
    chat_id = os.getenv('ZANGOOLE_CHAT_ID')
    telegram_client = Telegram(token=token, chat_id=chat_id)
    economic_calendar = fetch_forex_factory_economic_calendar()
    if economic_calendar:
        for idx, event in enumerate(economic_calendar, start=1):
            if "usd" in event['currency'].lower():
                telegram_client.send_message(event['time'])
            print(f"Event {idx}:")
            print(f"Time: {event['time']}")
            print(f"Currency: {event['currency']}")
            print(f"Impact: {event['impact']}")
            print(f"Description: {event['description']}")
            print(f"Actual: {event['actual']}")
            print(f"Forecast: {event['forecast']}")
            print(f"Previous: {event['previous']}")
            print("----------------------")
    else:
        print("No economic calendar data available.")
