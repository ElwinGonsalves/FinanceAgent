def get_maps_link(country_name: str):
    """
    Returns a Google Maps link for the main Stock Exchange HQ of the country.
    """
    country_name = country_name.lower().strip()
    
    # Mock Data Source
    data = {
        "japan": "https://www.google.com/maps/search/?api=1&query=Tokyo+Stock+Exchange",
        "india": "https://www.google.com/maps/search/?api=1&query=Bombay+Stock+Exchange",
        "us": "https://www.google.com/maps/search/?api=1&query=New+York+Stock+Exchange",
        "usa": "https://www.google.com/maps/search/?api=1&query=New+York+Stock+Exchange",
        "united states": "https://www.google.com/maps/search/?api=1&query=New+York+Stock+Exchange",
        "south korea": "https://www.google.com/maps/search/?api=1&query=Korea+Exchange+Seoul",
        "china": "https://www.google.com/maps/search/?api=1&query=Shanghai+Stock+Exchange",
        "uk": "https://www.google.com/maps/search/?api=1&query=London+Stock+Exchange",
        "united kingdom": "https://www.google.com/maps/search/?api=1&query=London+Stock+Exchange"
    }
    
    return data.get(country_name, "https://www.google.com/maps")
