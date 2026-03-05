import asyncio
import time
from googletrans import Translator, LANGUAGES

def CodeLang(lang):
    lang = lang.lower()
    if lang in LANGUAGES:
        return LANGUAGES[lang].capitalize()
    for code, name in LANGUAGES.items():
        if name.lower() == lang:
            return code
    return "Мова або код не знайдено."

async def LangDetect(txt):
    translator = Translator()
    try:
        detection = await translator.detect(txt)
        return detection.lang, detection.confidence
    except Exception as e:
        return f"Помилка визначення мови: {str(e)}"

async def TransLate(str, lang):
    translator = Translator()
    d_code = lang.lower()
    
    if d_code not in LANGUAGES:
        d_code = CodeLang(lang)
        if d_code == "error":
            return "error"
            
    try:
        result = await translator.translate(str, dest=d_code)
        return result.text
    except Exception as e:
        return f"Помилка перекладу: {str(e)}"

async def main():
    file_name = "Steve_Jobs_6.txt"
    v_lang = "Greek"
    
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            text = file.read()
    except:
        print("Помилка читання файлу")
        return

    symb = len(text)
    
    raw_list = text.split(". ")
    TxtList = []
    for sentence in raw_list:
        if sentence != "":
            TxtList.append(sentence + ".")
            
    s_count = len(TxtList)

    start_sync = time.time()
    lang_code, confidence = await LangDetect(text)
    sync_translated = []
    for sentence in TxtList:
        t = await TransLate(sentence, v_lang)
        sync_translated.append(t)
    end_sync = time.time()
    sync_time = end_sync - start_sync

    start_async = time.time()
    await LangDetect(text)
    tasks = []
    for sentence in TxtList:
        task = asyncio.create_task(TransLate(sentence, v_lang))
        tasks.append(task)
    async_translated = await asyncio.gather(*tasks)
    end_async = time.time()
    async_time = end_async - start_async

    lang_name = CodeLang(lang_code)
    lang_code = CodeLang(v_lang)

    print(f"1. Ім'я файлу: {file_name}")
    print(f"2. Кількість символів в тексті: {symb}")
    print(f"3. Кількість речень в тексті: {s_count}")
    print(f"4. Мова - {lang_name}, код - {lang_code}, confidence - {confidence} для оригінального тексту\n")
    print(f"5. Оригінальний текст:\n{text}\n")
    print(f"6. Мова - {v_lang}, код - {lang_code} на якій було зроблено переклад\n")
    print(f"7. Перекладений текст:\n{' '.join(async_translated)}\n")
    print(f"8. Час роботи (пункт 3.4.1): {sync_time: .1f} сек")
    print(f"9. Час роботи (пункт 3.4.2): {async_time: .1f} сек")

if __name__ == "__main__":
    asyncio.run(main())