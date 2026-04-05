from deep_translator import GoogleTranslator
from langdetect import detect_langs
from langdetect.lang_detect_exception import LangDetectException

langs_dict = GoogleTranslator().get_supported_languages(as_dict=True)
codes_dict = {v: k for k, v in langs_dict.items()}

def CodeLang(lang: str) -> str:
    lang = lang.lower().strip()
    
    if lang in codes_dict:
        return codes_dict[lang].capitalize()
    elif lang in langs_dict:
        return langs_dict[lang]
    else:
        return "Language or code not found."

def TransLate(text: str, scr: str, dest: str) -> str:
    try:
        src_lang = "auto" if scr.lower() == "auto" else scr.lower()

        dest_lang = dest.lower()
        if dest_lang in langs_dict:
            dest_code = langs_dict[dest_lang]
        elif dest_lang in codes_dict:
            dest_code = dest_lang
        else:
            return "Error."

        translator = GoogleTranslator(source=src_lang, target=dest_code)
        result = translator.translate(text)
        return result
        
    except Exception as e:
        return f"Error translation: {str(e)}"

def LangDetect(text: str, set: str = "all") -> str:
    try:
        result = detect_langs(text)[0]
        lang_code = result.lang
        confidence = result.prob
        
        if set == "lang":
            return lang_code
        elif set == "confidence":
            return str(confidence)
        elif set == "all":
            return f"Language: {lang_code}, Confidence: {confidence}"
        else:
            return "Incorrect set parameter."
            
    except LangDetectException as e:
        return f"Language detection error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

def LanguageList(out: str = "screen", text: str = "") -> str:
    try:
        headers = ["№", "Language", "ISO-639 code"]
        if text:
            headers.append("Text")
            
        rows = []
        for i, (name, code) in enumerate(langs_dict.items(), start=1):
            row = [str(i), name.capitalize(), code]
            
            if text:
                try:
                    translated = GoogleTranslator(source='auto', target=code).translate(text)
                    row.append(translated)
                except:
                    row.append("-")
                    
            rows.append(row)
            
        col_widths = [max(len(str(item)) for item in col) for col in zip(*([headers] + rows))]
        
        table_str = ""
        header_row = "  ".join(f"{h:<{w}}" for h, w in zip(headers, col_widths))
        table_str += header_row + "\n"
        table_str += "-" * len(header_row) + "\n"
        
        for row in rows:
            table_str += "  ".join(f"{item:<{w}}" for item, w in zip(row, col_widths)) + "\n"
            
        if out == "screen":
            print(table_str)
            return "Ok"
        elif out == "file":
            with open("LangugeList3.txt", "w", encoding="utf-8") as f:
                f.write(table_str)
            return "Ok"
        else:
            return "Incorrect parameter out."
            
    except Exception as e:
        return f"Error in 'LanguageList': {str(e)}"