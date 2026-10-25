import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")

if not API_KEY:
    print("Error: API key not found in .env file")
    exit()

url = "https://newsapi.org/v2/top-headlines"

params = {
    "country": "Kenya",
    "apiKey": API_KEY
}

try:
    response = requests.get(url, params=params, timeout=10)

    # Handle specific HTTP errors
    if response.status_code == 401:
        print("Authentication Error (401): Invalid API key.")
        exit()

    elif response.status_code == 429:
        print("Rate Limit Error (429): Too many requests. Try again later.")
        exit()

    elif response.status_code != 200:
        print(f"Unexpected Error ({response.status_code})")
        exit()

    data = response.json()

    print("\nTop News Headlines\n" + "-" * 30)

    articles = data.get("articles", [])

    if not articles:
        print("No articles found.")
    else:
        for article in articles[:5]:
            print(f"• {article['title']}")

except requests.exceptions.Timeout:
    print("Request timed out. Please check your connection.")

except requests.exceptions.ConnectionError:
    print("Connection error. Unable to reach the NewsAPI service.")

except requests.exceptions.RequestException as e:
    print("An unexpected request error occurred:")
    print(e)