import requests
import pysrt

def translate_text(text, source_lang, target_lang, api_key):
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

    response = requests.post(url, data=payload, headers=headers)
    return response.json()['trans']

def translate_srt(file_path, output_file, source_lang, target_lang, api_key):
    subs = pysrt.open(file_path)
    for sub in subs:
        translated_text = translate_text(sub.text, source_lang, target_lang, api_key)
        sub.text = translated_text
    subs.save(output_file, encoding='utf-8')

# Example usage
input_srt = 'tests/transcription_en.srt'  # Path to your input SRT file
output_srt = 'tests/transcription_he_good_translate.srt'  # Path for the translated SRT file
source_language = 'en'  # Source language
target_language = 'he'  # Target language (Hebrew in this example)
api_key = '536d405d53mshebfc39ec9e2c5c7p1e8489jsna23d14919022'  # Replace with your actual RapidAPI key

translate_srt(input_srt, output_srt, source_language, target_language, api_key)
