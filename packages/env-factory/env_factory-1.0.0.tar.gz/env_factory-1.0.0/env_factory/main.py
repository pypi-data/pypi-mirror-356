from abc import ABC, abstractmethod
from env_factory.exceptions import ConfigurationError, SecretRetrievalError, EnvFactoryError
import logging
from typing import Dict, Optional, Union, Any, List
from sm_env_read import get_env_secrets_from_sm
import os

logger = logging.getLogger(__name__)


# Env interface
class EnvRetrieval(ABC):
    """Abstract base class for environment variable retrieval"""

    @abstractmethod
    def get_env_variables(self, keys: List[str]) -> Dict[str, Optional[str]]:
        """
    Retrieve environment variables for the given keys

    Args:
        keys: List of environment variable names to retrieve

    Returns:
        Dictionary mapping keys to their values (or None if not found)

    Raises:
        EnvFactoryError: If retrieval fails
    """
        pass


class LocalEnvRetrieval(EnvRetrieval):
    """Retrieves environment variables from local system environment"""

    def get_env_variables(self, keys: List[str]) -> Dict[str, Optional[str]]:
        """
    Retrieve environment variables from local system

    Args:
        keys: List of environment variable names to retrieve

    Returns:
        Dictionary mapping keys to their values (or None if not found)

    Raises:
        ConfigurationError: If keys parameter is invalid
    """
        if not keys:
            raise ConfigurationError("Keys list cannot be empty")

        if not isinstance(keys, list):
            raise ConfigurationError("Keys must be a list of strings")

        if not all(isinstance(key, str) for key in keys):
            raise ConfigurationError("All keys must be strings")

        env_list: Dict[str, Optional[str]] = {}

        try:
            for key in keys:
                if not key.strip():
                    logger.warning(f"Empty or whitespace-only key found: '{key}'")
                    env_list[key] = None
                    continue

                value: Optional[str] = os.getenv(key, None)
                env_list[key] = value

                if value is None:
                    logger.debug(f"Environment variable '{key}' not found")

        except Exception as e:
            logger.error(f"Error retrieving local environment variables: {e}")
            raise EnvFactoryError(f"Failed to retrieve local environment variables: {e}")

        return env_list


class AWSEnvRetrieval(EnvRetrieval):
    """Retrieves environment variables from AWS Secrets Manager"""

    def __init__(self, secret_name: str, region: str, role_name: str):
        """
    Initialize AWS environment retrieval

    Args:
        secret_name: Name of the secret in AWS Secrets Manager
        region: AWS region
        role_name: IAM role name for accessing secrets

    Raises:
        ConfigurationError: If any parameter is invalid
    """
        if not secret_name or not secret_name.strip():
            raise ConfigurationError("Secret name cannot be empty")
        if not region or not region.strip():
            raise ConfigurationError("Region cannot be empty")
        if not role_name or not role_name.strip():
            raise ConfigurationError("Role name cannot be empty")

        self.secret_name = secret_name.strip()
        self.region = region.strip()
        self.role_name = role_name.strip()

    def get_env_variables(self, keys: List[str]) -> Dict[str, Optional[str]]:
        """
    Retrieve environment variables from AWS Secrets Manager

    Args:
        keys: List of environment variable names to retrieve

    Returns:
        Dictionary mapping keys to their values (or None if not found)

    Raises:
        ConfigurationError: If keys parameter is invalid
        SecretRetrievalError: If AWS secret retrieval fails
    """
        if not keys:
            raise ConfigurationError("Keys list cannot be empty")

        if not isinstance(keys, list):
            raise ConfigurationError("Keys must be a list of strings")

        if not all(isinstance(key, str) for key in keys):
            raise ConfigurationError("All keys must be strings")

        env_list: Dict[str, Optional[str]] = {}

        try:
            # Get AWS account ID from environment
            account_id: Optional[str] = os.getenv("AWS_ACCOUNT_ID", None)
            if not account_id:
                raise ConfigurationError("AWS_ACCOUNT_ID environment variable is required")

            # Retrieve secrets from AWS Secrets Manager
            secrets = get_env_secrets_from_sm(
                account_id=account_id,
                secret_name=self.secret_name,
                role_name=self.role_name,
                region=self.region,
            )

            if secrets is None:
                raise SecretRetrievalError("No secrets returned from AWS Secrets Manager")

            # Handle different secret formats
            if isinstance(secrets, dict):
                # If secrets is already a dictionary
                secrets_dict = secrets
            elif isinstance(secrets, list):
                # If secrets is a list of dictionaries, merge them
                secrets_dict = {}
                for secret_item in secrets:
                    if isinstance(secret_item, dict):
                        secrets_dict.update(secret_item)
                    else:
                        logger.warning(f"Unexpected secret format in list: {type(secret_item)}")
            else:
                raise SecretRetrievalError(f"Unexpected secrets format: {type(secrets)}")

            # Extract requested keys from secrets
            for key in keys:
                if not key.strip():
                    logger.warning(f"Empty or whitespace-only key found: '{key}'")
                    env_list[key] = None
                    continue

                # Look for exact key match
                if key in secrets_dict:
                    env_list[key] = secrets_dict[key]
                else:
                    # Try case-insensitive match as fallback
                    found = False
                    for secret_key, secret_value in secrets_dict.items():
                        if secret_key.lower() == key.lower():
                            env_list[key] = secret_value
                            found = True
                            logger.debug(f"Found case-insensitive match for '{key}': '{secret_key}'")
                            break

                    if not found:
                        env_list[key] = None
                        logger.debug(f"Key '{key}' not found in AWS secrets")

        except ConfigurationError:
            # Re-raise configuration errors as-is
            raise
        except SecretRetrievalError:
            # Re-raise secret retrieval errors as-is
            raise
        except Exception as e:
            logger.error(f"Unexpected error retrieving AWS secrets: {e}")
            raise SecretRetrievalError(f"Failed to retrieve secrets from AWS: {e}")

        return env_list


class EnvFactory:
    """Factory class for creating environment retrieval instances"""

    @staticmethod
    def create_local_retriever() -> LocalEnvRetrieval:
        """Create a local environment retriever"""
        return LocalEnvRetrieval()

    @staticmethod
    def create_aws_retriever(secret_name: str, region: str, role_name: str) -> AWSEnvRetrieval:
        """
    Create an AWS Secrets Manager environment retriever

    Args:
        secret_name: Name of the secret in AWS Secrets Manager
        region: AWS region
        role_name: IAM role name for accessing secrets

    Returns:
        AWSEnvRetrieval instance

    Raises:
        ConfigurationError: If any parameter is invalid
    """
        return AWSEnvRetrieval(secret_name, region, role_name)


# Convenience function for easy usage
def get_env_variables(keys: List[str],
                      source: str = "local",
                      **kwargs) -> Dict[str, Optional[str]]:
    """
  Convenience function to retrieve environment variables

  Args:
      keys: List of environment variable names to retrieve
      source: Environment source ('local' or 'aws')
      **kwargs: Additional arguments for AWS (secret_name, region, role_name)

  Returns:
      Dictionary mapping keys to their values (or None if not found)

  Raises:
      ConfigurationError: If configuration is invalid
      EnvFactoryError: If retrieval fails
  """
    if source.lower() == "local":
        retriever = EnvFactory.create_local_retriever()
    elif source.lower() == "aws":
        required_aws_params = ['secret_name', 'region', 'role_name']
        missing_params = [param for param in required_aws_params if param not in kwargs]

        if missing_params:
            raise ConfigurationError(f"Missing required AWS parameters: {missing_params}")

        retriever = EnvFactory.create_aws_retriever(
            secret_name=kwargs['secret_name'],
            region=kwargs['region'],
            role_name=kwargs['role_name']
        )
    else:
        raise ConfigurationError(f"Unsupported source: {source}. Use 'local' or 'aws'")

    return retriever.get_env_variables(keys)