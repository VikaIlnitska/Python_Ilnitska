from googletrans import Translator, LANGUAGES

def CodeLang(lang):
    lang_lower = lang.lower()

    if lang_lower in LANGUAGES:
        return LANGUAGES[lang_lower].capitalize()

    for code, name in LANGUAGES.items():
        if name.lower() == lang_lower:  
            return code
            
    return "Помилка: мову або код не знайдено."

def LangDetect(txt):
    translator = Translator()
    try:
        detection = translator.detect(txt)
        return f"Detected(lang={detection.lang}, confidence={detection.confidence})"
    except Exception as e:
        return f"Помилка визначення мови: {str(e)}"

def TransLate(str, lang):

    translator = Translator()
    dest_code = lang.lower()
  
    if dest_code not in LANGUAGES:
        dest_code = CodeLang(lang)
        if "Помилка" in dest_code:
            return dest_code
            
    try:
        result = translator.translate(str, dest=dest_code)
        return result.text
    except Exception as e:
        return f"Помилка під час перекладу: {str(e)}"

if __name__ == "__main__":
    print("Програма для перекладу тексту")

    user_text = input("Введіть текст для перекладу: ")
    user_lang = input("Введіть мову (наприклад, 'English', 'de' або 'FRENCH'): ")
    
    print("\nРезультати")

    print(f"1. Визначення мови оригіналу: {LangDetect(user_text)}")

    print(f"2. Перевірка коду/назви мови призначення: {CodeLang(user_lang)}")

    translation = TransLate(user_text, user_lang)
    print(f"3. Переклад тексту на '{user_lang}': {translation}")
