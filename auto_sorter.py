import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCH_FOLDER = "incoming"
OUTPUT_FOLDER = "organized"

def move_file(file_path):
    file_name = os.path.basename(file_path)

    if file_name.endswith(".pdf"):
        folder = "PDFs"
    elif file_name.endswith(".jpg") or file_name.endswith(".png"):
        folder = "Images"
    elif file_name.endswith(".txt"):
        folder = "Text"
    else:
        folder = "Other"

    destination = os.path.join(OUTPUT_FOLDER, folder)
    os.makedirs(destination, exist_ok=True)

    new_path = os.path.join(destination, file_name)

    try:
        shutil.move(file_path, new_path)
        print(f"Moved {file_name} → {folder}")
    except Exception as e:
        print(f"Error: {e}")


class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            time.sleep(1)
            move_file(event.src_path)


def start():
    os.makedirs(WATCH_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    observer = Observer()
    observer.schedule(Handler(), WATCH_FOLDER, recursive=False)
    observer.start()

    print("Watching folder: incoming")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":
    start()
