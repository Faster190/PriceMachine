import os


class PriceMachine:

    def __init__(self):
        self.data = []
        self.result = ''
        self.name_length = 0

    def _search_product_price_weight(self, headers=''):
        '''
            Возвращает номер столбца по которому происходила сортировка
        '''
        num = 4
        if headers == 'Название':
            num = 0
        if headers == 'Цена':
            num = 1
        if headers == 'Фасовка':
            num = 2
        if headers == 'Файл':
            num = 3
        self.data.sort(key=lambda num_of_head: num_of_head[num])
        return num + 1

    def load_prices(self, file_path='.'):
        '''
            Сканирует указанный каталог. Ищет файлы со словом price в названии.
            В файле ищет столбцы с названием товара, ценой и весом.
            Допустимые названия для столбца с товаром:
                товар
                название
                наименование
                продукт
                
            Допустимые названия для столбца с ценой:
                розница
                цена

            Допустимые названия для столбца с весом (в кг.)
                вес
                масса
                фасовка
        '''
        dir_files = os.listdir(file_path)
        for file_name in dir_files:
            if "price" in file_name:
                if file_path == '.':
                    file_path = ''
                path = file_path + file_name
                file = open(path, encoding='utf-8')
                file_data = file.read().split('\n')
                file.close()
                headers = file_data[0].split(',')
                file_data.pop(0)
                name_num, price_num, weight_num = None, None, None
                for i in range(len(headers)):
                    if headers[i] in ['товар', 'название', 'наименование', 'продукт']:
                        name_num = i
                    if headers[i] in ['розница', 'цена']:
                        price_num = i
                    if headers[i] in ['вес', 'масса', 'фасовка']:
                        weight_num = i
                for row_unsplited in file_data:
                    row = row_unsplited.split(',')
                    if len(row) < len(headers):
                        continue
                    self.data.append(
                        [
                            row[name_num],  # имя продукта
                            row[price_num],  # цена продукта
                            row[weight_num],  # вес продукта
                            file_name,  # имя файла
                            round(float(row[price_num]) / float(row[weight_num]), 2)  # цена/вес
                        ]
                    )
        self._search_product_price_weight()

    def export_to_html(self, indexes, fname='output.html'):
        result = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Позиции продуктов</title>
        </head>
        <body>
            <table>
                <tr>
                    <th>Номер</th>
                    <th>Название</th>
                    <th>Цена</th>
                    <th>Фасовка</th>
                    <th>Файл</th>
                    <th>Цена за кг.</th>
                </tr>
        '''
        for i, item in enumerate(indexes, 1):
            product, cost, weight, file, value = self.data[item]
            result += "<tr>"
            result += f"<td>{i}</td>"
            result += f"<td>{product}</td>"
            result += f"<td>{cost}</td>"
            result += f"<td>{weight}</td>"
            result += f"<td>{file}</td>"
            result += f"<td>{value}</td>"
            result += "</tr\n>"
        result += "</table>\n</body>"
        file = open(fname, 'w', encoding='utf-8')
        file.write(result)
        file.close()

    def find_text(self, text):
        new_data = []
        for i in range(len(self.data)):
            if text.lower() in self.data[i][0].lower():
                new_data.append(i)
        return new_data


pm = PriceMachine()
pm.load_prices()
'''
    Логика работы программы
'''
print('№ | Наименование | цена | вес | файл | цена за кг.')
for i in range(len(pm.data)):
    print(i + 1, *pm.data[i], sep=' | ')
indexes = len(pm.data)
while True:
    text = input("Введите слово для поиска: ")
    if text == "exit":
        break
    indexes = pm.find_text(text)
    for i in range(len(indexes)):
        print(i + 1, *pm.data[indexes[i]], sep=' | ')
print('the end')
print(pm.export_to_html(indexes=indexes))
