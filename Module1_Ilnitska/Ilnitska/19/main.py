import os
import sys
from module import translate, compare_speeds

FILENAME = "MyData.txt"

def read_data():
    if not os.path.exists(FILENAME):
        return None
    try:
        with open(FILENAME, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        
        if len(lines) < 3:
            return None
            
        v1 = float(lines[0])
        v2 = float(lines[1])
        lang = lines[2].lower()
        return v1, v2, lang
    except Exception:
        return None

def format_number(num):
    if float(num).is_integer():
        return str(int(num))
    return str(num).replace('.', ',')

def main():
    data = read_data()
    
    if data is None:
        try:
            v1_input = input("Speed v1 (km/h): ")
            v2_input = input("Speed v2 (m/s): ")
            lang_input = input("Interface language: ")
            float(v1_input)
            float(v2_input)
            
            with open(FILENAME, 'w', encoding='utf-8') as f:
                f.write(f"{v1_input}\n{v2_input}\n{lang_input}")
                
            print(f"Data saved in file {FILENAME}")
        except ValueError:
            print("Speed must be equal each other.")
        sys.exit()

    v1, v2, lang = data
    
    if lang not in ['uk', 'en']:
        lang = 'uk'
        
    v1_ms, v2_kmh, comparison_key = compare_speeds(v1, v2)

    v1_str = format_number(v1)
    v2_str = format_number(v2)
    v1_ms_str = format_number(v1_ms)
    v2_kmh_str = format_number(v2_kmh)

    print(f"Мова: {translate('lang_name', lang)}")
    print(f"{translate('v1_label', lang)} {v1_str}")
    print(f"{translate('v2_label', lang)} {v2_str}")
    
    print(f"{translate('speed', lang)} {v1_str} {translate('kmh', lang)}={v1_ms_str} {translate('ms', lang)}")
    print(f"{translate('speed', lang)} {v2_str} {translate('ms', lang)}={v2_kmh_str} {translate('kmh', lang)},")
    
    comp_word = translate(comparison_key, lang)
    speed_word = translate('speed', lang).lower()
    print(f"{translate('speed', lang)} v1={v1_str} {translate('kmh', lang)}, {comp_word} {speed_word} v2={v2_str}{translate('ms', lang)}")

if __name__ == "__main__":
    main()