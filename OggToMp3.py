import os
from pydub import AudioSegment

# Устанавливаем переменные среды для указания на ffmpeg и ffprobe
os.environ["PATH"] += os.pathsep + r'C:\ffmpeg\bin'

# Явно указываем путь к ffmpeg и ffprobe
AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"C:\ffmpeg\bin\ffprobe.exe"

# Функция для конвертации ogg в mp3
def convert_ogg_to_mp3(source_folder, target_folder):
    for subdir, dirs, files in os.walk(source_folder):
        for file in files:
            if file.endswith('.ogg'):
                ogg_path = os.path.join(subdir, file)
                relative_path = os.path.relpath(ogg_path, source_folder)
                mp3_relative_path = os.path.splitext(relative_path)[0] + '.mp3'
                mp3_path = os.path.join(target_folder, mp3_relative_path)

                os.makedirs(os.path.dirname(mp3_path), exist_ok=True)

                audio = AudioSegment.from_ogg(ogg_path)
                audio.export(mp3_path, format='mp3', bitrate='192k')

# Пути к исходной и целевой папке
source_folder = r'C:\Users\user\Downloads\1\OGG'
target_folder = r'C:\Users\user\Downloads\1\MP3'

convert_ogg_to_mp3(source_folder, target_folder)
