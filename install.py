from google.cloud import texttospeech
import requests
import json
import os

# Instantiates a client
key_file = '/home/kuba/IdeaProjects/czytanie/tts-key.json'
client = texttospeech.TextToSpeechClient.from_service_account_file(key_file)

audio_config = texttospeech.types.AudioConfig(
    audio_encoding=texttospeech.enums.AudioEncoding.MP3)

levels = [
    ['dom', 'mama', 'kot', 'Ula', 'tata'],
    ['tam', 'ma', 'kota', 'jest', 'da'],
    ['koc', 'banan', 'słoń', 'zupa', 'stół'],
]

def get_audio(text, target_file_name, voice_name='Wavenet-D'):

    if not target_file_name:
        target_file_name = f'{text}.mp3'

    voice = texttospeech.types.VoiceSelectionParams(
        language_code = 'pl-PL',
        name = f'pl-PL-{voice_name}',
        ssml_gender = texttospeech.enums.SsmlVoiceGender.NEUTRAL)

    synthesis_input = texttospeech.types.SynthesisInput(text=text)
    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    # The response's audio_content is binary.
    with open(target_file_name, 'wb') as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print(f'Audio content written to file "{target_file_name}"')

    return target_file_name

tmp_dir = 'tmp'
os.makedirs(tmp_dir, exist_ok=True)

for resource_file in (os.path.join(root, file) for root, dirs, files in os.walk('resources') for file in files):
    os.rename(resource_file, os.path.join(tmp_dir, os.path.split(resource_file)[1]))


for i in range(len(levels)):
    dir = os.path.join('resources', 'sounds', str(i))
    os.makedirs(dir, exist_ok=True)
    for txt in levels[i]:
        file_name = txt + '.mp3'
        file_path = os.path.join(dir, file_name)
        if os.path.isfile(os.path.join(tmp_dir, file_name)):
            os.rename(os.path.join(tmp_dir, file_name), file_path)
            print(f'{txt} moved from {tmp_dir} to {dir}')
        else:
            get_audio(txt, file_path)

