import os
import csv
from operator import itemgetter
from tabulate import tabulate


class PriceListAnalyzer:
    def __init__(self):
        self.data = []

    def load_prices(self, folder_path):
        for file_name in os.listdir(folder_path):
            if "price" in file_name:
                with open(os.path.join(folder_path, file_name), 'r') as file:
                    csv_reader = csv.DictReader(file, delimiter=';')
                    for row in csv_reader:
                        product_name = None
                        price = None
                        weight = None

                        for key, value in row.items():
                            if key.lower() in ["название", "продукт", "товар", "наименование"]:
                                product_name = value
                            elif key.lower() in ["цена", "розница"]:
                                price = float(value)
                            elif key.lower() in ["фасовка", "масса", "вес"]:
                                weight = float(value)

                        if product_name and price and weight:
                            self.data.append(
                                {'Наименование': product_name, 'Цена': price, 'Вес': weight, 'Файл': file_name})

    def export_to_html(self, file_name):
        with open(file_name, 'w') as file:
            file.write("<html><body>")
            file.write(tabulate(self.data, headers='keys', tablefmt='html'))
            file.write("</body></html>")

    def find_text(self, text):
        return [item for item in self.data if text.lower() in item['Наименование'].lower()]

    def display_results(self, results):
        sorted_results = sorted(results, key=itemgetter('Цена', 'Вес'))
        for i, result in enumerate(sorted_results, 1):
            result['Цена за кг.'] = result['Цена'] / result['Вес']
        print(tabulate(sorted_results, headers='keys', showindex='always'))


# Пример использования класса
analyzer = PriceListAnalyzer()
analyzer.load_prices("C:/Users/Admin/Downloads/_Практическое задание _Анализатор прайс-листов._")

while True:
    user_input = input("Введите текст для поиска (для выхода введите 'exit'): ")
    if user_input.lower() == 'exit':
        print("Работа завершена.")
        break
    else:
        results = analyzer.find_text(user_input)
        analyzer.display_results(results)

# Экспорт данных в HTML
analyzer.export_to_html("output.html")