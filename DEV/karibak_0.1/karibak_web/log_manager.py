import logging


def logging_init():
   #Below are the 4 log types we use. DEBUG, INFO, ERROR and WARNING
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    debug_handler = logging.FileHandler("logs/debug_log.log")
    debug_handler.setLevel(logging.DEBUG)

    info_handler=logging.FileHandler("logs/info_log.log")
    info_handler.setLevel(logging.INFO)

    error_handler=logging.FileHandler("logs/error_log.log")
    error_handler.setLevel(logging.ERROR)

    warning_handler=logging.FileHandler("logs/warning_log.log")
    warning_handler.setLevel(logging.WARNING)


    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    debug_handler.setFormatter(formatter)
    info_handler.setFormatter(formatter)
    error_handler.setFormatter(formatter)
    warning_handler.setFormatter(formatter)


    logger.addHandler(debug_handler)
    logger.addHandler(info_handler)
    logger.addHandler(error_handler)
    logger.addHandler(warning_handler)

def log_func(e, msg, type):
    logger = logging.getLogger()
    print(msg)
    try:
        if type == "debug":
            logger.debug(msg)
        elif type == "info":
            logger.info(msg)
        elif type == "error":
            logger.warning(msg)
        elif type == "warning":
            logger.error(msg)
        if e == "":
            return
        else:
            print("printing error")
            logger.error(e)
            print(e)
    except Exception as e:
        logger.error("Logging failed")
        print(e)

logging_init()
