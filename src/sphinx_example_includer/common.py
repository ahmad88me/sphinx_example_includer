import logging


def get_logger(name=None):
    if name:
        logger = logging.getLogger(name)
    else:
        logger = logging.getLogger(__name__)
    logger.setLevel(logging.WARN)
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARN)
    logger.addHandler(ch)
    return logger