import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Function to translate text using the Google Translate API
def translate_text(text, source_lang, target_lang):
    api_key = "536d405d53mshebfc39ec9e2c5c7p1e8489jsna23d14919022"
    url = "https://google-translate113.p.rapidapi.com/api/v1/translator/text"
    payload = {
        "from": source_lang,
        "to": target_lang,
        "text": text
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "google-translate113.p.rapidapi.com"
    }

    response = requests.post(url, data=payload, headers=headers, verify=False)
    translation = response.json()['trans']
    print(f"Got translation for: '{text}'. The translation is: '{translation}'")
    return translation

# Test function
def test_translate_text():
    # Sample text and languages for testing
    test_text = "Hello, world!"
    source_lang = "en"
    target_lang = "es"  # Translating to Spanish for example

    # Call the translate_text function
    try:
        translation = translate_text(test_text, source_lang, target_lang)
        print(f"Original: {test_text}")
        print(f"Translated: {translation}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the test
test_translate_text()
