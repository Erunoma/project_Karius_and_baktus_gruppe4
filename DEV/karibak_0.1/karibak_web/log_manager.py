import logging


def logging_init():
   
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



"""
def create_entry(msg, log_type):
    try:
        if log_type==0:
            logging.debug(f"<{date.today()}> <{time.strftime('%H:%M:%S',time.localtime())}> {msg}")
            print("Entry created under debug.")
        elif log_type==1:
            logging.info(f"<{date.today()}> <{time.strftime('%H:%M:%S',time.localtime())}> {msg}") 
            print("Entry created under info.") 
        elif log_type==2:
            logging.warning(f"<{date.today()}> <{time.strftime('%H:%M:%S',time.localtime())}> {msg}")
            print("Entry created under warning.")
        elif log_type==3:
            logging.error(f"<{date.today()}> <{time.strftime('%H:%M:%S',time.localtime())}> {msg}")
            print("Entry created under error.")
    except:
        print("CRITICAL ERROR: Could not create log entry.")
"""
logging_init()
