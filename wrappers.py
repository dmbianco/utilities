import functools


def yield_func_wrapper(f, n_results=3, *args, **kwargs):
    '''
    A wrapper for generator functions to test their behaviour.
    n: number of items to retreive
    '''
    l = []
    assert n_results >= 0
    for x in f(*args, **kwargs):
        l.append(x)
        n_results -= 1
        if n_results <= 0:
            break
    return l


def yield_to_return_function(f):
    def new_f(*args, **kwargs):
        for x in f(*args, **kwargs):
            a = x
            break
        return a
    return new_f


