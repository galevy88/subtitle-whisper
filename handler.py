from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import traceback
import os
from cloudwatch_logger import CloudWatchLogger as logger
import shutil
from encoding import encode_to_base64_response, save_base64_audio
from whisperer import run_whisper
from good_translator import translate_srt 
import uuid

app = FastAPI()

class AudioData(BaseModel):
    audio: str
    model_type: str = "tiny"
    lang: str = "en"

@app.get("/health")
def is_up():
    return {"status": "UP"}

@app.put("/transcribe_audio")
def transcribe_audio(data: AudioData):
    base64_audio = data.audio
    model_type = data.model_type
    target_lang = data.lang
    logger.log(f"Start working on whisper with parameters: model_type {model_type} , target_lang {target_lang}")

    if not base64_audio:
        raise HTTPException(status_code=400, detail="No audio data provided")

    uid = uuid.uuid4()
    logger.log(f"UUID for user is: {uid}")
    base_path = os.getcwd()
    dir_path = os.path.join(base_path, f'{uid}')
    audio_file_path = os.path.join(dir_path, 'audio.mp3')
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    logger.log(f"Start save base64 audio to path: {audio_file_path}")
    save_base64_audio(base64_audio, audio_file_path)
    logger.log(f"Finish save base64 audio to path: {audio_file_path}")

    try:
        return_code = run_whisper(audio_file_path, dir_path, model_type)
        srt_file_path = os.path.join(dir_path, 'audio.srt')

        if return_code == 0 and os.path.exists(srt_file_path):
            if target_lang != "en":
                translated_srt_path = os.path.join(dir_path, f'audio_{target_lang}.srt')
                translate_srt(srt_file_path, translated_srt_path, "en", target_lang)
                srt_file_path = translated_srt_path

            response_data = encode_to_base64_response(srt_file_path)
            return response_data
        else:
            raise HTTPException(status_code=500, detail="Transcription failed or SRT file not found")
        
    except Exception as e:
        print(f"Exception occurred: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        files_to_delete = ['audio.json', 'audio.txt', 'audio.tsv', 'audio.vtt']

        for file_name in files_to_delete:
            file_path = os.path.join(base_path, file_name)
            if os.path.exists(file_path):
                os.remove(file_path)
        
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
