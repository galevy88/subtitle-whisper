import requests
import base64
import uuid

def read_text_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

def call_api_and_save_srt(text_file_path):
    text_for_json = read_text_from_file(text_file_path)
    if text_for_json is None:
        return "File not found"

    uid = str(uuid.uuid4())

    url = "http://localhost:3005/transcribe_audio"
    headers = {"Content-Type": "application/json"}
    data = {
        "audio": text_for_json,
        "model_type": "tiny",
        "lang": "it",
        "uid": uid
    }

    response = requests.put(url, json=data, headers=headers)

    if response.status_code == 200:
        response_json = response.json()
        original_srt_base64 = response_json.get("base64_srt")
        translated_srt_base64 = response_json.get("base64_translated_srt")

        if original_srt_base64:
            original_srt_content = base64.b64decode(original_srt_base64)
            original_srt_file_name = f"{uid}_original.srt"
            with open(original_srt_file_name, "wb") as file:
                file.write(original_srt_content)

        if translated_srt_base64:
            translated_srt_content = base64.b64decode(translated_srt_base64)
            translated_srt_file_name = f"{uid}_translated.srt"
            with open(translated_srt_file_name, "wb") as file:
                file.write(translated_srt_content)

        return "SRT files saved" if original_srt_base64 or translated_srt_base64 else "No SRT data found in response"
    else:
        return f"Error: {response.status_code}"

if __name__ == "__main__":
    result = call_api_and_save_srt('base64.txt')
    print(result)
