import os
import re

user_path = 'E:\downloads youtubefdf'
res = os.path.exists(user_path)
print(res)


def audio_redactor(file_mp3_path, title_name, time_line: list):
    title_name = ''.join(re.split(r'[.;!:?*,()[@$%&-~|/-]', title_name))
    os.mkdir(title_name)
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
            startTime =startSec * 1000
            endTime = endSec * 1000
            song = AudioSegment.from_mp3(file_mp3_path)
            extract = song[startTime:endTime]
            dir = r'E:\downloads youtube' # Директория для сохранения аудио
            extract.export(dir + f'\{file_name_to}.mp3', format="mp3")
            path = dir + f'\{title_name}'
            print(f'{"-" * 50}\n#{line["title"]} Created\n{"-" * 50}')
        except Exception as ex:
            print(f"{'-' * 50}\n Произошла ошибка в файле {file_mp3_path}\n {ex} \n{'-' * 50}")
    os.remove('audioDownload.mp3')
    return path


def convert_wav_mp3(input_file, output_file):
    """
    Конвертирует аудиофайл из формата WAV в MP3.
    """
    try:
        # Загружаем WAV-файл
        audio_file = AudioSegment.from_wav(input_file)

        # Экспортируем в MP3. Можно указать битрейт, например '192k'
        audio_file.export(output_file, format="mp3", bitrate="320k")

        print(f"Файл '{input_file}' успешно сконвертирован в '{output_file}'! 🎉")
    except FileNotFoundError:
        print(f"Ошибка: Файл '{input_file}' не найден. ❌")
    except Exception as e:
        print(f"Произошла ошибка: {e} ❌")

    # Пример использования


def extract_audio(video_path, audio_path):
    """
    Извлекает аудио из видеофайла и сохраняет его в отдельный файл.

    :param video_path: Путь к исходному видеофайлу.
    :param audio_path: Путь, куда будет сохранён аудиофайл.
    """
    try:
        # Загружаем видеофайл. pydub автоматически определяет формат.
        video = AudioSegment.from_file(video_path)

        # Извлекаем аудиопоток.
        audio = video.set_channels(2) # Конвертируем в стерео

        # Экспортируем аудио в MP3 или любой другой формат.
        audio.export(audio_path, format="mp3")

        print(f"Аудио успешно извлечено и сохранено в {audio_path} 🎉")
    except Exception as e:
        print(f"Произошла ошибка: {e} ❌")


def download(url):
    ydl_opts = {
         'format': 'bestvideo+bestaudio/best',
         'outtmpl': '%(title)s.%(ext)s',
         'noplaylist': True,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        #ydl.download([url])

        info_dict = ydl.extract_info(url, download=False)
        audio_title = info_dict.get("title", None)
        audio_time_line = info_dict.get("chapters", None)
        print(f'{"-" * 50}\nDownload audio Successfully!\n{"-" * 50}')
        extract_audio("Музыка the best.mp4", "Музыка the best audio.mp3")
    return 'Музыка the best audio.mp3', audio_title, audio_time_line