import requests
import pysrt
import time
import os
from dotenv import load_dotenv
from cloudwatch_logger import CloudWatchLogger as logger

load_dotenv()

from aws_secrets import get_secret
api_key = get_secret('prod_fb_video_reels')

def translate_text(text, source_lang, target_lang, uid):

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
    translation=response.json()['trans']
    logger.log(f"Got translation for: {text}. The translation is: {translation}", uid=uid)
    return translation

def translate_srt(file_path, output_file, source_lang, target_lang, uid):
    start_time = time.time()
    subs = pysrt.open(file_path)
    for sub in subs:
        translated_text = translate_text(sub.text, source_lang, target_lang, uid)
        sub.text = translated_text
    subs.save(output_file, encoding='utf-8')
    end_time = time.time()
    logger.log(f"Time Taken For Google Translate: {end_time - start_time} seconds", uid=uid)

