def translate(text_key, lang='uk'):
    translations = {
        'uk': {
            'lang_name': 'Українська',
            'v1_label': 'Швидкість v1 (км/год):',
            'v2_label': 'Швидкість v2 (м/с):',
            'speed': 'Швидкість',
            'less': 'менша ніж',
            'greater': 'більша ніж',
            'equal': 'дорівнює',
            'kmh': 'км/год',
            'ms': 'м/с'
        },
        'en': {
            'lang_name': 'English',
            'v1_label': 'Speed v1 (km/h):',
            'v2_label': 'Speed v2 (m/s):',
            'speed': 'Speed',
            'less': 'is less than',
            'greater': 'is greater than',
            'equal': 'is equal to',
            'kmh': 'km/h',
            'ms': 'm/s'
        }
    }
    if lang not in translations:
        lang = 'uk'
    return translations[lang].get(text_key, text_key)

def compare_speeds(v1_kmh, v2_ms):
    v1_in_ms = v1_kmh / 3.6
    v2_in_kmh = v2_ms * 3.6
    
    if v1_in_ms < v2_ms:
        comparison = 'less'
    elif v1_in_ms > v2_ms:
        comparison = 'greater'
    else:
        comparison = 'equal'
        
    return round(v1_in_ms, 1), round(v2_in_kmh, 1), comparison