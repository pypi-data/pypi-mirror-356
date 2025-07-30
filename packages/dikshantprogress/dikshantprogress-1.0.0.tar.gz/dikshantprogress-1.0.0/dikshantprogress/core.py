import time
import threading
from typing import Callable, Optional

class ProgressBar:
    def __init__(self, total: int = 100, bar_length: int = 30):
        self.total = total
        self.bar_length = bar_length
        self.current = 0
        self.running = False
        
    def update(self, n: int = 1):
        """Update progress by n units"""
        self.current = min(self.current + n, self.total)
        self._draw()
        
    def _draw(self):
        progress = self.current / self.total
        bar = '█' * int(progress * self.bar_length)
        spaces = ' ' * (self.bar_length - len(bar))
        print(f'\r[{bar}{spaces}] {progress:.0%}', end='')
        
    def start(self):
        """Start the progress bar"""
        self.running = True
        self._draw()
        
    def complete(self):
        """Mark as completed"""
        self.current = self.total
        self._draw()
        print()  # Newline when done
        self.running = False

class TimedProgressBar(ProgressBar):
    def run_for(self, seconds: float):
        """Run progress bar for specified duration"""
        self.start()
        interval = seconds / self.total
        for _ in range(self.total):
            if not self.running:
                break
            time.sleep(interval)
            self.update()
        self.complete()

class TriggeredProgressBar(ProgressBar):
    def __init__(self, start_trigger: Callable, stop_trigger: Callable):
        super().__init__()
        self.start_trigger = start_trigger
        self.stop_trigger = stop_trigger
        
    def monitor(self):
        """Monitor triggers in background thread"""
        self.running = True
        threading.Thread(target=self._monitor_triggers, daemon=True).start()
        
    def _monitor_triggers(self):
        while not self.start_trigger():
            time.sleep(0.1)
            
        self.start()
        while not self.stop_trigger():
            self.update(1)
            time.sleep(0.1)
        self.complete()