import logging

def get_logger() -> logging.Logger:
    logger = logging.getLogger("Scanner")

    if not logger.hasHandlers():
        # initialize
        output = logging.StreamHandler()
        output.setLevel(logging.INFO)
        output.setFormatter(logging.Formatter("[%(asctime)s] %(message)s"))
        logger.addHandler(output)
    
    return logger