callbacks = []

def add_callback(func):
    #enforce no duplicates
    if func not in callbacks:
        remove_callback(func)
        callbacks.append(func)

def remove_callback(func):
    if func in callbacks:
        callbacks.remove(func)

def run_callbacks(*args, **kwargs):
    """DONT CALL THIS! its internally used to trigger callbacks"""
    for func in callbacks:
        func(*args, **kwargs)
