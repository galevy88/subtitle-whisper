import pysrt
from googletrans import Translator, LANGUAGES

def translate_srt(file_path, target_language):
    # Load the subtitles
    subs = pysrt.open(file_path)

    # Initialize the translator
    translator = Translator()

    # Translate each subtitle
    for sub in subs:
        translated_text = translator.translate(sub.text, dest=target_language).text
        sub.text = translated_text

    # Return the translated subtitles
    return subs

def save_translated_srt(subs, output_file):
    subs.save(output_file, encoding='utf-8')

# Example usage
input_srt = 'tests/transcription_en.srt'  # Path to your input SRT file
output_srt = 'tests/transcription_he_bad_translate.srt'  # Path for the translated SRT file
target_language = 'he'  # Target language (Spanish in this example)

translated_subs = translate_srt(input_srt, target_language)
save_translated_srt(translated_subs, output_srt)
