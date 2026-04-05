import json

data = {
    "Ільніцька": ["Віка", "Олександрівна", 2005],
    "Шевченко": ["Тарас", "Григорович", 1814],
    "Косач": ["Лариса", "Петрівна", 1871],
    "Франко": ["Іван", "Якович", 1856],
    "Стус": ["Василь", "Семенович", 1938],
    "Костенко": ["Ліна", "Василівна", 1930],
    "Симоненко": ["Василь", "Андрійович", 1935],
    "Грушевський": ["Михайло", "Сергійович", 1866],
    "Довженко": ["Олександр", "Петрович", 1894],
    "Хмельницький": ["Богдан", "Михайлович", 1595]
}

with open('lab3.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Data added to data.json")

with open('lab3.json', 'r', encoding='utf-8') as f:
    loaded_data = json.load(f)

print("\nData from data.json:")
for surname, info in loaded_data.items():
    print(f"{surname}: {info[0]} {info[1]}, year of birth: {info[2]}")