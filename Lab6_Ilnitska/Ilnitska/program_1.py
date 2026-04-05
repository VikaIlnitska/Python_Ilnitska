UKR_ALPHABET = 'абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'

def sort_key(word):
    first_char = word[0].lower()
    if first_char in UKR_ALPHABET:
        key_chars = []
        for c in word.lower():
            if c in UKR_ALPHABET:
                key_chars.append(UKR_ALPHABET.index(c))
            else:
                key_chars.append(len(UKR_ALPHABET))
        return (0, key_chars)
    else:
        return (1, list(word.lower()))

with open('text_1.txt', 'r', encoding='utf-8') as f:
    text = f.read()

words = text.split()

print('List of words to sort:')
print(words)

sorted_words = sorted(words, key=sort_key)

print('\nSorted list:')
print(sorted_words)