# lib/logger.py

import logging
import sys
from colorama import Fore, Style


# Definir colores para diferentes niveles de log
LOG_COLORS = {
    "DEBUG": Fore.CYAN,
    "INFO": Fore.GREEN,
    "WARNING": Fore.YELLOW,
    "ERROR": Fore.RED,
    "CRITICAL": Fore.MAGENTA,
}


class ColoredFormatter(logging.Formatter):
    """
    Formateador de logs con colores.
    """

    def format(self, record):
        log_color = LOG_COLORS.get(record.levelname, Fore.WHITE)
        log_msg = super().format(record)
        return f"{log_color}{log_msg}{Style.RESET_ALL}"


def get_logger(
    name: str, level: str = "INFO", use_colors: bool = True
) -> logging.Logger:
    """
    Crea y configura un logger con formato personalizado y soporte para colores.

    Args:
        name (str): Nombre del logger.
        level (str): Nivel de log (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        use_colors (bool): Si se deben usar colores en la salida.

    Returns:
        logging.Logger: Logger configurado.
    """

    logger = logging.getLogger(name)
    if logger.hasHandlers():
        return logger  # Evita agregar múltiples handlers

    level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(level)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler = logging.StreamHandler(sys.stdout)

    if use_colors:
        handler.setFormatter(ColoredFormatter(formatter._fmt))
    else:
        handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger
