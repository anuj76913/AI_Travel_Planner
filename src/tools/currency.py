import requests
from langchain_core.tools import tool

@tool
def convert_currency(amount: float, from_currency: str = "USD", to_currency: str = "AED") -> str:
    """
    Convert an amount from one currency to another using current exchange rates.
    Useful for budget calculations. Defaults to USD to AED.
    """
    # Using a free open API that doesn't require an API key for basic rates
    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
    try:
        response = requests.get(url)
        data = response.json()
        if "rates" in data and to_currency in data["rates"]:
            rate = data["rates"][to_currency]
            converted = amount * rate
            return f"{amount} {from_currency} is approximately {converted:.2f} {to_currency} (Rate: {rate})"
        else:
            # Fallback to mock rate if API fails
            mock_rate = 3.67 if from_currency == "USD" and to_currency == "AED" else 1.0
            converted = amount * mock_rate
            return f"[MOCK CURRENCY] {amount} {from_currency} is approx {converted:.2f} {to_currency}"
    except Exception as e:
        mock_rate = 3.67 if from_currency == "USD" and to_currency == "AED" else 1.0
        return f"[MOCK CURRENCY] {amount} {from_currency} is approx {amount * mock_rate:.2f} {to_currency} (Error: {e})"
