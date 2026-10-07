# Thread
#  │
#  ├── start() / join()
#  │       → lifecycle
#  │
#  ├── daemon
#  │       → process lifetime
#  │
#  ├── shared state
#  │       → race condition
#  │
#  ├── Lock
#  │       → bảo vệ shared state
#  │
#  └── Event          ← HÔM NAY
#         │
#         └── signal / coordination

import threading
import time

stop_event = threading.Event()


def worker():
    print("Worker: started")

    while not stop_event.is_set():
        print("Worker: working...")
        time.sleep(1)

    print("Worker: stopped")


thread = threading.Thread(target=worker)

thread.start()

time.sleep(3)

print("Main: sending stop signal")

stop_event.set()

thread.join()

print("Main: worker finished")
