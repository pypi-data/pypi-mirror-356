import logging
import argparse
import threading
import multiprocessing as mp
from kLogger import kLogger


def basic_test(log):
    #test default usage
    log.debug("debug message")
    log.info("info message")
    log.warning("warning message")
    log.error("error message")
    log.critical("critical message")

    #test calls
    log()
    x = 10
    log(x)

def test(logfile, loglevel):
    #test creation
    log = kLogger("klogs", logfile, loglevel)
    basic_test(log)

def test_threads(logfile, loglevel):
    log = kLogger("klogs", logfile, loglevel)
    
    def thread():
        basic_test(log)

    info_string = "######## In thread ########"
    if logfile:
        with open(logfile, "a") as fd:
            fd.write(info_string)
            fd.write("\n")
    else:
        print(info_string)
    t = threading.Thread(target=thread)
    t.start()
    t.join()
    info_string = "######## Outside thread ########"
    if logfile:
        with open(logfile, "a") as fd:
            fd.write(info_string)
            fd.write("\n")
    else:
        print(info_string)
    basic_test(log)


def process(logfile, loglevel):
    log = kLogger("klogs", logfile, loglevel)
    log.debug("debug message")
    log.info("info message")
    log.warning("warning message")
    log.error("error message")
    log.critical("critical message")

    #test calls
    log()
    x = 10
    log(x)

def test_process(logfile, loglevel):
    log = kLogger("klogs", logfile, loglevel)
    info_string = "######## In process ########"
    if logfile:
        with open(logfile, "a") as fd:
            fd.write(info_string)
            fd.write("\n")
    else:
        print(info_string)
    p = mp.Process(target=process, args=(logfile, loglevel,))
    p.start()
    p.join()
    info_string = "######## Outside process ########"
    if logfile:
        with open(logfile, "a") as fd:
            fd.write(info_string)
            fd.write("\n")
    else:
        print(info_string)
    basic_test(log)

def test_multifile(logfile, loglevel):
    if not logfile:
        logfile = "log"
    log = kLogger("klogs-multifile", logfile, loglevel)
    log.addFile(logfile+"2")
    log.addFile(logfile+"3")
    log.addFile(logfile+"4")
    basic_test(log)

if __name__ == "__main__":
    #argparsing 
    argparser = argparse.ArgumentParser(description='Klogs')
    argparser.add_argument('-f', '--file', help='Log file')
    argparser.add_argument('-l', '--level', help='Log level')
    args = argparser.parse_args()
    info_string = "######## Testing normal usage ########"
    if args.file:
        with open(args.file, "w") as fd:
            fd.write(info_string)
            fd.write("\n")
    else:
        print(info_string)
    test(args.file, args.level)
    info_string = "######## Testing threaded usage ########"
    if args.file:
        with open(args.file, "a") as fd:
            fd.write(info_string)
            fd.write("\n")
    else:
        print(info_string)
    test_threads(args.file, args.level)
    info_string = "######## Testing process usage ########"
    if args.file:
        with open(args.file, "a") as fd:
            fd.write(info_string)
            fd.write("\n")
    else:
        print(info_string)
    test_process(args.file, args.level)
    #This multifile test is kind of dumb / not useful
    # info_string = "######## Testing multi file ########"
    # if args.file:
    #     with open(args.file, "a") as fd:
    #         fd.write(info_string)
    #         fd.write("\n")
    # else:
    #     print(info_string)
    # test_multifile(args.file, args.level)

