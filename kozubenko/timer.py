import time

class Timer:

    def start():
        Timer.start = time.perf_counter()

    def stop():
        end = time.perf_counter()
        elapsed = (end - Timer.start) * 1000
        print(f'Operation timed at: {elapsed:.3f}ms')