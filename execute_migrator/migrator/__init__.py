import logging

logging.disable(logging.CRITICAL)

from .str import migrate_execute
from .level import migrate_level, migrate_level_zip
from .mcfunction import migrate_mcfunction, migrate_mcfunctions

logging.disable(logging.NOTSET)
