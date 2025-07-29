# errors.py


class FonderError(Exception):
    """Excepción base para todos los errores de Fonder."""

    def __init__(self, message=None):
        super().__init__(message or "FONDER ERROR HAPPENED")
