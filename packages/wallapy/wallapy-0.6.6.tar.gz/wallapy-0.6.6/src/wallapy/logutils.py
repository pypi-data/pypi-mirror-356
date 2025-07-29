import logging
from typing import Literal


logger = logging.getLogger("wallapy")  # Use a specific logger name for the library
logger.addHandler(logging.NullHandler())

Verbosity = Literal[0, 1, 2]
_LEVEL_MAP = {0: logging.WARNING, 1: logging.INFO, 2: logging.DEBUG}


def _has_real_handler(log: logging.Logger) -> bool:
    """
    Ritorna True se 'log' o un suo antenato ha almeno un handler
    che NON sia NullHandler.
    """
    current = log
    while current:
        if any(not isinstance(h, logging.NullHandler) for h in current.handlers):
            return True
        if not current.propagate:
            break
        current = current.parent
    return False


def set_verbosity(verbose: Verbosity = 0) -> None:
    """
    Imposta il livello di logging della libreria e, se necessario,
    aggiunge un handler di default.
    """

    if verbose > 2:
        verbose = 2  # Limit to maximum verbosity level
    elif verbose < 0:
        verbose = 0

    logger.setLevel(_LEVEL_MAP.get(verbose, logging.WARNING))

    # Aggiungiamo il nostro StreamHandler **solo** se non esiste
    # già un handler “reale” (cioè != NullHandler) da nessuna parte.
    if not _has_real_handler(logger):
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                datefmt="%H:%M:%S",
            )
        )
        logger.addHandler(handler)
