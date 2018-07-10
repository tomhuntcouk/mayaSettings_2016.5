



import logging

LOGGER = logging.getLogger(__name__)



def crash_method():
    LOGGER.info("About to crash - Via Method")
    myvar = int("String")
    LOGGER.info("Past Crash")

def try_crash_method():
    LOGGER.info("About to crash - Via Method")
    try:
        myvar = int("String")
    except Exception as error:
        LOGGER.error("We had a crash - oh no! : {}".format(error))
    LOGGER.info("Past Crash")


class CrashClass(object):

    def __init__(self):
        self.my_var = None
        pass

    def crash_method(self):
        LOGGER.info("About to crash - Via Method")
        self.my_var = int("String")
        LOGGER.info("Past Crash")

    def try_crash_method(self):
        LOGGER.info("About to crash - Via Method")
        try:
            self.my_var = int("String")
        except Exception as error:
            LOGGER.error("We had a crash - oh no! : {}".format(error))
        LOGGER.info("Past Crash")
