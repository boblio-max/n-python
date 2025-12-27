import time
import sys
from functools import wraps
_data = {}

def info(message: str) -> None:

    _data[time.time()] = f"info: {message}"
    print(f"[INFO] {message}")
    
def wait(seconds: float) -> None:
    print(f"[TIME] waiting {seconds} sec")
    itr = 20
    for i in range(itr):
        print("☰", end=" ")
        time.sleep(seconds/itr)
    print()
        
def get_log() -> str:
    """returns the entire log."""
    logs = ""
    for timestamp, message in _data.items():
        logs += f"{time.ctime(timestamp)}: {message}\n"
    return logs

def set_log(new_data: dict) -> None:
    """changes the entire log to new__data."""
    global _data
    _data = new_data
    
def change_log_entry(timestamp: float, new_message: str) -> None:
    """changes a specific log entry."""
    if timestamp in _data:
        _data[timestamp] = new_message
        
def metric(name: str, value: float) -> None:
    _data[time.time()] = f"Metric {name}: {value}"
    print(f"[METRIC] {name}: {value}")
    
def timer(func):
    """A decorator that logs the time a function takes to execute."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start_time
        _data[time.time()] = f"Function {func.__name__} took {elapsed:.4f} seconds"
        print(f"[TIMER] Function {func.__name__} took {elapsed:.4f} seconds")
        return result
    return wrapper



