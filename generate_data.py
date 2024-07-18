import requests
from bs4 import BeautifulSoup


class Sinoptik:
    def __init__(self, city):
        self.city = city

    def get_page_city(self):
        url = f'https://sinoptik.ua/погода-{self.city}'
        page = requests.get(url)
        return page.text

    def get_data(self):
        page = self.get_page_city()
        soup = BeautifulSoup(page, 'html.parser')
        weather_data = []

        for node in soup.select('#blockDays .main'):
            id = node['id']
            day = node.select_one('.day-link').text
            date = node.select_one('.date').text
            temp_min = node.select_one('.temperature .min span').text
            temp_max = node.select_one('.temperature .max span').text

            weather_data.append({
                'id': id,
                'day': day,
                'date': date,
                'tMin': temp_min,
                'tMax': temp_max,
            })

        return weather_data