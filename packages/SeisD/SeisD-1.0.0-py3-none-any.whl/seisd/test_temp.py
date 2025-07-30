import threading
import time

class MyThread(threading.Thread):
    def __init__(self, stop_event):
        super(MyThread, self).__init__()
        self.stop_event = stop_event

    def run(self):
        while not self.stop_event.is_set():
            print(f"{self.name} is running")
            time.sleep(1)
        print(f"{self.name} is stopping")
        


# 创建一个线程停止事件
stop_event = threading.Event()
length = len(threading.enumerate())
print('当前运行的线程数为：%d'%length)
# 创建并启动子线程
t1 = MyThread(stop_event)
t1.start()

length = len(threading.enumerate())
print('当前运行的线程数为：%d'%length)

time.sleep(2)  # 主线程等待5秒

# 通知子线程停止
stop_event.set()

# 等待子线程退出
# t1.join(timeout=0.5)
length = len(threading.enumerate())
print('当前运行的线程数为：%d'%length)

print("Main thread continues running")
time.sleep(1)  # 主线程等待5秒

length = len(threading.enumerate())
print('当前运行的线程数为：%d'%length)

import threading
import time
from tkinter import Tk, Button

class ExampleApp:
    def __init__(self, root):
        self.root = root
        self.thread = None
        self.stop_event = threading.Event()

        self.start_button = Button(root, text="Start Thread", command=self.start_thread)
        self.start_button.pack()

        self.stop_button = Button(root, text="Stop Thread", command=self.stop_thread)
        self.stop_button.pack()

    def worker(self):
        while not self.stop_event.is_set():
            print("Thread is running...")
            time.sleep(1)

    def start_thread(self):
        if self.thread is None or not self.thread.is_alive():
            self.stop_event.clear()  # 清除停止事件
            self.thread = threading.Thread(target=self.worker)
            self.thread.start()
        else:
            print("Thread is already running.")
        length = len(threading.enumerate())
        print('当前运行的线程数为：%d' % length)
        for thread in threading.enumerate():
            print(f"Thread name: {thread.name}, is_alive: {thread.is_alive()}, is_daemon: {thread.daemon}")


    def stop_thread(self):
        if self.thread is not None and self.thread.is_alive():
            self.stop_event.set()  # 设置停止事件
            self.thread.join()  # 等待线程结束
            self.thread = None
            print("Thread has been stopped.")
        length = len(threading.enumerate())
        print('当前运行的线程数为：%d' % length)
        for thread in threading.enumerate():
            print(f"Thread name: {thread.name}, is_alive: {thread.is_alive()}, is_daemon: {thread.daemon}")


root = Tk()
app = ExampleApp(root)
root.mainloop()
