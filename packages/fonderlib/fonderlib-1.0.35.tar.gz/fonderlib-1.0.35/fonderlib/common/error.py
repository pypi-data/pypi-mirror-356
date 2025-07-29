from .fonder_error import FonderError


class ConfigError(FonderError):
    """Error relacionado con la configuración del entorno o variables faltantes."""

    def __init__(self, message=None):
        super().__init__(message or "Error en la configuración.")


class AuthError(FonderError):
    """Error relacionado con autenticación o autorización."""

    def __init__(self, message=None):
        super().__init__(message or "Error de autenticación/autorización.")


class DatabaseError(FonderError):
    """Error relacionado con la base de datos."""

    def __init__(self, message=None):
        super().__init__(message or "Error de base de datos.")


class NotFoundError(FonderError):
    """Error cuando no se encuentra un recurso."""

    def __init__(self, message=None):
        super().__init__(message or "Recurso no encontrado.")


class ValidationError(FonderError):
    """Error de validación de datos."""

    def __init__(self, message=None):
        super().__init__(message or "Error de validación.")


class ExternalServiceError(FonderError):
    """Error al interactuar con un servicio externo (API, third-party, etc)."""

    def __init__(self, message=None):
        super().__init__(message or "Error al comunicarse con un servicio externo.")


class IntegrationError(FonderError):
    def __init__(self, integ: str, message=None):
        super().__init__(f"{integ} ERROR" + message or "en la integracion.")
