"""
a = (5,)
b = (5)
a
(5,)
b
5
for element in a:
    print(a)

(5,)
for element in b:
    print(element)

Traceback (most recent call last):
  File "<input>", line 1, in <module>
TypeError: 'int' object is not iterable

"""

import threading
import time
from queue import Queue


def chef(amount: int, q):
    print('I don\'t want to work!')
    time.sleep(amount)
    print("I'm done with not working!")
    q.put(amount+1)


def worker():
    print('im doing serious work here')
    time.sleep(1)
    print('im done with working for today')


def main():
    queue = Queue()
    for i in range(5):
        threading.Thread(target=worker).start()
    task = threading.Thread(target=chef, args=(3, queue))
    task.start()

    print('got from chef', queue.get())

if __name__ == '__main__':
    main()
