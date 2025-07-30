# dikshantprogress

[![PyPI](https://img.shields.io/pypi/v/dikshantprogress)](https://pypi.org/project/dikshantprogress/)
![Python](https://img.shields.io/pypi/pyversions/dikshantprogress)

Customizable progress bars with time-based and event-triggered controls.

## Features
- Time-based progress bars
- Event-triggered progress
- Thread-safe operations
- Customizable display

## Installation
```bash
pip install dikshantprogress
```

## Basic Usage
```python
from dikshantprogress import TimedProgressBar

# Run for 5 seconds
bar = TimedProgressBar(total=100)
bar.run_for(5)
```

## Advanced Usage
```python
from dikshantprogress import TriggeredProgressBar

# Event-based progress
def start_condition():
    return server_online()

def stop_condition():
    return download_complete()

bar = TriggeredProgressBar(start_condition, stop_condition)
bar.monitor()
```