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
            temp_min = node.select_one('.temperature .min span').text
            temp_max = node.select_one('.temperature .max span').text

            weather_details = False
            if soup.select(f'#{id}c'):
                weather_details = self.weather_details(soup.select_one(f'#{id}c'))

            weather_data.append({
                'id': id,
                'day': day,
                'tMin': temp_min,
                'tMax': temp_max,
                'weather_details': weather_details
            })

        return weather_data

    def weather_details(self, node):
        Th = [td.text for td in node.select('thead td')]
        Titles = [p.text for p in node.select('.titles p')]

        Body = []
        for tr in node.select('tbody tr'):
            row_data = []
            for td in tr.select('td'):
                if td.select_one('.weatherIcoS'):
                    row_data.append(td.select_one('div')['title'])
                else:
                    row_data.append(td.text)
            Body.append(row_data)

        Titles.insert(0, 'Години')
        Titles.insert(1, 'Погода')

        Body = [[row[i:i + 2] for i in range(0, len(row), 2)] for row in Body]

        modifiArray = {}
        for i, key in enumerate(Titles):
            if i < len(Body):
                for itemKey, item in enumerate(Body[i]):
                    modifiArray.setdefault(key, {})[Th[itemKey]] = item

        return {'details': modifiArray}