'''
Description

A decorator to check whether the execution of a function is timeout.

If timeout, raise an exception. If no, return the result.

Attention please, this module is just working in Unix System.
'''

import signal
import functools

class TimeoutError(Exception):
    def __init__(self, warn_info):
        super(TimeoutError, self).__init__()
        self.warn_info = warn_info
    def __str__(self):
        return self.warn_info

def check_timeout(second = 7):
    def decorator(func):
        def wrapper(*args, **kwargs):
            def treat_timeout(signum, frame):
                raise TimeoutError('Timeout Detected !')
            signal.signal(signal.SIGALRM, treat_timeout)
            signal.setitimer(signal.ITIMER_REAL, second)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result
        return functools.wraps(func)(wrapper)
    return decorator

if __name__ == '__main__':
    import time

    @check_timeout(3)
    def delay_operations(delay_time, num_x, num_y):
        time.sleep(delay_time)
        return (num_x + num_y)

    try:
        result = delay_operations(1, num_x = 7, num_y = 8)
    except TimeoutError as err_info:
        print('Error:', err_info)
    else:
        print('Success:', result) # Success: 15

    try:
        result = delay_operations(5, num_x = 7, num_y = 8)
    except TimeoutError as err_info:
        print('Error:', err_info) # Error: Timeout Detected !
    else:
        print('Success:', result)
