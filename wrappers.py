import functools


def yield_func_wrapper(f, n=3, *args, **kwargs):
    '''
    A wrapper for generator functions to test their behaviour.
    n: number of items to retreive
    '''
    l = []
    assert n >= 0
    for x in f(*args, **kwargs):
        l.append(x)
        n -= 1
        if n <= 0:
            break
    return l


def yield_to_return_function(f):
    def new_f(*args, **kwargs):
        for x in f(*args, **kwargs):
            a = x
            break
        return a
    return new_f


