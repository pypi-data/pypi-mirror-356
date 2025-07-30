import logging
from reffinder.settings import LOG_LEVEL

logging.basicConfig(
    level=LOG_LEVEL,
    format='[%(levelname)s] %(message)s',
    force=True
)
