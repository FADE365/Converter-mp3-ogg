import os
from pydub import AudioSegment

# Устанавливаем переменные среды для указания на ffmpeg и ffprobe
os.environ["PATH"] += os.pathsep + r'C:\ffmpeg\bin'

# Определяем конвертер и ffprobe для pydub
AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"C:\ffmpeg\bin\ffprobe.exe"

# Функция для конвертации mp3 в ogg
def convert_mp3_to_ogg(source_folder, target_folder):
    for subdir, dirs, files in os.walk(source_folder):
        for file in files:
            if file.endswith('.mp3'):
                mp3_path = os.path.join(subdir, file)
                relative_path = os.path.relpath(mp3_path, source_folder)
                ogg_relative_path = os.path.splitext(relative_path)[0] + '.ogg'
                ogg_path = os.path.join(target_folder, ogg_relative_path)

                os.makedirs(os.path.dirname(ogg_path), exist_ok=True)

                audio = AudioSegment.from_mp3(mp3_path)
                audio.export(ogg_path, format='ogg', bitrate='192k')

# Пути к исходной и целевой папке
source_folder = r'C:\Users\user\Downloads\1\MP3'
target_folder = r'C:\Users\user\Downloads\1\OGG_Work'

convert_mp3_to_ogg(source_folder, target_folder)
