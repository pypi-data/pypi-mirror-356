class EnvFactoryError(Exception):
    """Base exception for env_factory package"""
    pass


class SecretRetrievalError(EnvFactoryError):
    """Exception raised when secret retrieval fails"""
    pass


class ConfigurationError(EnvFactoryError):
    """Exception raised when configuration is invalid"""
    pass