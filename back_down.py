from __future__ import unicode_literals
import os
import shutil
import yt_dlp as youtube_dl
from pydub import AudioSegment
import re


def audio_download(url_video_youtube: str, ydl_opts: dict):

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url_video_youtube])

        info_dict = ydl.extract_info(url_video_youtube, download=False)
        audio_time_line = info_dict.get("chapters", None)
        print(f'{"-" * 50}\nDownload audio Successfully!\n{"-" * 50}')
    return audio_time_line


def audio_redactor(file_mp3_path, audio_path, time_line: list):
    time_line_quantity = len(time_line)
    now = 0
    for line in time_line:
        now += 1
        print(f"{'-' * 50}\nCreate audio #{line['title']}\n"
              f"Please wait....\nPROCESS {now}/{time_line_quantity}\n{'-' * 50}")
        try:
            endSec = int(line["end_time"])
            startSec = int(line["start_time"])
            file_name_to = line["title"]
            file_name_to = ''.join(re.split(r'[\\~|/]', file_name_to))
            startTime = startSec * 1000
            endTime = endSec * 1000
            song = AudioSegment.from_mp3(file_mp3_path)
            extract = song[startTime:endTime]
            extract.export(audio_path + f'\{file_name_to}.mp3', format="mp3")
            print(f'{"-" * 50}\n#{line["title"]} Created\n{"-" * 50}')
        except Exception as ex:
            print(f"{'-' * 50}\n Произошла ошибка в файле {file_mp3_path}\n {ex} \n{'-' * 50}")

    os.remove(file_mp3_path)
    print("Загрузка всех аудиофайлов успешно завершена 🎉🎉🎉")


def move_files(destination_folder, file_name):
    source_folder = "."

    source_path = os.path.join(source_folder, file_name)
    destination_path = os.path.join(destination_folder, file_name)

    try:
        shutil.move(source_path, destination_path)
        print(f"Файл успешно скачан в '{destination_folder}' 🎉")
    except FileNotFoundError:
        print(f"Ошибка: Файл или папка не найдены. ❌")
    except Exception as e:
        print(f"Произошла ошибка: {e} ❌")


def main(ydl_opts):
    file_name = "audioDownload.mp3"

    url = input("Введите ссылку для скачивания видео ")
    path_audio_files = input("Введите путь к папке для сохранения аудиофайлов ")

    if not os.path.exists(path_audio_files):
        print("Указанный путь к папке для сохранения аудиофайлов не существует!")
        return

    audio_time_line = audio_download(url, ydl_opts)

    if audio_time_line:
        audio_redactor(file_name, path_audio_files, audio_time_line)
    else:
        move_files(path_audio_files, file_name)


if __name__ == "__main__":
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audioDownload',
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    main(ydl_opts)
