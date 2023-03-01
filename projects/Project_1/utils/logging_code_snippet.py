import logging
from os import path, makedirs
from datetime import datetime
from pathlib import Path
import re

# LOG LEVELS
# DEBUG		Detailed information, useful during bugfixing
# INFO		Just enough information to be able to understand the flow
# WARNING	Information about unexpected conditions that might be solved later
# ERROR		Reporting that the program can perform some task
# CRITICAL	Reporting that the program can not continue

loggingPath = path.join(Path.cwd(), "logs")

if not path.exists(loggingPath):
    makedirs(loggingPath)

now, n = re.subn("[/,:]", "", datetime.today().strftime("%Y%m%d_%X"))
loggingFile = path.join(loggingPath, f"{now}.log")

logging.basicConfig(filename=loggingFile, level=logging.INFO)
logging.info("Logging to file..")
