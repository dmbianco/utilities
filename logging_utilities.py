import time
import datetime
import os
import sys


def pretty_print_ts(ts, format="%Y-%m-%d %H:%M:%S"):
    dt = datetime.datetime.fromtimestamp(ts)
    return datetime.datetime.strftime(dt, format=format)


def get_current_timestamp(datetime_format="%Y-%m-%d_%H:%M:%S"):
    return datetime.datetime.strftime(datetime.datetime.now(), datetime_format)


class MyTimer():

    def __init__(self, id_=""):
        self.time = time.time
        self.id = id_
        self.last_tic = self.time()
        self.last_toc = self.time()
        self.start_time = self.time()

    def print_time(self):
        print(self.time())

    def tic(self):
        self.last_tic = self.time()

    def toc(self):
        self.last_toc = self.time()
        return self.last_toc - self.last_tic

    def time_from_start(self):
        return self.time() - self.start_time

    def yield_time(self):
        while True:
            yield self.time() - self.last_tic


class MyLogger():

    modes = ("file", "stdout", "get_log")
    
    def __init__(self, log_dir="", log_filepath="", name="", logging_mode="stdout"):
        self.name = name
        self.timer = MyTimer(id_="logger_" + name)
        assert logging_mode in self.modes
        self.logging_mode = logging_mode
        if log_filepath:
            if os.path.isfile(log_filepath):
                os.remove(log_filepath)
            self.log_file = log_filepath
        elif log_dir:
            if not os.path.isdir(log_dir):
                raise FileNotFoundError
            else:
                log_filepath = self.get_log_filename()
                self.log_file = log_filepath


    def logit(self, log=""):
        if self.logging_mode == "file":
            with open(self.log_file, "a") as fout:
                fout.write(log + "\n")
                fout.flush()
        elif self.logging_mode == "stdout":
            sys.stdout.write(log + "\n")
        elif self.logging_mode == "get_log":
            return log


    def start_task(self, name="", description=""):
        self.timer.tic()
        self.current_task_name = name
        dt = pretty_print_ts(self.timer.last_tic)
        self.logit("{}|TASK START|{}|{}".format(dt, name, description))


    def end_task(self):
        duration = self.timer.toc()
        dt = pretty_print_ts(self.timer.last_toc)
        self.logit("{0:}|TASK END|{1:}|duration {2:0.4f} s".format(dt, self.current_task_name, duration))


    def __str__(self):
        return "Logger {}".format(self.name)


    def get_log_filename(self):
        return "log.txt"



if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description='Test the functionalities of the class')

    parser.add_argument('--mylogger', help='Test MyLogger class.', required=False,
                        action='store_false')

    args = parser.parse_args()
    test_mylogger = args.mylogger

    if test_mylogger:
        logger = MyLogger(name="test", log_dir=".")
        logger.start_task("Test sleep", "2 seconds sleep")
        time.sleep(2)
        logger.end_task()



