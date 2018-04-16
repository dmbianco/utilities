import string
import datetime
import time
import itertools
import random
from wrappers import yield_func_wrapper


def id_from_datetime(datetime_format="%Y-%m-%d_%H:%M:%S"):
    dt = datetime.datetime.strftime(datetime.datetime.now(), datetime_format)
    return dt


def id_from_timestamp():
    return str(int(time.time()))


def n_characters_ids(pattern="U2_D1", already_generated_ids=None, sep="", random_mode=False):
    '''
    It generates a unique identifier.
    Pattern should be a string with the following pattern:
        xN_yM
    where x (y) should be 'U', 'L' or 'D' and N (M) can be any natural number.
    Each atomic sequence 'xN' should be separeated by an underscore. An assertion error will
    be raised if the previous constraints will not be respected.
    '''
    bag_of_chs = {}
    bag_of_chs["U"] = string.ascii_uppercase
    bag_of_chs["L"] = string.ascii_lowercase
    bag_of_chs["D"] = string.digits

    def parse_pattern(pt):
        pt = pt.split("_")
        assert len(pt) >= 1
        bag = []
        for p in pt:
            assert p[0] in bag_of_chs
            assert p[1:].isdigit()
            assert int(p[1:]) > 0 and int(p[1:]) > 0
            ch = p[0]
            N = int(p[1:])
            if not random_mode:
                bag.extend([bag_of_chs[ch]]*N)
            else:
                l = []
                random.seed(time.time())
                for x in range(N):
                    s = bag_of_chs[ch]
                    l.append(''.join( random.sample(s,len(s)) ))
                bag.extend(l)
        return bag
    
    bag = parse_pattern(pattern)

    try:
        run_ids = set(already_generated_ids)
    except:
        run_ids = None
        
    for x in itertools.product(*bag):
        run_id = sep.join(x)
        if run_ids is not None and run_id not in run_ids:
            yield run_id
        elif run_ids is None:
            yield run_id
        else:
            continue


def generate_random_id(n_ch=4, already_generated_ids=None):
    '''
    n_ch: the number of characters to generate.
    '''
    try:
        run_ids = set(already_generated_ids)
    except:
        run_ids = None

    random.seed(time.time())
    while True:
        chs = string.ascii_uppercase + string.ascii_lowercase + string.digits
        l = [random.choice(chs) for x in range(n_ch)]
        run_id = "".join(l)
        if run_ids is not None and run_id not in run_ids:
            yield run_id
        elif run_ids is None:
            yield run_id
        else:
            continue



if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description='Test the functionalities of the class')

    function_list = ("id_from_datetime", "id_from_timestamp", "n_characters_ids",
                     "generate_random_id")
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

    if args["id_from_datetime"]:
        print("TESTING id_from_datetime")
        print("First id: {}".format(id_from_datetime()))
        time.sleep(2)
        print("Sleeping for 2 seconds.")
        print("Second id: {}".format(id_from_datetime()))
        print()
    
    if args["id_from_timestamp"]:
        print("TESTING id_from_timestamp")
        print("First id: {}".format(id_from_timestamp()))
        time.sleep(2)
        print("Sleeping for 2 seconds.")
        print("Second id: {}".format(id_from_timestamp()))
        print()

    if args["n_characters_ids"]:
        print("TESTING n_characters_ids")
        print("Base mode U2_D2")
        l = yield_func_wrapper(n_characters_ids, pattern="U2_D2")
        print(l)

        print("Base mode U1_D1_L1")
        l = yield_func_wrapper(n_characters_ids, pattern="U1_D1_L1")
        print(l)
    
        print("Already generated ['AA0', 'AA2'] mode U2_D1")
        l = yield_func_wrapper(n_characters_ids, pattern="U2_D1", 
                                already_generated_ids=['AA0', 'AA2'])
        print(l)

        print("Random mode mode U2_D1")
        l = yield_func_wrapper(n_characters_ids, pattern="U2_D1", 
                                already_generated_ids=['AA0', 'AA2'], random_mode=True)
        print(l)

    if args["generate_random_id"]:
        print("TESTING generate_random_id n_ch=5")
        l = yield_func_wrapper(generate_random_id, n_ch=5)
        print(l, "\n")
        print("TESTING generate_random_id n_ch=20")
        l = yield_func_wrapper(generate_random_id, n_ch=20)
        print(l, "\n")

