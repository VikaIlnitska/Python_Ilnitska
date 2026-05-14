def translate(text_key, lang='uk'):
    translations = {
        'uk': {
            'lang_name': 'Українська',
            'time_label': 'Час (год хв):',
            'after_lunch': 'Час після обіду.',
            'before_lunch': 'Час до обіду.',
            'incorrect_time': 'Некоректний час.'
        },
        'en': {
            'lang_name': 'English',
            'time_label': 'Time (hr min):',
            'after_lunch': 'Time after lunch.',
            'before_lunch': 'Time before lunch.',
            'incorrect_time': 'Incorrect time.'
        }
    }
    if lang not in translations:
        lang = 'uk'
    return translations[lang].get(text_key, text_key)

def process_time(h, m):

    if not (0 <= h <= 23) or not (0 <= m <= 59):
        return False, None, None
    
    period = 'am' if h < 12 else 'pm'
    
    h_12 = h % 12
    if h_12 == 0:
        h_12 = 12
        
    time_str = f"{h_12}:{m:02d} {period}"
    period_key = 'before_lunch' if period == 'am' else 'after_lunch'
    
    return True, time_str, period_key