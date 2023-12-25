from google.cloud import translate_v2 as translate
import pysrt

def translate_srt(file_path, target_language):
    # Initialize the Google Cloud translator
    translator = translate.Client()

    # Load the subtitles
    subs = pysrt.open(file_path)

    # Translate each subtitle
    for sub in subs:
        translated_text = translator.translate(sub.text, target_language=target_language)['translatedText']
        sub.text = translated_text

    return subs

def save_translated_srt(subs, output_file):
    subs.save(output_file, encoding='utf-8')

# Example usage
input_srt = 'tests/transcription_en.srt'  # Path to your input SRT file
output_srt = 'tests/transcription_he_google.srt'  # Path for the translated SRT file
target_language = 'it'  # Target language (Spanish in this example)

translated_subs = translate_srt(input_srt, target_language)
save_translated_srt(translated_subs, output_srt)
