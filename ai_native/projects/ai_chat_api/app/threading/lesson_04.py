import threading
import time

counter = 0


def worker():
    global counter
    for _ in range(10_000):
        current = counter
        time.sleep(0)
        counter = current + 1


threads = []


for n in range(3):
    for _ in range(10):
        thread = threading.Thread(target=worker)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("run", n)
    print("Expected:", 1_000_000)
    print("Actual:", counter)
