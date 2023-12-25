import requests
import pysrt
import time
from dotenv import load_dotenv

load_dotenv()


def translate_text(text, source_lang, target_lang):
    api_key = ''
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

def translate_srt(file_path, output_file, source_lang, target_lang):
    start_time = time.time()
    subs = pysrt.open(file_path)
    for sub in subs:
        translated_text = translate_text(sub.text, source_lang, target_lang)
        sub.text = translated_text
    subs.save(output_file, encoding='utf-8')
    end_time = time.time()
    print(f"Time Taken For Google Translate: {end_time - start_time} seconds")



# Example usage
# input_srt = 'tests/transcription_en.srt'  # Path to your input SRT file
# output_srt = 'tests/transcription_es_good_translate.srt'  # Path for the translated SRT file
# source_language = 'en'  # Source language
# target_language = 'es'  # Target language (Hebrew in this example)

# translate_srt(input_srt, output_srt, source_language, target_language)
