#!/bin/python2


import time
import sys

from IPython import embed


class Logger():
    def __init__(self, fname, mode, suppress):
        self.logfile = open(fname, mode)
        self.stdout = sys.stdout
        self.suppressed = suppress
        sys.stdout = self


    def write(self, text):
        self.logfile.write(text)
        if not self.suppressed:
            self.stdout.write(text)

    def __del__(self):
        sys.stdout = self.stdout
        self.logfile.close()


class Timer():
    def __init__(self, label="~", verbose=True):
        self.label = label
        self.verbose = verbose

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, *args):
        self.delta = time.time() - self.start
        if self.verbose:
            logtime("---> [%s elapsed %f s]"%(self.label, self.delta))


class CumTimer():
    def __init__(self, ctimer):
        self.ctimer = ctimer

    def __enter__(self):
        self.start = time.time()

    def __exit__(self):
        self.ctimer += time.time() - self.start


def set_file(fname=sys.argv[0].split('.')[0]+"_"+time.strftime('%y%m%d-%H%M%S')+".log", suppress=False):
    sys.stdout = Logger(fname, "w", suppress)


def IPS(loc=None):
    shelltime = time.time()
    try:
        fname = sys.stdout.logfile.name
        suppress = sys.stdout.suppressed

        del(sys.stdout)
        embed(user_ns=loc)
        sys.stdout = Logger(fname, "a", suppress)
    except:
        embed(user_ns=loc)
    info("Embedded IPython shell")
    logtime("---> [%s elapsed %f s]"%("IPS",time.time()-shelltime))


def msg(label, text):
    #sys.stdout.write(time.strftime('%d-%m-%Y_%H:%M:%S')+"\t"+label+"\t"+text+"\n")
    sys.stdout.write(label+"\t"+text+"\n")

def info(text):
    msg("INFO:", text)

def logtime(text):
    msg("TIME:", text)

def warn(text):
    msg("WARN:", text)

def err(text):
    msg("ERROR:", text)


if __name__ == "__main__":
    import log

    log.set_file()

    with log.Timer("testing"):
        log.info("Information")
        log.warn("Warning")
        log.err("Error")

    log.IPS()
    log.info("succeeded")

