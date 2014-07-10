#!/usr/bin/env python
from Queue import Queue
from threading import Thread
from time import time
import urllib2

hosts = ['http://www.baidu.com', 'http://www.hao123.com']

queue = Queue()

class ThreadUrl(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            host = self.queue.get()
            url = urllib2.urlopen(host)
            print url.read(1024)
            self.queue.task_done()
        
start = time()
def main():
    for i in range(2):
        t = ThreadUrl(queue)
        t.setDaemon(True)
        t.start()
    for host in hosts:
        queue.put(host)
    queue.join()
main()
print 'Elapsed time : %s' %(time() - start)
