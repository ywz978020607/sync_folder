#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import os
import re
import platform

from subprocess import call
from shutil import copy
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading

# git root path for files to push to remote
# DIR_FOR_GIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_FOR_GIT = os.path.dirname(os.path.abspath(__file__))

# folders to synchronize
SYNC_FOLDER_LIST = []
f = open(os.path.join(DIR_FOR_GIT, "file_list.txt"), "r")
try:
    SYNC_FOLDER_LIST = [line.strip().replace('\\','/') for line in f] # if os.path.isfile(line.strip().replace('\\','/'))]
except Exception as e:
    raise e
finally:
    f.close()

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self) -> None:
        super().__init__()
        # self.timer = None
        self.timer = threading.Timer(3, self.checkSnapshot) #延后
        self.timer.start()
        self.push_set = set()
        for SYNC_PATH in SYNC_FOLDER_LIST:
            self.push_set.add((SYNC_PATH, "initrefresh"))
    def on_any_event(self, event):
        # 先判断是否有效
        print(event.event_type, event.src_path)
        src_path = event.src_path.replace('\\','/')
        for SYNC_PATH in SYNC_FOLDER_LIST:
            if SYNC_PATH in src_path and ".git" not in src_path: #排除.git
                # do push and delay
                if self.timer:
                    self.timer.cancel()
                self.timer = threading.Timer(3, self.checkSnapshot) #延后
                self.push_set.add((SYNC_PATH, src_path))
                self.timer.start()

    def checkSnapshot(self):
        while len(self.push_set) > 0:
            SYNC_PATH, src_path = self.push_set.pop()
            os.chdir(SYNC_PATH)
            git_add_cmd = "git add -A"
            git_commit_cmd = "git commit -m " + re.escape("Update "+os.path.basename(src_path))
            if platform.system() == "Windows":
                git_commit_cmd = "git commit -m Update."
            git_pull_cmd = "git pull origin master"
            git_push_cmd = "git push origin master"
            call(
                git_add_cmd + "&&" +
                git_commit_cmd + "&&" +
                git_pull_cmd + "&&" +
                git_push_cmd,
                shell=True
            )

if __name__ == "__main__":
    observer = Observer()
    event_handler = FileChangeHandler()

    for file_path in SYNC_FOLDER_LIST:
        observer.schedule(event_handler, path=os.path.dirname(os.path.realpath(file_path)), recursive=True)

    observer.start()

    try:
        while True:
            time.sleep(5)
            with open(os.path.join(DIR_FOR_GIT, "run.txt"),"w") as f:
                f.write(time.asctime(time.localtime(time.time()))) 
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
