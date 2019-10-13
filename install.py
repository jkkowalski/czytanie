import requests
import json
import os

levels = [
    ['a', 'ma', 'am', 'mama'],
    ['ta', 'at', 'tam', 'mata', 'tata', 'tama'],
    ['o', 'om', 'mo', 'ot', 'to', 'oto', 'tom', 'tamto', 'atom'],
    ['i', 'im', 'mi', 'it', 'ti', 'Timi', 'Mimi', 'Mati'],
    ['da', 'do', 'di', 'ad', 'od', 'id', 'dama', 'data', 'moda'],
    ['ko', 'ka', 'ki', 'ok', 'ak', 'ik', 'kot', 'kotka', 'kotki', 'kto', 'kita', 'kok', 'komoda', 'oko', 'maki', 'dok'],
    ['la', 'lo', 'li', 'al', 'ol', 'lala', 'lama', 'lato', 'lada', 'loki', 'Lola', 'dola', 'molo', 'Lila', 'Tola', 'Ola', 'Ala']
]

def get_sound(text, target_file_name:None):
    url='https://ttsmp3.com/makemp3.php'
    data = {'msg': text, 'lang': 'Maja', 'source': 'ttsmp3'}

    resp = requests.post(url, data)
    data = json.loads(resp.text)

    print(resp.text)
    mp3 = requests.get(data['URL'])
    if not target_file_name:
        target_file_name = text + '.mp3'
    with open(target_file_name, 'wb') as mp3f:
        mp3f.write(mp3.content)
    print(f'Saved {target_file_name}')
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
            get_sound(txt, file_path)
