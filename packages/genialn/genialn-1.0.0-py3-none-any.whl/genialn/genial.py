import time
import platform
import functools
import threading

class Speed:
    def __init__(self, use_cache=False, use_threads=False):
        self.use_cache = use_cache
        self.use_threads = use_threads
        self.threads = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for thread in self.threads:
            thread.join()
        self.threads = []

    def cache(self, func):
        if self.use_cache:
            return functools.lru_cache(maxsize=None)(func)
        else:
            return func

    def run_in_thread(self, func, *args, **kwargs):
        if self.use_threads:
            thread = threading.Thread(target=func, args=args, kwargs=kwargs)
            self.threads.append(thread)
            thread.start()
        else:
            func(*args, **kwargs)

class Slowed:
    def __init__(self, delay=0.1):
        self.delay = delay

    def slowed(self):
        if platform.system() != "Emscripten":
            time.sleep(self.delay)
        else:
            print("Замедление пропущено, так как программа запущена в браузере.")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if platform.system() != "Emscripten":
            time.sleep(self.delay)
        else:
            print("Замедление пропущено, так как программа запущена в браузере.")
