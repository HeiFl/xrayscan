import queue
import threading
import subprocess

exitFlag = 0

class myThread (threading.Thread):
    def __init__(self,q):
        threading.Thread.__init__(self)
        self.q = q
    def run(self):
        xray_scan(self.q)

def xray_scan(q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            url = q.get()
            queueLock.release()
            cmd = ["./xray_darwin_amd64", "webscan", "--basic-crawler", url, "--html-output", "report__datetime__.html","--webhook-output", "http://127.0.0.1:5000/webhook"]
            rsp = subprocess.Popen(cmd)
            output, error = rsp.communicate()
            print(output)
        else:
            queueLock.release()


threadnum = 10
url_list = []
file = open("url.txt")
for text in file.readlines():
    text = text.strip('\n')
    url_list.append(text)
queueLock = threading.Lock()
workQueue = queue.Queue(1000)
threads = []

for tName in range(10):
    thread = myThread(workQueue)
    thread.start()
    threads.append(thread)
queueLock.acquire()
for word in url_list:
    workQueue.put(word)
queueLock.release()

while not workQueue.empty():
    pass
exitFlag = 1
for t in threads:
    t.join()
print("退出主线程")
