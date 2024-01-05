from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import traceback
import os
import shutil
from cloudwatch_logger import CloudWatchLogger as logger
from encoding import encode_to_base64_response, save_base64_audio
from whisperer import run_whisper
from good_translator import translate_srt
import logging
import warnings

warnings.filterwarnings("ignore")
import argparse
import json

parser = argparse.ArgumentParser(description='Run FastAPI server.')
parser.add_argument('--port', type=int, default=3000, help='Port to run the server on')
args = parser.parse_args()

app = FastAPI()

class AudioData(BaseModel):
    audio: str
    model_type: str = "tiny"
    lang: str = "en"
    uid: str

@app.get("/health")
def is_up():
    return {"status": "UP"}

@app.put("/transcribe_audio")
def transcribe_audio(data: AudioData):
    uid = data.uid
    try:
        logger.log(
            f"Start working on whisper with parameters: model_type {data.model_type}, target_lang {data.lang}, uid {uid}",
            uid=uid)

        if not data.audio:
            raise HTTPException(status_code=400, detail="No audio data provided")

        base_path = os.getcwd()
        dir_path = os.path.join(base_path, str(uid))
        audio_file_path = os.path.join(dir_path, 'audio.mp3')
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        save_base64_audio(data.audio, audio_file_path)
        return_code = run_whisper(audio_file_path, dir_path, data.model_type, uid)
        srt_file_path = os.path.join(dir_path, 'audio.srt')

        if return_code != 0 or not os.path.exists(srt_file_path):
            raise HTTPException(status_code=500, detail="Transcription failed or SRT file not found")

        response_data = {"base64_srt": encode_to_base64_response(srt_file_path)}

        if data.lang != "en":
            translated_srt_path = os.path.join(dir_path, f'audio_{data.lang}.srt')
            translate_srt(srt_file_path, translated_srt_path, "en", data.lang, uid)
            if os.path.exists(translated_srt_path):
                response_data["base64_translated_srt"] = encode_to_base64_response(translated_srt_path)

        return response_data

    except Exception as e:
        logger.log(f"Exception occurred: {e}", level=logging.ERROR, uid=uid)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=args.port)
