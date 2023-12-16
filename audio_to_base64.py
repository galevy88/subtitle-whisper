import base64

def convert_audio_to_base64_and_save(audio_file_path, output_txt_file):
    try:
        # Read the audio file and encode it to base64
        with open(audio_file_path, 'rb') as audio_file:
            encoded_audio = base64.b64encode(audio_file.read()).decode('utf-8')
        
        # Write the base64 string to a text file
        with open(output_txt_file, 'w') as txt_file:
            txt_file.write(encoded_audio)
        return True
    except FileNotFoundError:
        return False

# Using the function to convert an audio file and save the result to a text file
success = convert_audio_to_base64_and_save('audio.mp3', 'base64.txt')

if success:
    print('The audio was successfully converted to base64 and saved to a text file.')
else:
    print('File not found. Make sure the audio file path is correct.')
