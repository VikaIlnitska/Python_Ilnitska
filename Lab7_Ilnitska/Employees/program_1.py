import csv
import random
import datetime
from faker import Faker

fake = Faker(locale='uk_UA')

male_middle_names = [
    "Олександрович", "Іванович", "Васильович", "Петрович", "Миколайович",
    "Володимирович", "Михайлович", "Дмитрович", "Юрійович", "Андрійович",
    "Сергійович", "Вікторович", "Анатолійович", "Степанович", "Євгенович",
    "Богданович", "Тарасович", "Романович", "Григорович", "Павлович"
]

female_middle_names = [
    "Олександрівна", "Іванівна", "Василівна", "Петрівна", "Миколаївна",
    "Володимирівна", "Михайлівна", "Дмитрівна", "Юріївна", "Андріївна",
    "Сергіївна", "Вікторівна", "Анатоліївна", "Степанівна", "Євгенівна",
    "Богданівна", "Тарасівна", "Романівна", "Григорівна", "Павлівна"
]

genders = ['Чоловіча'] * 300 + ['Жіноча'] * 200
random.shuffle(genders)

people_data = []

for gender in genders:
    if gender == 'Чоловіча':
        first_name = fake.first_name_male()
        last_name = fake.last_name_male()
        middle_name = random.choice(male_middle_names)
    else:
        first_name = fake.first_name_female()
        last_name = fake.last_name_female()
        middle_name = random.choice(female_middle_names)
        
    birth_date = fake.date_between_dates(
        date_start=datetime.date(1946, 1, 1), 
        date_end=datetime.date(2011, 12, 31)
    )
    
    address = fake.address().replace('\n', ', ')

    people = {
        "Прізвище": last_name,
        "Ім'я": first_name,
        "По батькові": middle_name,
        "Стать": gender,
        "Дата народження": birth_date.strftime("%Y-%m-%d"),
        "Посада": fake.job(),
        "Місто проживання": fake.city(),
        "Адреса проживання": address,
        "Телефон": fake.phone_number(),
        "Email": fake.email()
    }
    people_data.append(people)

fieldnames = [
    "Прізвище", "Ім'я", "По батькові", "Стать", "Дата народження", 
    "Посада", "Місто проживання", "Адреса проживання", "Телефон", "Email"
]

with open('people_data.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(people_data)

print("Data successfully generated and saved.")