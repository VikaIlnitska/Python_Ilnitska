import os

surname_var = os.getenv('SURNAME')

if surname_var is not None:
    print(f"Змінна: {surname_var}")
else:
    print("Cистемна змінна відсутня.")