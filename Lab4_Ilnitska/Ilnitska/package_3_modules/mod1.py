import asyncio
from googletrans import Translator, LANGUAGES

def CodeLang(lang: str) -> str:
    lang = lang.lower().strip()
    
    if lang in LANGUAGES:
        return LANGUAGES[lang].capitalize()

    for code, name in LANGUAGES.items():
        if name.lower() == lang:
            return code
            
    return "Language or code not found."

async def TransLate(text: str, scr: str, dest: str) -> str:
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
                
        result = await translator.translate(text, src=src_code, dest=dest_code)
        return result.text
        
    except Exception as e:
        return f"Error translation: {str(e)}"

async def LangDetect(text: str, set: str = "all") -> str:
    try:
        translator = Translator()
        detection = await translator.detect(text)
        
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

async def _safe_translate(translator, text, dest_code):
    try:
        res = await translator.translate(text, dest=dest_code)
        return res.text
    except:
        return "-"

async def LanguageList(out: str = "screen", text: str = "") -> str:
    try:
        translator = Translator()
        headers = ["№", "Language", "ISO-639 code"]
        if text:
            headers.append("Text")
            
        codes = list(LANGUAGES.keys())
        translated_texts = []

        if text:
            tasks = [_safe_translate(translator, text, code) for code in codes]
            translated_texts = await asyncio.gather(*tasks)
            
        rows = []
        for i, code in enumerate(codes, start=1):
            name = LANGUAGES[code].capitalize()
            row = [str(i), name, code]
            if text:
                row.append(translated_texts[i-1])
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
            with open("LanguageList.txt", "w", encoding="utf-8") as f:
                f.write(table_str)
            return "Ok"
        else:
            return "Incorrect parameter out"
            
    except Exception as e:
        return f"Error in 'LanguageList': {str(e)}"