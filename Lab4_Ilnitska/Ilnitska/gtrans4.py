import asyncio
from package_3_modules.mod1 import TransLate, LangDetect, CodeLang, LanguageList
from package_3_modules import NAME, AUTHOR

async def main():
    print(f"Програма: {NAME}")
    print(f"Розробник: {AUTHOR}\n")

    print("1.CodeLang")
    print(f"Код для 'Greek': {CodeLang('Greek')}")
    print(f"Мова для коду 'el': {CodeLang('el')}")
    print(f"Неіснуюча мова: {CodeLang('fake_lang')}\n")

    print("2. LangDetect")
    txt = "Μου αρέσει ο σχεδιασμός ιστοσελίδων."
    print(f"Текст: '{txt}'")
    print(f"Параметр 'lang': {await LangDetect(txt, 'lang')}")
    print(f"Параметр 'confidence': {await LangDetect(txt, 'confidence')}")
    print(f"Параметр 'all': {await LangDetect(txt, 'all')}\n")

    print("3. Тестування TransLate")
    word = "Мені подобається веб-дизайн"
    print(f"Оригінал: '{word}'")
    print(f"Переклад на грецьку (auto -> el): {await TransLate(word, 'auto', 'el')}")
    print(f"Переклад на грецьку (uk -> greek): {await TransLate(word, 'uk', 'greek')}")
    print(f"Переклад з грецької на англійську: {await TransLate(txt, 'auto', 'en')}\n")

    print("4. LanguageList")
    
    result_screen = await LanguageList("screen", "Добрий день")
    print(f"Статус (screen): {result_screen}\n")

    result_file = await LanguageList("file", "Добрий день")
    print(f"Статус (file): {result_file}")

if __name__ == "__main__":
    asyncio.run(main())