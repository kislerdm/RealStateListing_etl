import os

from config import parser
import logging

logger = logging.getLogger(__name__)

def stop():
    """
    function to create a dummy file stop.dat which will shutdown the main process
    :return:
    """

    conf = parser.config_parser()
    file = "stop.dat"
    stop_file = os.path.join(conf['Input-file']['filepath'], file)
    with open(stop_file,'w') as sf:
        sf.write("Shutting down the process.")
        logger.info("Shutting down the process.")


if __name__ == "__main__":
    stop()
