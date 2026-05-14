def translate(text_key, lang='uk', **kwargs):
    translations = {
        'uk': {
            'lang_name': 'Українська',
            'time_label': 'Час (ч м):',
            'period_label': 'Половина доби:',
            'time_left': 'До опівночі залишилося {h} годин {m} хвилин.',
            'incorrect_input': 'Некоректний вві.!'
        },
        'en': {
            'lang_name': 'English',
            'time_label': 'Time (h m):',
            'period_label': 'Half of the day:',
            'time_left': '{h} hours and {m} minutes left until midnight.',
            'incorrect_input': 'Incorrect input.'
        }
    }
    if lang not in translations:
        lang = 'uk'
        
    text = translations[lang].get(text_key, text_key)
    if kwargs:
        return text.format(**kwargs)
    return text

def calculate_time_to_midnight(h, m, period):
    if not (1 <= h <= 12) or not (0 <= m <= 59) or period not in ['a', 'p']:
        return False, 0, 0

    if period == 'a':
        h_24 = 0 if h == 12 else h
    else: 
        h_24 = 12 if h == 12 else h + 12
        
    current_minutes = h_24 * 60 + m
    total_minutes_in_day = 24 * 60
    minutes_to_midnight = total_minutes_in_day - current_minutes

    if minutes_to_midnight == total_minutes_in_day:
        minutes_to_midnight = 0
        
    left_h = minutes_to_midnight // 60
    left_m = minutes_to_midnight % 60
    
    return True, left_h, left_m