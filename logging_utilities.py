import timeit
import datetime
import os


def pretty_print_ts(ts, format="%Y-%m-%d %H:%M:%S"):
    dt = datetime.datetime.fromtimestamp(ts)
    return datetime.datetime.strftime(dt, format=format)


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
    
    def __init__(self, log_dir="", log_filepath="", name=""):
        self.name = name
        self.timer = MyTimer(id_="logger_" + name)
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


    def logit(self, message=""):
        with open(self.log_file, "a") as fout:
            fout.write(message + "\n")
            fout.flush()


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

