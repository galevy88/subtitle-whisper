import requests
import base64

def read_text_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

def call_api_and_save_video(text_file_path):
    text_for_json = read_text_from_file(text_file_path)
    if text_for_json is None:
        return "File not found"

    url = "http://3.238.98.134:3007/transcribe_audio"
    headers = {"Content-Type": "application/json"}
    
    data = {"audio": text_for_json}
    response = requests.put(url, json=data, headers=headers)

    if response.status_code == 200:
        base64_srt = response.json().get("base64_srt")
        if base64_srt:
            # Decoding the base64 string to get the SRT content
            srt_content = base64.b64decode(base64_srt)

            # Writing the decoded content to an SRT file
            srt_file_name = "transcription.srt"
            with open(srt_file_name, "wb") as file:
                file.write(srt_content)
            
            return f"SRT file saved as {srt_file_name}"
        else:
            return "No SRT data found in response"
    else:
        return f"Error: {response.status_code}"

if __name__ == "__main__":
    result = call_api_and_save_video('base64.txt')
    print(result)
