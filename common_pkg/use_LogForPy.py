import logging
from LogForPy.emb_log import config_logging

config_logging('./log/test.log', is_console_output=False)
#config_logging('./log/test.log')

if __name__ == '__main__':
    logging.error('error occur.')
    logging.info("infomation")
    logging.debug("debug pro.")
