import threading
import time

main_thread_id = threading.get_ident()
main_thread_name = threading.current_thread().name
main_thread_is_alive = threading.current_thread().is_alive()
print(
    f"main thread: \n id = {main_thread_id} \n name = {main_thread_name} \n is_alive = {main_thread_is_alive}"
)
print("\n\n\n")


def worker():
    print("Worker started")
    time.sleep(3)
    print("Worker finished")


thread_1 = threading.Thread(target=worker)


is_alive = thread_1.is_alive()
print(f"Before start: \n is_alive = {is_alive}")


thread_1.start()
is_alive = thread_1.is_alive()
print(f"After start: \n is_alive = {is_alive}")


# thread_1.join()
is_alive = thread_1.is_alive()
print(f"After join: \n is_alive = {is_alive}")
