from flask import Flask, request, jsonify
import os
import datetime
import shutil  # Import shutil module
from encoding import encode_to_base64_response, save_base64_audio
from whisperer import run_whisper

app = Flask(__name__)

@app.route('/transcribe_audio', methods=['PUT'])
def transcribe_audio():
    data = request.json
    base64_audio = data.get("audio")
    model_type = data.get("model_type", "tiny")

    if not base64_audio:
        return jsonify({"error": "No audio data provided"}), 400

    iat = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    base_path = os.getcwd()
    dir_path = os.path.join(base_path, f'{iat}')
    audio_file_path = os.path.join(dir_path, 'audio.mp3')

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    save_base64_audio(base64_audio, audio_file_path)

    try:
        return_code = run_whisper(audio_file_path, dir_path, model_type)
        srt_file_path = os.path.join(dir_path, 'audio.srt')

        if return_code == 0 and os.path.exists(srt_file_path):
            data = encode_to_base64_response(srt_file_path)
            return data
        else:
            return jsonify({"error": "Transcription failed or SRT file not found"}), 500
    finally:
        files_to_delete = ['audio.json', 'audio.txt', 'audio.tsv', 'audio.vtt']

        # Delete the specified files if they exist
        for file_name in files_to_delete:
            file_path = os.path.join(base_path, file_name)
            if os.path.exists(file_path):
                os.remove(file_path)
        
        # Delete the IAT directory and everything inside it
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
