import tkinter as tk
from tkinter import messagebox
from back_down import main


class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.pack()

        self.entry_link = tk.Entry(width=int(int(width * 0.8) / 8))
        self.entry_link.pack(pady=(10, 5))

        self.link_download = tk.StringVar()
        self.link_download.set("Ссылка для скачивания")
        self.entry_link["textvariable"] = self.link_download

        self.entry_path = tk.Entry(width=int(int(width * 0.8) / 8))
        self.entry_path.pack(pady=(5, 5))

        self.path_download = tk.StringVar()
        self.path_download.set("Путь для сохранения файлов")
        self.entry_path["textvariable"] = self.path_download

        button = tk.Button(text="Выполнить", width=15, height=10, command=self.print_contents)
        button.pack(pady=10)

    def print_contents(self):
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
        link = self.link_download.get()
        path = self.path_download.get()
        message = main(ydl_opts, link, path)
        print(message)
        if message[0] == "Информация":
            messagebox.showinfo(message[0], message[1])
        else:
            messagebox.showerror(message[0], message[1])

# E:\downloads youtube
if __name__ == "__main__":

    width = 600
    height = 120

    root = tk.Tk()
    root.title("Загрузчик видео")
    root.geometry(f"{width}x{height}")
    root.resizable(False, False)

    myapp = App(root)

    myapp.mainloop()
