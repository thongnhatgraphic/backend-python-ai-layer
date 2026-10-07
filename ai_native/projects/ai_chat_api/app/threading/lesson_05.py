import threading
import time

counter = 0

lock = threading.Lock()


def worker():
    global counter

    for _ in range(10_000):
        with lock:
            current = counter
            time.sleep(0)
            counter = current + 1


for n in range(5):
    threads = []
    print(f"run {n + 1}-time")
    for m in range(10):
        thread = threading.Thread(target=worker)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    print("Expected:", 100_000 * (n + 1))
    print("Actual:", counter)
