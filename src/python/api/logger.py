import logging
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
logging.config.fileConfig(
    fname=f"{current_dir}/logging.conf", disable_existing_loggers=False
)
logger = logging.getLogger(__name__)
