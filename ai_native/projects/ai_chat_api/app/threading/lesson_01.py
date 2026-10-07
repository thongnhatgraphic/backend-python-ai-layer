import os
import threading

process_id = os.getpid()

thread_id = threading.get_ident()

thread_name = threading.current_thread().name

print("Process Id: ", process_id)
print("Thread Id: ", thread_id)
print("Thread Name: ", thread_name)


def do_something(worker_name: str):
    for i in range(5):
        print(f"{worker_name} count: {i}")


def worker1():
    do_something("worker 1")


def worker2():
    do_something("worker 2")


def worker3():
    do_something("worker 3")


thread_1 = threading.Thread(target=worker1)
thread_2 = threading.Thread(target=worker2)
thread_3 = threading.Thread(target=worker3)

thread_1.start()
thread_2.start()
thread_3.start()

thread_1.join()
thread_2.join()
thread_3.join()
