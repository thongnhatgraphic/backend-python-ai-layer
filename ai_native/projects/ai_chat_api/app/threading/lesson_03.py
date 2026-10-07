import threading
import time


def worker():
    print("Worker started")

    time.sleep(5)

    print("Worker finished")


thread = threading.Thread(
    target=worker,
    daemon=True,
)

thread.start()

print("Main thread finished")
