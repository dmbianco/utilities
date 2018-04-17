import time
import datetime
import os
import sys
from generate_id import id_from_timestamp, hash_object_to_id


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


class Log():

    logging_levels = ("DEBUGGING", "CRITIAL", "PROBLEM")

    def __init__(self, level, name="", subname="", description=""):
        pass


class CriticalError(Exception):
    """Base class for exceptions in this module."""
    pass


class MyLogger():
    '''
    Class for logging purposes.
    The format of the logs is determined by log_format.
    '''

    modes = ("file", "stdout")
    logging_levels = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
    log_format = "{}|{}|{}|{}|{}"

    def __init__(self, log_dir="", log_filepath="", name="", logging_mode="stdout", raise_critical=False):
        self.name = name
        self.timer = MyTimer(id_="logger_" + name)
        assert logging_mode in self.modes
        self.logging_mode = logging_mode
        self.raise_critical = raise_critical
        if log_filepath:
            if os.path.isfile(log_filepath):
                os.remove(log_filepath)
            self.log_file = log_filepath
        elif log_dir:
            if not os.path.isdir(log_dir):
                raise FileNotFoundError
            else:
                log_filepath = "log.txt"
                self.log_file = log_filepath


    def generate_log(self, dt, name="", subname="", level="DEBUG", description=""):
        return self.log_format.format(dt, level, name, subname, description)


    def logit(self, log=""):
        if self.logging_mode == "file":
            with open(self.log_file, "a") as fout:
                fout.write(log + "\n")
                fout.flush()
        elif self.logging_mode == "stdout":
            sys.stdout.write(log + "\n")

        if self.raise_critical and "CRITICAL" in log:
            raise CriticalError


    def start_task(self, task_name="", description=""):
        self.timer.tic()
        self.current_task_name = task_name
        dt = self.pretty_print_ts(self.timer.last_tic)
        log = self.generate_log(dt, name="TASK START", subname=task_name, level="DEBUG", description=description)
        self.logit(log)


    def end_task(self):
        duration = self.timer.toc()
        dt = self.pretty_print_ts(self.timer.last_toc)
        description = "duration {0:0.4f} s".format(duration)
        log = self.generate_log(dt, name="TASK END", subname=self.current_task_name, level="DEBUG", description=description)
        self.logit(log)


    def check_condition(self, condition, condition_name=""):
        dt = self.pretty_print_ts(self.timer.time())
        if condition:
            log = self.generate_log(dt, name="CHECK CONDITION", subname=condition_name, level="INFO",
                                    description=str(condition))
        else:
            log = self.generate_log(dt, name="CHECK CONDITION", subname=condition_name, level="CRITICAL",
                                    description=str(condition))
        self.logit(log)


    def log_message(self, name="", subname="", level="DEBUG", description=""):
        dt = self.pretty_print_ts(self.timer.time())
        log = self.generate_log(dt=dt, name=name, subname=subname, level=level, description=description)
        self.logit(log)


    def __str__(self):
        return "Logger {}".format(self.name)

    def pretty_print_ts(self, ts, format="%Y-%m-%d %H:%M:%S"):
        dt = datetime.datetime.fromtimestamp(ts)
        return datetime.datetime.strftime(dt, format=format)




class Task():

    def __init__(self, id="", description=""):
        if not id:
            id = hash_object_to_id(id_from_timestamp, only_last=5)
        self.id = id
        self.description = description
    
    def __str__(self):
        to_print = "TASK: {}".format(self.id)
        if self.description:
            to_print += "\n{}".format(self.description)
        return to_print
        
        
class Plan():

    def __init__(self, id="", description="", subtasks=[]):
        if not id:
            id = hash_object_to_id(id_from_timestamp, only_last=5)
        self.id = id
        self.description = description
        self.subtasks = subtasks


    def add_subtasks(self, subtasks):
        self.subtasks.extend(subtasks)


    def print_plan(self):
        to_print = self.__str__() + "\n"
        for sub in self.subtasks:
            to_print += sub.__str__() + "\n"
        print(to_print)


    def __str__(self):
        to_print = "PLAN: {}".format(self.id)
        if self.description:
            to_print += "\n{}".format(self.description)
        return to_print




if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description='Test the functionalities of the class')

    function_list = ("plan", "mylogger")
    for x in function_list:
        cmd = '--{}'.format(x)
        help = 'Test {} class.'.format(x)
        parser.add_argument(cmd, help=help, required=False, action='store_true')
    parser.add_argument("--test_all", help="Test all functions",
                        required=False, action='store_true')

    args = parser.parse_args()
    args = vars(parser.parse_args())
    if args["test_all"]:
        for x in args:
            args[x] = True

    if args["mylogger"]:
        logger = MyLogger(name="test", log_dir=".")
        logger.start_task("Test sleep", "2 seconds sleep")
        time.sleep(2)
        logger.end_task()

    
    if args["plan"]:
        subs = []
        for x in range(3):
            sub = Task(id=str(x), description="Subtask {}".format(x))
            subs.append(sub)
        plan = Plan(id="A1", description="Test plan", subtasks=subs)
        plan.print_plan()


