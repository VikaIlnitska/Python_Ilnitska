import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

try:
    df = pd.read_csv('people_data.csv', encoding='utf-8')
    print("Ok")
except Exception:
    print("Повідомлення про відсутність, або проблеми при відкритті файлу CSV")
    exit()

current_date = datetime.now().date()
df['Дата народження'] = pd.to_datetime(df['Дата народження']).dt.date

def calculate_age(birth_date):
    return current_date.year - birth_date.year - ((current_date.month, current_date.day) < (birth_date.month, birth_date.day))

df['Вік'] = df['Дата народження'].apply(calculate_age)

def categorize_age(age):
    if age < 18:
        return 'younger_18'
    elif 18 <= age <= 45:
        return '18-45'
    elif 45 < age <= 70:
        return '45-70'
    else:
        return 'older_70'

df['Вікова категорія'] = df['Вік'].apply(categorize_age)

gender_counts = df['Стать'].value_counts()
print("\nКількість співробітників чоловічої і жіночої статі:")
print(gender_counts.to_string())

plt.figure(1, figsize=(6, 6))
gender_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90)
plt.title('Кількість співробітників чоловічої і жіночої статі')
plt.ylabel('')

categories_order = ['younger_18', '18-45', '45-70', 'older_70']
df['Вікова категорія'] = pd.Categorical(df['Вікова категорія'], categories=categories_order, ordered=True)
age_category_counts = df['Вікова категорія'].value_counts().sort_index()

print("\nКількість співробітників кожної вікової категорії:")
print(age_category_counts.to_string())

plt.figure(2, figsize=(8, 5))
age_category_counts.plot(kind='bar')
plt.title('Кількість співробітників кожної вікової категорії')
plt.xlabel('Вікова категорія')
plt.ylabel('Кількість')
plt.xticks(rotation=0)

gender_age_counts = df.groupby(['Вікова категорія', 'Стать']).size().unstack(fill_value=0)
print("\nКількість співробітників за статтю в кожній віковій категорії:")
print(gender_age_counts.to_string())

plt.figure(3, figsize=(10, 6))
gender_age_counts.plot(kind='bar', ax=plt.gca())
plt.title('Кількість співробітників за статтю в кожній віковій категорії')
plt.xlabel('Вікова категорія')
plt.ylabel('Кількість')
plt.xticks(rotation=0)
plt.legend(title='Стать')

plt.show()