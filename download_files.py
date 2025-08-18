import tkinter as tk
import threading
import queue
from tkinter import ttk
from back_down import main, audio_video_download


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Загрузка Аудио / Видео")
        self.geometry(f"{width}x{height}")
        self.resizable(False, False)

        self.config(bg="#C7FCEC")

        self.entry_link = tk.Entry(width=int(int(width * 0.8) / 8))
        self.entry_link.pack(pady=(10, 5))
        self.link_download = tk.StringVar()
        self.link_download.set("Ссылка для скачивания")
        self.entry_link["textvariable"] = self.link_download

        self.entry_path = tk.Entry(width=int(int(width * 0.8) / 8))
        self.entry_path.pack(pady=(5, 5))
        self.path_download = tk.StringVar()
        self.path_download.set("E:\downloads youtube")
        self.entry_path["textvariable"] = self.path_download

        # Очередь для обмена данными между потоком и GUI
        self.queue = queue.Queue()

        # Прогрессбар
        self.progressbar = ttk.Progressbar(self, length=300, orient=tk.HORIZONTAL, mode='determinate', maximum=100)
        self.progressbar.pack(padx=10, pady=10)

        # Кнопки запуска скачивания Аудио и Видео
        frame = tk.Frame(self, bg="#C7FCEC")
        frame.pack(expand=True)
        self.button_audio = tk.Button(frame,
                                      text="Музыка",
                                      width=10,
                                      height=2,
                                      bg="#b9f264",
                                      command=self.start_action_audio)
        self.button_video = tk.Button(frame,
                                      text="Видео",
                                      width=10,
                                      height=2,
                                      bg="#b9f264",
                                      command=self.start_action_video)

        self.button_audio.pack(side=tk.LEFT, padx=(0, 10))
        self.button_video.pack(side=tk.LEFT)

    def prepare_actions(self):
        self.button_video.config(state=tk.DISABLED)
        self.button_audio.config(state=tk.DISABLED)
        self.progressbar['value'] = 0
        link = self.link_download.get()
        path = self.path_download.get()
        return link, path

    def start_action_audio(self):
        link, path = self.prepare_actions()

        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['outtmpl'] = 'audioDownload'
        ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]

        # Запуск фоновой задачи в отдельном потоке
        thread = threading.Thread(target=main, args=(link, path, ydl_opts, self.queue))
        thread.start()
        self.after(100, lambda: self.poll_thread(thread))

    def start_action_video(self):
        link, path = self.prepare_actions()

        ydl_opts['format'] = 'bestvideo+bestaudio/best'
        ydl_opts['outtmpl'] = f'{path}/%(title)s.%(ext)s'
        ydl_opts.pop('postprocessors', None)

        video, steps = True, 2
        thread = threading.Thread(target=audio_video_download, args=(link, ydl_opts, self.queue, steps, video))
        thread.start()
        self.after(100, lambda: self.poll_thread(thread))

    def poll_thread(self, thread):
        self.check_queue()
        if thread.is_alive():
            self.after(100, lambda: self.poll_thread(thread))
        else:
            self.button_audio.config(state=tk.NORMAL)
            self.button_video.config(state=tk.NORMAL)

    def check_queue(self):
        while not self.queue.empty():
            step = self.queue.get()
            self.progressbar.step(step)


width = 600
height = 160

ydl_opts = {
    'noplaylist': True,
}

app = App()
app.mainloop()
