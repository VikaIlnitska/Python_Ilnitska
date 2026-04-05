from urllib.parse import unquote
import pyperclip

url_encoded = input("Encoded link: ")

url_decoded = unquote(url_encoded)

print("Decoded link:")
print(url_decoded)

pyperclip.copy(url_decoded)
print("Link copied to clipboard.")