import os
import shutil
import yt_dlp as youtube_dl
from pydub import AudioSegment
import re
from tkinter import messagebox


def audio_video_download(url_video_youtube: str, ydl_opts: dict, queue, steps=2, video=False):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        queue.put(100 / steps)
        ydl.download([url_video_youtube])
        queue.put(100 / steps)

    if video:
        messagebox.showinfo("Готово!", "Видео успешно загружено 🎉")
    else:
        print(f'{"-" * 50}\nDownload Successfully!\n{"-" * 50}')


def get_info_by_video(ydl_opts: dict, url_video_youtube: str):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url_video_youtube, download=False)
        audio_time_line = info_dict.get("chapters", None)
        new_name = info_dict.get("title", None) + ".mp3"
    return audio_time_line, new_name


def audio_redactor(file_mp3_path: str, audio_path: str, time_line: list, steps: int, queue):
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
            return "Error", f"{'-' * 50}\n Произошла ошибка в файле {file_mp3_path}\n {ex} \n{'-' * 50}"

        queue.put(100 / steps)
    os.remove(file_mp3_path)
    return "Готово!", "Загрузка всех аудиофайлов успешно завершена 🎉🎉🎉"


def move_files(destination_folder: str, file_name: str, new_name: str):
    source_folder = "."
    title_name = re.sub(r'[^\w\s\.-]', '', new_name)
    os.rename(file_name, title_name)

    source_path = os.path.join(source_folder, title_name)
    destination_path = os.path.join(destination_folder, title_name)

    try:
        shutil.move(source_path, destination_path)
        return "Готово!", f"Файл успешно скачан в '{destination_folder}' 🎉"
    except FileNotFoundError:
        return "Error", f"Ошибка: Файл или папка не найдены. ❌"
    except Exception as e:
        return "Error", f"Произошла ошибка: {e} ❌"


def main(url, path_audio_files, ydl_opts, queue):
    file_name = "audioDownload.mp3"

    if not os.path.exists(path_audio_files):
        messagebox.showerror("Error", "Указанный путь к папке для сохранения аудиофайлов не существует!")
        exit(0)

    audio_time_line, new_name = get_info_by_video(ydl_opts, url)

    if audio_time_line:
        steps = len(audio_time_line) + 2
        audio_video_download(url, ydl_opts, queue, steps)
        message = audio_redactor(file_name, path_audio_files, audio_time_line, steps, queue)
    else:
        audio_video_download(url, ydl_opts, queue)
        message = move_files(path_audio_files, file_name, new_name)

    if message[0] == "Error":
        messagebox.showerror(message[0], message[1])
    else:
        messagebox.showinfo(message[0], message[1])
