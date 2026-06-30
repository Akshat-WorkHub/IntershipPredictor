import os,sys
import logging
from datetime import datetime as time

LOG_FILE = f"{time.now().strftime('Date-%d-%m-%Y-Time-%H-%M-%S')}.log"

logDir = os.path.join(os.getcwd(),"logs",LOG_FILE[:-4])
os.makedirs(logDir,exist_ok=True)

LOG_FILE_PATH = os.path.join(logDir,LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format="[ %(asctime)s ] File : %(filename)s | LineNo : %(lineno)s | Name : %(name)s | Level-Name : %(levelname)s | Message : %(message)s "
)