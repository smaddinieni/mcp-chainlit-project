import os
import getpass
from dotenv import load_dotenv
load_dotenv()
from tavily import TavilyClient
import requests
from typing import Any, Dict, List, Optional, Union

def tavily_search(query: str) -> dict:
    """
    Search for information using the Tavily API.

    Args:
        query (str): The search query string.

    Returns:
        dict: The search results from Tavily.
    """
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        api_key = getpass.getpass("Enter Tavily API key: ")
        os.environ["TAVILY_API_KEY"] = api_key
    client = TavilyClient(api_key=api_key)
    return client.search(query)

def get_wikipedia_summary(title: str, sentences: int = 3) -> Dict[str, Any]:
    """
    Fetches an encyclopedic summary for a given Wikipedia article title.

    Leverages the Wikimedia Action API with zero credential overhead.

    Args:
        title (str): The exact title of the Wikipedia article.
        sentences (int): Maximum number of sentences to return (default: 3).

    Returns:
        Dict[str, Any]: A dict containing 'title', 'extract', and 'pageid'.
    """
    endpoint = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "prop": "extracts",
        "exsentences": sentences,
        "explaintext": True,
        "format": "json",
        "titles": title,
    }
    resp = requests.get(endpoint, params=params)
    resp.raise_for_status()
    pages = resp.json()["query"]["pages"]
    page = next(iter(pages.values()))
    return {
        "title": page.get("title"),
        "extract": page.get("extract"),
        "pageid": page.get("pageid"),
    }


def get_weather_open_meteo(lat: float, lon: float, hourly: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Retrieves real-time and forecast weather data for specified coordinates.

    Utilizes the Open-Meteo endpoint without API keys or sign-ups.

    Args:
        lat (float): Latitude of the target location.
        lon (float): Longitude of the target location.
        hourly (List[str], optional): List of meteorological variables (e.g., ["temperature_2m", "windspeed_10m"]).

    Returns:
        Dict[str, Any]: Complete JSON payload of weather forecasts and metadata.
    """
    endpoint = "https://api.open-meteo.com/v1/forecast"
    params: Dict[str, Union[float, str, List[str]]] = {
        "latitude": lat,
        "longitude": lon,
        "timezone": "auto",
    }
    if hourly:
        params["hourly"] = ",".join(hourly)
    resp = requests.get(endpoint, params=params)
    resp.raise_for_status()
    return resp.json()


def get_all_countries() -> List[Dict[str, Any]]:
    """
    Retrieves the full catalogue of countries with metadata.

    Interfaces with the REST Countries API, delivering geo-context out of the box.

    Returns:
        List[Dict[str, Any]]: A list of country objects, each containing keys like 'name', 'capital', 'currencies', etc.
    """
    endpoint = "https://restcountries.com/v3.1/all"
    resp = requests.get(endpoint)
    resp.raise_for_status()
    return resp.json()


def get_exchange_rates(base: str = "EUR") -> Dict[str, Any]:
    """
    Fetches latest foreign‐exchange rates against a base currency.

    Consumes ExchangeRate.host’s zero-friction endpoint for financial superpowers.

    Args:
        base (str): ISO currency code to use as the reference (default: "EUR").

    Returns:
        Dict[str, Any]: A dict containing 'base', 'date', and 'rates' mapping currency codes to floats.
    """
    endpoint = "https://api.exchangerate.host/latest"
    params = {"base": base}
    resp = requests.get(endpoint, params=params)
    resp.raise_for_status()
    return resp.json()


def get_number_fact(number: Union[int, str], fact_type: str = "trivia") -> str:
    """
    Retrieves a contextual trivia/math/date fact for a given number.

    Orchestrates a simple HTTP call to Numbers API—no credentials required.

    Args:
        number (int | str): The subject number or date (use 'month/day' for date facts).
        fact_type (str): One of 'trivia', 'math', 'date', or 'year' (default: 'trivia').

    Returns:
        str: A plain-text fact string.
    """
    endpoint = f"http://numbersapi.com/{number}/{fact_type}"
    resp = requests.get(endpoint)
    resp.raise_for_status()
    return resp.text

def get_bitcoin_price() -> dict:
    """
    Fetches the current Bitcoin Price Index (BPI) from CoinDesk.

    This is a public API that does not require an API key, offering a simple
    way to get near real-time cryptocurrency data.

    Returns:
        dict: A dictionary containing Bitcoin price data (e.g., USD, GBP, EUR rates),
              or an error message if the request fails.
    """
    url = "https://api.coindesk.com/v1/bpi/currentprice.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("bpi", {})
    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching Bitcoin price: {e}"}

def get_random_activity() -> dict:
    """
    Fetches a suggestion for a random activity from the Bored API.

    This API is public and does not require an API key, making it excellent for
    adding dynamic, "real-time" (in the sense of fresh on demand) content.

    Returns:
        dict: A dictionary containing activity details (e.g., 'activity', 'type', 'participants'),
              or an error message if the request fails.
    """
    url = "https://www.boredapi.com/api/activity"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching random activity: {e}"}

def get_latest_news_headlines(query: str, api_key: str) -> dict:
    """
    Fetches the latest news headlines related to a specific query from GNews.

    This API requires a free API key for access, which is easy to obtain and
    provides a low-friction entry point for news data.

    Args:
        query (str): The search query for news headlines (e.g., "AI advancements").
        api_key (str): Your GNews API key. You can get one by signing up at gnews.io.

    Returns:
        dict: A dictionary containing news articles, or an error message if the request fails.
    """
    base_url = "https://gnews.io/api/v4/search"
    params = {
        "q": query,
        "lang": "en",      # Language of the articles
        "country": "us",   # Country of the articles
        "max": 5,          # Number of articles to retrieve
        "token": api_key   # Your GNews API key
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching news headlines: {e}"}