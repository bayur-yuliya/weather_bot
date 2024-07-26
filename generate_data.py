import requests
from bs4 import BeautifulSoup
from datetime import datetime

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

    def fetch_weather_data(self, city, time, time2):
        s = Sinoptik(city)
        data = s.get_data()[0]["weather_details"]["details"]
        res = ""
        if 'Температура, °C' in data:
            res += f"Температура {data['Температура, °C'][time][time2]} °C "
        if 'чувствуется как ' in data:
            res += f"Чувствуется как {data['чувствуется как '][time][time2]} °C "
        if 'Давление, мм' in data and data['Давление, мм'][time][time2] != '  ':
            res += f"Давление: {data['Давление, мм'][time][time2]} мм "
        if 'Влажность, %' in data:
            res += f"Влажность: {data['Влажность, %'][time][time2]} %"
        if 'Вероятность осадков, %' in data and data['Вероятность осадков, %'][time][time2] != '-':
            res += f"Вероятность осадков: {data['Вероятность осадков, %'][time][time2]} %"
        return res


def get_time_period():
    current_hour = datetime.now().hour
    if 0 <= current_hour < 3:
        return ('ночь', 0)
    elif 3 <= current_hour < 6:
        return ('ночь', 1)

    elif 6 <= current_hour < 9:
        return ('утро', 0)
    elif 9 <= current_hour < 12:
        return ('утро', 1)

    elif 12 <= current_hour < 15:
        return ('день', 0)
    elif 15 <= current_hour < 18:
        return ('день', 1)

    elif 18 <= current_hour < 21:
        return ('вечер', 0)
    else:
        return ('вечер', 1)
