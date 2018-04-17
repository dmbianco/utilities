

def is_iterable(some_object):
    '''
    Returns True if an object is iterable.
    '''
    try:
        iter(some_object)
        return True
    except TypeError:
        return False





if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description='Test the functionalities of the class')

    function_list = ("is_iterable", "is_iterable_2")
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