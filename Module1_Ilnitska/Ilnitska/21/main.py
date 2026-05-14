import os
import sys
from module import translate, calculate_time_to_midnight

FILENAME = "MyData.txt"

def read_data():
    if not os.path.exists(FILENAME):
        return None
    try:
        with open(FILENAME, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        
        if len(lines) < 3:
            return None
            
        time_parts = lines[0].split()
        if len(time_parts) != 2:
            return None
            
        h = int(time_parts[0])
        m = int(time_parts[1])
        period = lines[1].lower()
        lang = lines[2].lower()
        
        return h, m, period, lang, lines[0]
    except Exception:
        return None

def main():
    data = read_data()
    
    if data is None:
        time_input = input("Time (h m): ")
        period_input = input("Half of day: ")
        lang_input = input("Interface language: ")
        
        with open(FILENAME, 'w', encoding='utf-8') as f:
            f.write(f"{time_input}\n{period_input}\n{lang_input}")
            
        print(f"Data saved in file {FILENAME}")
        sys.exit()

    h, m, period, lang, original_time_str = data
    
    if lang not in ['uk', 'en']:
        lang = 'uk'
        
    print(f"Language: {translate('lang_name', lang)}")
    print(f"{translate('time_label', lang)} {original_time_str}")
    print(f"{translate('period_label', lang)} {period}")
    
    is_valid, left_h, left_m = calculate_time_to_midnight(h, m, period)
    
    if not is_valid:
        print(translate('incorrect_input', lang))
    else:
        print(translate('time_left', lang, h=left_h, m=left_m))

if __name__ == "__main__":
    main()