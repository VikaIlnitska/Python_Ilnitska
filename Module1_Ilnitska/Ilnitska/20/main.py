import os
import sys
from module import translate, process_time

FILENAME = "MyData.txt"

def read_data():
    if not os.path.exists(FILENAME):
        return None
    try:
        with open(FILENAME, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        
        if len(lines) < 2:
            return None
            
        time_parts = lines[0].split()
        if len(time_parts) != 2:
            return None
            
        h = int(time_parts[0])
        m = int(time_parts[1])
        lang = lines[1].lower()
        return h, m, lang, lines[0]
    except Exception:
        return None

def main():
    data = read_data()
    
    if data is None:
        time_input = input("Time (h m): ")
        lang_input = input("Interface language: ")
        
        with open(FILENAME, 'w', encoding='utf-8') as f:
            f.write(f"{time_input}\n{lang_input}")
            
        print(f"Data saved in file {FILENAME}")
        sys.exit()

    h, m, lang, original_time_str = data
    
    if lang not in ['uk', 'en']:
        lang = 'uk'
        
    print(f"Language: {translate('lang_name', lang)}")
    print(f"{translate('time_label', lang)} {original_time_str}")
    
    is_valid, time_str, period_key = process_time(h, m)
    
    if not is_valid:
        print(translate('incorrect_time', lang))
    else:
        print(time_str)
        print(translate(period_key, lang))

if __name__ == "__main__":
    main()