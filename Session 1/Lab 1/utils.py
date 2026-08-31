DUMMY_WEATHER_DATA = {
    "pune": {
        "location": "Pune",
        "temperature_c": 22,
        "condition": "rainy",
        "humidity": 48,
    },
    "london": {
        "location": "London",
        "temperature_c": 18,
        "condition": "light rain",
        "humidity": 72,
    },
    "tokyo": {
        "location": "Tokyo",
        "temperature_c": 28,
        "condition": "partly cloudy",
        "humidity": 61,
    },
    "hyderabad": {
        "location": "Hyderabad",
        "temperature_c": 33,
        "condition": "hot and dry",
        "humidity": 34,
    },
}

def _normalize_location(location: str) -> str:
    return " ".join(location.strip().lower().split())


def get_weather(location: str) -> str:
    """Return dummy weather data for a given location."""
    weather = DUMMY_WEATHER_DATA.get(_normalize_location(location))
    if weather is None:
        supported_locations = ", ".join(
            sorted(item["location"] for item in DUMMY_WEATHER_DATA.values())
        )
        return (
            f"No dummy weather is configured for '{location}'. "
            f"Try one of: {supported_locations}."
        )

    return (
        f"Weather for {weather['location']}: {weather['temperature_c']}C, "
        f"{weather['condition']}, humidity {weather['humidity']}%."
    )