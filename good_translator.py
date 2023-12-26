import requests
import pysrt
import time
import os
from dotenv import load_dotenv
from cloudwatch_logger import CloudWatchLogger as logger

load_dotenv()


def translate_text(text, source_lang, target_lang):
    api_key = os.getenv('RAPID_API_KEY')
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
    logger.log(f"Sending post request to: {url}")
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
    logger.log(f"Time Taken For Google Translate: {end_time - start_time} seconds")

