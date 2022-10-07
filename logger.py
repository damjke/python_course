import logging

logger = logging.getLogger('mylogger')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(fmt='%(asctime)s %(levelname)s \t %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.INFO)
