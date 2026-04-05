import sys

if sys.version_info >= (3, 13):
    print("Python 3.13 or higher is used. Googletrans package==3.1.0a0 "
          "may not work correctly on this version. Python 3.12 or below is recommended.")
    sys.exit()
from googletrans import Translator, LANGUAGES

def CodeLang(lang: str) -> str:
    lang = lang.lower().strip()
    
    if lang in LANGUAGES:
        return LANGUAGES[lang].capitalize()
        
    for code, name in LANGUAGES.items():
        if name.lower() == lang:
            return code
            
    return "Language or code not found."

def TransLate(text: str, scr: str, dest: str) -> str:
    try:
        translator = Translator()
        
        src_code = "auto" if scr.lower() == "auto" else scr.lower()
        if src_code != "auto" and src_code not in LANGUAGES:
            src_code = CodeLang(scr)
            if "Error" in src_code:
                return src_code
                
        dest_code = dest.lower()
        if dest_code not in LANGUAGES:
            dest_code = CodeLang(dest)
            if "Error" in dest_code:
                return dest_code
                
        result = translator.translate(text, src=src_code, dest=dest_code)
        return result.text
        
    except Exception as e:
        return f"Error translation: {str(e)}"

def LangDetect(text: str, set: str = "all") -> str:
    try:
        translator = Translator()
        detection = translator.detect(text)
        
        if set == "lang":
            return detection.lang
        elif set == "confidence":
            return str(detection.confidence)
        elif set == "all":
            return f"Language: {detection.lang}, Confidence: {detection.confidence}"
        else:
            return "Incorrect set parameter."
            
    except Exception as e:
        return f"Language detection error: {str(e)}"

def LanguageList(out: str = "screen", text: str = "") -> str:
    try:
        translator = Translator()
        headers = ["№", "Language", "ISO-639 code"]
        if text:
            headers.append("Text")
            
        codes = list(LANGUAGES.keys())
        rows = []
        
        for i, code in enumerate(codes, start=1):
            name = LANGUAGES[code].capitalize()
            row = [str(i), name, code]
            
            if text:
                try:
                    res = translator.translate(text, dest=code)
                    row.append(res.text)
                except:
                    row.append("-")
                    
            rows.append(row)
            
        cwidths = [max(len(str(item)) for item in col) for col in zip(*([headers] + rows))]
        
        table_str = ""
        header_row = "  ".join(f"{h:<{w}}" for h, w in zip(headers, cwidths))
        table_str += header_row + "\n"
        table_str += "-" * len(header_row) + "\n"
        
        for row in rows:
            table_str += "  ".join(f"{item:<{w}}" for item, w in zip(row, cwidths)) + "\n"
            
        if out == "screen":
            print(table_str)
            return "Ok"
        elif out == "file":
            with open("LanguageList2.txt", "w", encoding="utf-8") as f:
                f.write(table_str)
            return "Ok"
        else:
            return "Incorrect parameter out."
            
    except Exception as e:
        return f"Error in 'LanguageList': {str(e)}"