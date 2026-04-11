import csv
from datetime import datetime
from openpyxl import Workbook

current_date = datetime.now().date()

people_data = []

try:
    with open('people_data.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        people_data = list(reader)
except Exception:
    print("Повідомлення про відсутність, або проблеми при відкритті файлу CSV")
    exit()

younger_18 = []
age_18_45 = []
age_45_70 = []
older_70 = []

for row in people_data:
    birth_date = datetime.strptime(row['Дата народження'], "%Y-%m-%d").date()
    age = current_date.year - birth_date.year - ((current_date.month, current_date.day) < (birth_date.month, birth_date.day))

    category_row = [
        row['Прізвище'], 
        row["Ім'я"], 
        row['По батькові'], 
        row['Дата народження'], 
        age
    ]

    if age < 18:
        younger_18.append(category_row)
    elif 18 <= age <= 45:
        age_18_45.append(category_row)
    elif 45 < age <= 70:
        age_45_70.append(category_row)
    else:
        older_70.append(category_row)

def add_index(data_list):
    return [[index] + row for index, row in enumerate(data_list, 1)]

younger_18 = add_index(younger_18)
age_18_45 = add_index(age_18_45)
age_45_70 = add_index(age_45_70)
older_70 = add_index(older_70)

headers_all = list(people_data[0].keys()) if people_data else []
headers_category = ["№", "Прізвище", "Ім'я", "По батькові", "Дата народження", "Вік"]

try:
    workbook = Workbook()

    sheet_all = workbook.active
    sheet_all.title = "all"
    sheet_all.append(headers_all)
    for row in people_data:
        sheet_all.append(list(row.values()))

    def create_category_sheet(title, data_list):
        sheet = workbook.create_sheet(title=title)
        sheet.append(headers_category)
        for row in data_list:
            sheet.append(row)

    create_category_sheet("younger_18", younger_18)
    create_category_sheet("18-45", age_18_45)
    create_category_sheet("45-70", age_45_70)
    create_category_sheet("older_70", older_70)

    workbook.save("people_data.xlsx")
    print("Ok")
    
except Exception:
    print("Повідомлення про неможливість створення XLSX файлу")