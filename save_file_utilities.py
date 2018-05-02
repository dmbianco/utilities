import os
import sys
import datetime
import re


class FileManager():

    def __init__(self):
        pass


    def mkdir(self, path):
        try:
            os.mkdir(path)
        except FileExistsError:
            pass


    @staticmethod
    def get_current_timestamp(datetime_format="%Y-%m-%d_%H:%M:%S"):
        return datetime.datetime.strftime(datetime.datetime.now(), datetime_format)


    @staticmethod
    def list_files(dir):
        if os.path.isdir(dir):
            return [f for f in os.listdir(dir)]
        else:
            return []

    @staticmethod
    def clean_dir(dir, logging=None):
        '''
        It deletes all the files into the directory dir.
        '''
        error_occurred = False
        for filename in os.listdir(dir):
            file_path = os.path.join(dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                err_msg = "Cannot remove " + file_path + ". MESSAGE: " + str(e)
                error_occurred = True
                if logging:
                    logging.error(err_msg)
                else:
                    print(err_msg)
        if error_occurred:
            return False
        else:
            return True



class FilenamesWithId():
    '''
    The filename format is
    base_filename**sep**key.ext
    '''

    sep = "__"

    def __init__(self, dir, base_filename, extension):
        if not os.path.isdir(dir):
            raise AssertionError # <--- CHECK THIS!!!
        self.base_dir = dir
        self.base_filename = base_filename
        self.extension = extension
        self._get_keys()
        

    def list_files(self, only_id_files=True):
        filenames = os.listdir(self.base_dir)
        if only_id_files:
            filenames = [f for f in filenames if self.sep in f]
        return filenames


    def get_already_generated_keys(self):
        self._get_keys()
        return list(self.old_keys)


    def _get_keys(self):
        filenames = [f for f in os.listdir(self.base_dir) if self.sep in f]
        keys = map(lambda x: x.split(self.sep)[1], filenames)
        keys = list(map(lambda x: x.replace("." + self.extension, ""), keys))
        self.old_keys = set(keys)
        assert len(self.old_keys) == len(keys)


    def key_exists(self, key):
        self._get_keys()
        if key in self.old_keys:
            return True
        else:
            return False



def get_completed_files(completed_file_path):
    completed_files = []
    if os.path.isfile(completed_file_path):
        with open(completed_file_path, "rb") as fin:
            for row in fin:
                file_path = row.strip()
                completed_files.append(file_path)
    return completed_files


def get_all_days_between(d1, d2, date_format="%Y-%m-%d %H:%M:%s"):
    '''
    It returns all the days between d1 and d2.
    date_format is the format of the aforementioned dates.
    '''
    def parse_date(d):
        new_d = datetime.datetime.strptime(d, date_format)
        return new_d

    d1 = parse_date(d1)
    d2 = parse_date(d2)
    delta = d2 - d1
    dates = []
    for i in range(delta.days + 1):
        dates.append(d1 + timedelta(days=i))

    return dates


def load_night_macs(filepath):
    night_macs = {}
    if not os.path.isfile(filepath):
        return night_macs
    with open(filepath, "rb") as fin:
        for l in fin:
            mac, day = l.strip().split("\t")
            if day not in night_macs:
                night_macs[day] = set()
            night_macs[day].add(mac)
    return night_macs


def extract_date_from_filename(filename, join_char="-"):
    '''
    It extracts the date from a filename with the following pattern:
        xxx_YYYY_MM_DD.yyy
    '''
    filename = filename.split("_")[-3:]
    filename[-1] = filename[-1].split(".")[0]
    return join_char.join(filename)


def get_files_to_process(input_dir, output_dir=None, completed_file_path=None,
                         dates=None):
    input_files = list_files(input_dir)

    if isinstance(dates,set) or isinstance(dates,list):
        for f in input_files[:]:
            if extract_date_from_filename(f) not in dates:
                input_files.pop(input_files.index(f))

    if output_dir is not None:
        completed_files = list_files(output_dir)
    elif completed_file_path is not None:
        completed_files = get_completed_files(completed_file_path)
    else:
        completed_files = []

    res_files = set(input_files) - set(completed_files)
    return sorted(list(res_files))


def get_all_dates(dates_dict, dir=None, return_one_list=False):
    train_start_date = dates_dict["train_start_date"]
    train_end_date = dates_dict["train_end_date"]
    validation_start_date = dates_dict["validation_start_date"]
    validation_end_date = dates_dict["validation_end_date"]
    test_start_date = dates_dict["test_start_date"]
    test_end_date = dates_dict["test_end_date"]

    train_dates = get_list_of_dates(train_start_date, train_end_date, dir=dir)
    validation_dates = get_list_of_dates(validation_start_date, validation_end_date, dir=dir)
    test_dates = get_list_of_dates(test_start_date, test_end_date, dir=dir)

    if return_one_list:
        train_dates.extend(validation_dates)
        train_dates.extend(test_dates)
        return sorted(list(set(train_dates)))
    else:
        return train_dates, validation_dates, test_dates


def get_list_of_dates(start_date, end_date, dir=None):
    '''
    It returns a list of dates (str) between start_date and end_date.
    If dir is provided, it checks whether the corresponding files are available
    to be processed.
    '''
    dates = get_all_days_between(start_date, end_date)
    dates = map(lambda x: datetime.datetime.strftime(x, DATE_FORMAT), dates)
    if dir is not None:
        filenames = [ f for f in os.listdir(dir) ]
        if os.path.isdir(dir):
            filenames = [ f for f in os.listdir(dir) ]
            old_dates = dates[:]
            dates = []
            for filename in sorted(filenames):
                date = extract_date_from_filename(filename, join_char="-")
                if date in old_dates:
                    dates.append(date)
    return dates



if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description='Test the functionalities of the class')

    function_list = ("FilenamesWithId", )
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

    if args["FilenamesWithId"]:
        print("TESTING FilenamesWithId")
        test_dir = "./TEST/"
        base_filename = "test"
        keys = list(map(lambda x: str(x), range(10)))
        extension = "txt"
        sep = "__"
        print("Creating a directory {}".format(test_dir))
        print("Base filename: {}".format(base_filename))
        print("Extension: {}".format(extension))
        print("Keys: {}".format(keys))
        if not os.path.isdir(test_dir):
            os.mkdir(test_dir)
            for k in keys:
                filename = base_filename + sep + k + "." + extension
                open(test_dir + filename, "w+")
        file_manager = FilenamesWithId(test_dir, base_filename, extension)
        new_keys = list(map(lambda x: str(x), range(5,15)))
        print("New keys: {}".format(new_keys))
        old_keys = file_manager.get_already_generated_keys()
        print("Old keys: {}".format(old_keys))
        for k in new_keys:
            exist = file_manager.key_exists(k)
            exist = "" if exist else "DOES NOT"
            print("Key {} {} exist".format(k, exist))
