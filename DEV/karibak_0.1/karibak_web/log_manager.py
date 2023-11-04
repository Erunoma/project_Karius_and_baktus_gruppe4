import logging
def logging_init():
    logging.basicConfig(filename="logs/debug_log.log", level=logging.DEBUG)
    logging.basicConfig(filename="logs/info_log.log", level=logging.INFO)
    logging.basicConfig(filename="logs/warning_log.log", level=logging.WARNING)
    logging.basicConfig(filename="logs/error_log.log", level=logging.ERROR)




logging_init()