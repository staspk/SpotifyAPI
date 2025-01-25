import time

class Timer:

    def start(msg = ''):
        Timer.start = time.perf_counter()
        if msg:
            print(f'{msg}. Timer Started...')

    def elapsed(msg):
        end = time.perf_counter()
        elapsed = (end - Timer.start) * 1000
        if elapsed > 1000:
            elapsed = elapsed / 1000
            print(f'Operation timed at: {elapsed:.3f}s')
        else:
            print(f'Operation timed at: {elapsed:.3f}ms')

    def stop():
        end = time.perf_counter()
        elapsed = (end - Timer.start) * 1000
        if elapsed > 1000:
            elapsed = elapsed / 1000
            print(f'Operation timed at: {elapsed:.3f}s')
        else:
            print(f'Operation timed at: {elapsed:.3f}ms')