import threading
import time

stop_event = threading.Event()


def worker():
    print("Worker: started")

    while not stop_event.wait(10):
        print("Worker: heartbeat")
        print("time out", stop_event.is_set())

    print("Worker: stopped")


thread = threading.Thread(target=worker)

thread.start()

time.sleep(2)

thread.join()

print("Main: sending stop signal")
