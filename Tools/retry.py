'''
Description

A decorator to repeat the execution of a function for specified times.

Some generated result of the function are the best, some are aceepted and some are rejected.

The target of this decorator is to help the function find out the best result.

Attention please, this module is not guaranteed to return the expected result.

Because the function may be impossible to generate an expected result.
'''

from functools import wraps

def conditional_repeat(best_stop_time = 5, must_stop_time = 10):
    def decorator(func):
        def wrapper(*args, **kwargs):
            repeat_time = 0
            while True:
                repeat_time += 1
                wrap_result = func(*args, **kwargs)
                # the return value of the function must be a dict
                # and it is required to have keys, best_repeat and must_repeat
                if type(wrap_result) != type({}):
                    raise TypeError('return value must be a dict')
                # best_repeat: a boolean, indicate whether it is better to repeat again, default to False
                # must_repeat: a boolean, indicate whether it is required to repeat again, default to False
                best_repeat = wrap_result.get('best_repeat', False)
                must_repeat = wrap_result.get('must_repeat', False)
                if (
                    (repeat_time > must_stop_time) or
                    (repeat_time > best_stop_time and not must_repeat) or
                    (repeat_time < best_stop_time and not must_repeat and not best_repeat)
                ):
                    break
            return wrap_result
        return wraps(func)(wrapper)
    return decorator

if __name__ == '__main__':
    import time
    import random

    random.seed(int(time.time() * 1000))

    # assuming that the return value is required to be an integer that must range between 1 and 10 and better equal to 1
    @conditional_repeat(5, 10)
    def rand_int(choices_list):
        chosen_number = random.choice(choices_list)
        must_repeat = False
        best_repeat = False
        if not (1 <= chosen_number <= 10):
            must_repeat = True
        if chosen_number != 1:
            best_repeat = True
        result = {
            'best_repeat': best_repeat,
            'must_repeat': must_repeat,
            'data': chosen_number
        }
        result = []
        return result

    # now we do not know what number is in the list
    choices = list(range(1, 31))
    random.shuffle(choices)
    choices = choices[: 20]

    # the function is choose a number from the list
    result = rand_int(choices)
    data = result['data']

    print('choice list:', choices)
    print('chosen data:', data)
