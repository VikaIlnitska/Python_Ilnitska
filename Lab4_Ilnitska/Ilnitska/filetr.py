import json
import os
import importlib
import asyncio
import inspect

from package_3_modules import NAME, AUTHOR

async def main():
    print(f"Програма: {NAME}")
    print(f"Розробник: {AUTHOR}")

    config_file = "config.json"
    
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)
    except Exception as e:
        print(f"Error reading configuration file: {e}")
        return
        
    txt_filename = config.get("text_file", "")
    target_lang = config.get("target_language", "el")
    module_name = config.get("module_name", "mod3")
    output_dest = config.get("output", "screen")
    max_sentences = config.get("max_sentences", 10)
    
    if not os.path.exists(txt_filename):
        print(f"File is '{txt_filename}' not found.")
        return
        
    try:
        file_size = os.path.getsize(txt_filename)
        with open(txt_filename, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception as e:
        print(f"Error reading text file: {e}")
        return
        
    try:
        mod = importlib.import_module(f"package_3_modules.{module_name}")
    except Exception as e:
        print(f"Module loading error '{module_name}': {e}")
        return

    async def call_func(func, *args):
        if inspect.iscoroutinefunction(func):  
            return await func(*args)
        return func(*args)

    char_count = len(text)
    
    raw_list = text.split(". ")
    sentences = [s + "." if not s.endswith(".") else s for s in raw_list if s.strip()]
    total_sentences = len(sentences)

    try:
        detected_lang = await call_func(mod.LangDetect, text, "lang")
    except Exception as e:
        detected_lang = f"Error: {e}"

    print("\nAbout file")
    print(f"Назва файлу: {txt_filename}")
    print(f"Розмір файлу: {file_size} байт")
    print(f"Кількість символів: {char_count}")
    print(f"Кількість речень: {total_sentences}")
    print(f"Мова тексту: {detected_lang}\n")

    sentences_to_translate = sentences[:max_sentences]
    text_to_translate = " ".join(sentences_to_translate)
    
    try:
        translated_text = await call_func(mod.TransLate, text_to_translate, "auto", target_lang)
    except Exception as e:
        print(f"Error translation: {e}")
        return
        
    lang_check = await call_func(mod.CodeLang, target_lang)
    if len(lang_check) <= 3: 
        lang_code = lang_check
        lang_name = target_lang.capitalize()
    else:                 
        lang_code = target_lang
        lang_name = lang_check

    if output_dest == "screen":
        print("Results")
        print(f"Мова перекладу: {lang_name}")
        print(f"Модуль: {module_name}\n")
        print(f"Перекладений текст: {translated_text}\n")
        
    elif output_dest == "file":
        try:
            base_name = os.path.splitext(txt_filename)[0]
            new_filename = f"{base_name}_{lang_code}.txt"
            with open(new_filename, "w", encoding="utf-8") as f:
                f.write(translated_text)
            print("Ok")
        except Exception as e:
            print(f"Error writing to file: {e}")
            
    else:
        print(f"Unknown output type '{output_dest}' in config.")

if __name__ == "__main__":
    asyncio.run(main())