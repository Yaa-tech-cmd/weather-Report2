"""
Travel Snapshot CLI

This command-line tool fetches:
1. Current weather for a city
2. Country information for the city's country

Usage:
    python main.py

Requirements:
    pip install requests

You will need an OpenWeatherMap API key:
https://openweathermap.org/api
"""

import json
import requests

API_KEY = "OPENWEATHER_API_KEY"


def get_weather(city):
    """Fetch weather data for a city"""
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    response = requests.get(url)

    if response.status_code != 200:
        raise ValueError("Could not find weather information for that city.")

    return response.json()


def get_country_info(country_name):
    """Fetch country data"""
    url = f"https://restcountries.com/v3.1/name/{country_name}"

    response = requests.get(url)

    if response.status_code != 200:
        raise ValueError("Could not retrieve country information.")

    return response.json()[0]


def save_to_file(data):
    """Save results to JSON file"""
    with open("travel_snapshot.json", "w") as file:
        json.dump(data, file, indent=4)


def display_results(data):
    """Print readable results"""

    print("\n===== TRAVEL SNAPSHOT =====")
    print(f"City: {data['city']}")
    print(f"Country: {data['country']}")
    print(f"Temperature: {data['temperature']}°C")
    print(f"Weather: {data['weather']}")
    print(f"Capital: {data['capital']}")
    print(f"Population: {data['population']:,}")
    print(f"Region: {data['region']}")
    print(f"Currency: {data['currency']}")
    print("===========================\n")


def main():
    city = input("Enter a city name: ").strip()

    try:
        weather_data = get_weather(city)

        country_name = weather_data["sys"]["country"]

        # Convert country code to full country name
        country_lookup = requests.get(
            f"https://restcountries.com/v3.1/alpha/{country_name}"
        ).json()[0]

        country_data = get_country_info(
            country_lookup["name"]["common"]
        )

        currency = list(country_data["currencies"].values())[0]["name"]

        combined_data = {
            "city": weather_data["name"],
            "country": country_data["name"]["common"],
            "temperature": weather_data["main"]["temp"],
            "weather": weather_data["weather"][0]["description"],
            "capital": country_data["capital"][0],
            "population": country_data["population"],
            "region": country_data["region"],
            "currency": currency
        }

        save_to_file(combined_data)
        display_results(combined_data)

        print("Data saved to travel_snapshot.json")

    except Exception as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    main()