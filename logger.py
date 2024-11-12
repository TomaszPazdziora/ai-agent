import os
import logging
from datetime import datetime

current_file_location = os.path.dirname(os.path.abspath(__file__))
log_directory = current_file_location + os.sep + 'logs'


if not os.path.exists(log_directory):
    os.makedirs(log_directory)

log_filename = datetime.now().strftime('%Y-%m-%d-%H-%M-%S.log')
log_filepath = os.path.join(log_directory, log_filename)

file_handler = logging.FileHandler(log_filepath)
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)


def setup_logger(logger: logging.Logger) -> None:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
