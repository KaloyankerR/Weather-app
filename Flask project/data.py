import time
import json
import requests
from bs4 import BeautifulSoup


class WeatherData():
    def __init__(self):
        self.url = ""
        self.page = ""
        self.soup = None
        self.data = {}
        self.result = []
        self.links = {"Amsterdam": "https://weather.com/weather/today/l/3507575ecc2861a186231bbaf61661fd789f860cceff8379c37a316e0622af04",
                      "Eindhoven": "https://weather.com/weather/today/l/79dfcc3ff0cfcafe69dc42c1558040907b27d8c288a816a62c0ef28f687b3a6b",
                      "Breda": "https://weather.com/weather/today/l/2d459432494694c7ea573e9613be5a669fad4b41ed390231e6d7159f5bb64105",
                      "Utrecht": "https://weather.com/weather/today/l/a3531af342d5a4be0c2a2d3f106f14ec4479cb27b3f910561b4ea5ef731d7cdf",
                      "Groningen": "https://weather.com/weather/today/l/4ce50fcb3961e2d9423669cf60d9f76b0a891e75ae8d32eb5ddc82c517a1e778"}

    def set_up_url(self, url: str):
        self.url = url
        self.page = requests.get(url=self.url)
        self.soup = BeautifulSoup(self.page.content, "html.parser")

    def get_elements(self):
        result = self.soup.find(id="todayDetails")

        temp = result.find(
            "span", {"class": "TodayDetailsCard--feelsLikeTempValue--Cf9Sl"}).get_text()
        high_low = result.find(
            "div", {"class": "WeatherDetailsListItem--wxData--2s6HT"}).get_text()
        wind = result.find(
            "span", {"class": "Wind--windWrapper--3aqXJ undefined"})
        wind = list(wind.children)[1]
        humidity = result.find(
            "span", {"data-testid": "PercentageValue"}).get_text()
        uv_index = result.find(
            "span", {"data-testid": "UVIndexValue"}).get_text()

        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)

        self.data = {"Temperature": temp,
                     "High and low": high_low,
                     "Wind": wind,
                     "Humidity": humidity,
                     "UV index": uv_index,
                     "Time": current_time}

    def update_json(self):
        with open("WeatherData.json", "r") as f:
            data = json.load(f)

        for key in self.links.keys():
            link = self.links[key]

            new_data = WeatherData()
            new_data.set_up_url(url=link)

            data[key] = [self.links[key], new_data.get_data(url=link)]

        with open('WeatherData.json', 'w') as f:
            json.dump(data, f)
            f.close()

    def get_data(self, url: str):
        self.set_up_url(url=url)
        self.get_elements()
        return self.data

    def __repr__(self):
        for title in self.data.keys():
            self.result.append(f"{title} - {self.data[title]}")
        return '\n'.join(self.result)


# a = WeatherData()
# a.update_json()
