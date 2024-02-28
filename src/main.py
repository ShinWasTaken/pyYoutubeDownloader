import tkinter as tk
import threading
import json
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from os import system

class GUI:
    def __init__(self):
        with open('config.json', 'r', encoding='utf8') as f:
            self.config = json.load(f)

        self.root = tk.Tk()
        self.root.title("Youtube Downloader")
        self.root.geometry("500x100")

        self.frame = ttk.Frame(self.root)
        self.frame.grid()

        self.root.bind("<Button-3>", self.RightClickToPaste)

        self.out_path = self.config["out"]

        self.label = tk.Label(self.frame, text="Please read reqs.txt if you haven't.")
        self.label.grid(column=0,row=0)

        self.entry = tk.Entry(self.frame, width=80)
        self.entry.grid(column=0,row=1)
        #self.entry.bind("<Button-3>", self.RightClickToPaste)

        self.combo = ttk.Combobox(self.frame, state="readonly", values=["Sound", "Video"])
        self.combo.current(0)
        self.combo.grid(column=0,row=2)

        self.frame2 = tk.Frame(self.root)
        self.frame2.grid()

        self.openFolderButton = tk.Button(self.frame2, text="Save to...", command=self.OpenFolder)
        self.openFolderButton.grid(column=0, row=0)

        self.downloadButton = tk.Button(self.frame2, text="Download", command=self.Download)
        self.downloadButton.grid(column=1, row=0)

        self.root.mainloop()

    def OpenFolder(self):
        self.config["out"] = filedialog.askdirectory(initialdir="%HOMEPATH%/Desktop")
        with open('config.json', 'w', encoding='utf8') as f:
            json.dump(self.config, f, ensure_ascii=False)
        # re-read so it updates
        with open('config.json', 'r', encoding='utf8') as f:
            self.config = json.load(f)
        self.out_path = self.config["out"]

    def DownloadSound(self):
        system(f'yt-dlp --no-playlist -P {self.out_path} -f ba[ext=m4a] "{self.entry.get()}"')

    def DownloadVideo(self):
        system(f'yt-dlp --no-playlist -P {self.out_path} -f "bestvideo[ext=mov]+bestaudio[ext=m4a]/bestvideo+bestaudio" "{self.entry.get()}"')

    def Download(self):
        match self.combo.get():
            case "Sound":
                thread = threading.Thread(target=self.DownloadSound)
                thread.start()
            case "Video":
                thread = threading.Thread(target=self.DownloadVideo)
                thread.start()
            case _:
                self.warning = messagebox.Message(self.root, title="Warning", message="Please make sure you've selected an option.")
                self.warning.show()

    def RightClickToPaste(self, itGivesAnErrorWithoutThisDontDelete):
        self.entry.insert(0, self.root.clipboard_get())

GUI()
