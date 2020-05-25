import requests
import bs4
import csv

class PriceTracker():
    items = []

    def __init__(self):
        with open('products.csv', newline='') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                self.items.append({
                    'name': row[0],
                    'url': row[1],
                    'first_price': float(row[2]),
                    'target_price': float(row[3]),
                    'actual_price': 0,
                })

    def fetch_items(self):
        pass

    def find_price(self, item):
        pass

    def fetch_prices(self):
        i = 0
        for item in self.items:
            self.print_price(self.items[i])
            i += 1

    def calculate_diff(self, item):
        return round(((item['actual_price'] - item['first_price']) / ((item['actual_price'] + item['first_price']) / 2)) * 100, 2)

    def print_price(self, item):
        print(f"{item['name']} ----- {item['actual_price']} $ ({self.calculate_diff(item)}%)")


tracker = PriceTracker()
tracker.fetch_prices()
