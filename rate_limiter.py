import time

# OpenAQ rate limits to 60/min and 2000/hr

class RateLimiter:
    def __init__(self, min_interval=1.1):
        self.min_interval = min_interval
        self.last_call = 0

    def wait(self):
        now = time.time()
        elapsed = now - self.last_call
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_call = time.time()