from Queue import Queue
from threading import Thread
from time import sleep
q = Queue()
NUM = 3
JOBS = 10
def do_somthing(arg):
    print arg
def run():
    while 1:
        arg = q.get()
        do_somthing(arg)
        sleep(2)
        q.task_done()
for i in range(NUM):
    t = Thread(target=run)
    print t.name
    t.setDaemon(True)
    t.start()
for i in range(JOBS):
    q.put(i)
q.join()

