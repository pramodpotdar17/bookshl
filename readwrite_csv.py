import csv
from datetime import datetime


def get_random_highlight():
    with open('highlights.csv', newline='') as csvfile:
        day_of_year = datetime.now().timetuple().tm_yday  # stackoverflow
        print(f'Hightlight of the day {day_of_year} -- {datetime.now()}')
        highlights = list(csv.reader(csvfile))
        # print()
        return highlights[day_of_year]
