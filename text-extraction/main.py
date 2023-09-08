import PyPDF2
from gtts import gTTS
import time
import tkinter as tk
from tkinter import ttk, filedialog
import threading

import my_openai
from audio_queue import AudioQueue
from my_reader import MyReader

window = tk.Tk()
window.title("PDF Reader")
window.geometry("500x500")

is_processing = False
def stop_processing():
    global is_processing
    is_processing = False
    stop_processing_button.pack_forget()
    continue_processing_button.pack()


def start_processing():
    global is_processing
    is_processing = True
    threading.Thread(target=process_text, args=([int(start_page_entry.get())])).start()
    stop_processing_button.pack()
    process_text_button.pack_forget()

def continue_processing():
    global is_processing
    is_processing = True
    threading.Thread(target=process_text, args=([int(audio_queue.get_last_in_queue()[5:7])])).start()
    stop_processing_button.pack()

audio_queue = AudioQueue()
my_reader = MyReader()

def open_file_picker():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    my_reader.set_file_path(file_path)
    current_file_label.configure(text=file_path)
    page_count = my_reader.get_page_count()
    page_count_label.configure(text="Page Count: " + str(page_count))
    input_frame.pack()
    process_text_button.pack()

def process_text(start_page):
    print("Processing text")
    controls_frame.pack()
    file_path = my_reader.get_file_path()
    page = start_page - 1

    while page <= my_reader.get_page_count() and is_processing:
        queue = audio_queue.get_queue()
        if len(queue) < 5:
            text = my_reader.get_text_from_page(page)
            try:
                tts = gTTS(text=text, lang="en")
                tts.save(f"page_{page+1}.mp3")
            except AssertionError:
                page += 1
                continue
            audio_queue.add_to_queue(f"page_{page+1}.mp3")
            page += 1
        else:
            queue = audio_queue.get_queue()
            time.sleep(1)

select_file_button = ttk.Button(window, text="Open File", command=open_file_picker)
select_file_button.pack()

current_file_label = ttk.Label(window, text="Current PDF: No file selected")
page_count_label = ttk.Label(window, text="Page Count: No file selected")
current_file_label.pack()
page_count_label.pack()

input_frame = ttk.Frame(window)
start_page_label = ttk.Label(input_frame, text="Start Page: ")
start_page_entry = ttk.Entry(input_frame)
start_page_entry.insert(0, "1")
start_page_label.pack(side='left')
start_page_entry.pack(side='left')

process_text_button = ttk.Button(window, text="Process Text", command=start_processing)
stop_processing_button = ttk.Button(window, text="Stop Processing", command=stop_processing)
continue_processing_button = ttk.Button(window, text="Continue Processing", command=continue_processing)

def play_audio():
    audio_queue.start_thread()
    update_currently_playing()

controls_frame = ttk.Frame(window)
read_button = ttk.Button(controls_frame, text="Read", command=play_audio)
pause_button = ttk.Button(controls_frame, text="Pause", command=lambda: (audio_queue.pause(), pause_button.configure(text="Resume" if audio_queue.is_paused else "Pause")))
read_button.pack(side='left')
pause_button.pack(side='left')


def set_volume(volume):
    audio_queue.set_volume(float(volume) / 100)

# audio slider
audio_slider = ttk.Scale(controls_frame, from_=0, to=100, orient='horizontal', command=set_volume)
audio_slider.pack(side='left')

# currently playing label
currently_playing_label = ttk.Label(controls_frame, text="Currently Playing: ")
currently_playing_label.pack(side='left')

def update_currently_playing():
    currently_playing_label.configure(text="Currently Playing: " + str(audio_queue.get_current_file()) if audio_queue.get_current_file() is not None else "Still Processing Text")
    currently_playing_label.after(1000, update_currently_playing)

window.mainloop()