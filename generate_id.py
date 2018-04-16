import string
import datetime
import time
import itertools


def id_from_datetime(datetime_format="%Y-%m-%d_%H:%M:%S"):
    dt = datetime.datetime.strftime(datetime.datetime.now(), datetime_format)
    return dt


def id_from_timestamp():
    return str(int(time.time()))


def n_characters_run_id(pattern="U2_D1", already_generated_keys=None, sep=""):
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
            print(p)
            assert p[0] in bag_of_chs
            assert p[1:].isdigit()
            assert int(p[1:]) > 0 and int(p[1:]) > 0
            ch = p[0]
            N = int(p[1:])
            bag.extend([bag_of_chs[ch]]*N)
        return bag
    
    bag = parse_pattern(pattern)

    try:
        run_ids = set(already_generated_keys)
    except:
        pass
    finally:
        run_ids = None

    for x in itertools.product(*bag):
        run_id = sep.join(x)
        if run_ids is not None and run_id not in run_ids:
            yield run_id
        else:
            yield run_id



def generate_random_run_id(type="numeric", n=4):
    pass



if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description='Test the functionalities of the class')

    function_list = ("id_from_datetime", "id_from_timestamp", "n_characters_run_id")
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

    if args["n_characters_run_id"]:
        print("TESTING n_characters_run_id")
        print("Base mode U2_D2")
        i = 3
        for id_ in n_characters_run_id(pattern="U2_D2"):
            print(id_)
            i -= 1
            if i <= 0:
                break
        print()

        i = 3
        for id_ in n_characters_run_id(pattern="U2_D2"):
            print(id_)
            i -= 1
            if i <= 0:
                break
        print()

    
