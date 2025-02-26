import time

class Timer:

    def start(msg = ''):
        if msg:
            print(f'{msg}. Timer Started...')
            
        Timer.start_time = time.perf_counter()

    def elapsed(msg):
        end = time.perf_counter()
        elapsed = (end - Timer.start_time) * 1000
        if elapsed > 1000:
            elapsed = elapsed / 1000
            print(f'Operation timed at: {elapsed:.3f}s')
        else:
            print(f'Operation timed at: {elapsed:.3f}ms')

    def stop():
        end = time.perf_counter()
        elapsed = (end - Timer.start_time) * 1000
        if elapsed > 1000:
            elapsed = elapsed / 1000
            print(f'Operation timed at: {elapsed:.3f}s')
        else:
            print(f'Operation timed at: {elapsed:.3f}ms')

        Timer.start_time = None

        