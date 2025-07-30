import unittest
import time
from dikshantprogress import ProgressBar, TimedProgressBar

class TestProgressBar(unittest.TestCase):
    def test_basic_progress(self):
        bar = ProgressBar(total=10)
        bar.start()
        for _ in range(10):
            bar.update(1)
        bar.complete()
        
    def test_timed_progress(self):
        bar = TimedProgressBar(total=20)
        start = time.time()
        bar.run_for(2)  # 2 seconds
        self.assertAlmostEqual(time.time() - start, 2, delta=0.1)

if __name__ == '__main__':
    unittest.main()