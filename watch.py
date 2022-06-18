# demo 监控文件夹下的所有变动

#-*- coding: utf-8 -*-

import os, threading
from watchdog.observers import Observer
from watchdog.events import *
from watchdog.utils.dirsnapshot import DirectorySnapshot, DirectorySnapshotDiff

class FileEventHandler(FileSystemEventHandler):
    def __init__(self, aim_path):
        FileSystemEventHandler.__init__(self)
        self.aim_path = aim_path
        self.timer = None
        self.snapshot = DirectorySnapshot(self.core.proj_path)

    def on_any_event(self, event):
        if self.timer:
            self.timer.cancel()
        self.timer = threading.Timer(0.2, self.checkSnapshot)
        self.timer.start()

    def checkSnapshot(self):
        snapshot = DirectorySnapshot(self.aim_path)
        diff = DirectorySnapshotDiff(self.snapshot, snapshot)
        self.snapshot = snapshot
        self.timer = None
        #下面是应处理的各种事项
        print("files_created:", diff.files_created)
        print("files_deleted:", diff.files_deleted)
        print("files_modified:", diff.files_modified)
        print("files_moved:", diff.files_moved)
        print("dirs_modified:", diff.dirs_modified)
        print("dirs_moved:", diff.dirs_moved)
        print("dirs_deleted:", diff.dirs_deleted)
        print("dirs_created:", diff.dirs_created)
        # 接下来就是你想干的啥就干点啥，或者该干点啥就干点啥
        pass

class DirMonitor(object):
    """文件夹监视类"""

    def __init__(self, aim_path):
        """构造函数"""
        self.aim_path= aim_path
        self.observer = Observer()

    def start(self):
        """启动"""
        event_handler = FileEventHandler(self.aim_path)
        self.observer.schedule(event_handler, self.aim_path, True)
        self.observer.start()

    def stop(self):
        """停止"""
        self.observer.stop()

if __name__ == "__main__":
    monitor = DirMonitor(r"C:\Users\W\Desktop\folder\gitfolder")
    monitor.start()
