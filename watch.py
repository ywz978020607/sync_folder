# demo 监控文件夹下的所有变动
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
 
 
class MyHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        print(event.event_type, event.src_path)
 
 
event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, path='.', recursive=False)
observer.start()
try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    observer.stop()
observer.join()