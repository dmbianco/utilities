from itertools import chain

def is_iterable(some_object):
    '''
    Returns True if an object is iterable.
    '''
    try:
        iter(some_object)
        return True
    except TypeError:
        return False


def flatten_iterable(iterable, levels=1, flatten_string=False, debug_mode=False):
    """
    Flatten n levels of nesting recursively.
    """
    if debug_mode:
        print(iterable, levels, not iterable, not is_iterable(iterable), levels <= 0, not flatten_string, isinstance(iterable, str))
    if not iterable or not is_iterable(iterable)\
        or levels <= 0 or (not flatten_string and isinstance(iterable, str)):
        if not isinstance(iterable, str):
            return iterable
        else:
            return [iterable]
    if is_iterable(iterable[0]):
        args_1 = [iterable[0], levels-1, flatten_string]
        args_2 = [iterable[1:], levels, flatten_string]
        return flatten_iterable(*args_1) + flatten_iterable(*args_2)
    args = [iterable[1:], levels, flatten_string]
    return iterable[:1] + flatten_iterable(*args)





if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description='Test functions')

    function_list = ("is_iterable", "flatten_iterable")
    for x in function_list:
        cmd = '--{}'.format(x)
        help = 'Test {} function.'.format(x)
        parser.add_argument(cmd, help=help, required=False, action='store_true')
    parser.add_argument("--test_all", help="Test all functions",
                        required=False, action='store_true')
    
    args = vars(parser.parse_args())
    if args["test_all"]:
        for x in args:
            args[x] = True

    if args["is_iterable"]:
        print("TESTING id_from_datetime")
        for x in (dict(), list(), "AA", 1):
            print(x, is_iterable(x))

    if args["flatten_iterable"]:
        print("TESTING flatten_iterable")
        l = [[[1,3],2], [3,[4,5],5]]
        print("Initial list:", l)
        print("Flattened list (1 level):", list(flatten_iterable(l, levels=1)))
        print("Flattened list (2 levels):", list(flatten_iterable(l, levels=2)))
        print("Flattened list (5 levels):", list(flatten_iterable(l, levels=5)))
        l = [[["AA","B"],2], [3,["CC",5],5]]
        print("Initial list:", l)
        print("Flattened list (2 levels):", list(flatten_iterable(l, levels=2, flatten_string=False)))
        print("Flattened list (5 levels):", list(flatten_iterable(l, levels=5, flatten_string=False)))
