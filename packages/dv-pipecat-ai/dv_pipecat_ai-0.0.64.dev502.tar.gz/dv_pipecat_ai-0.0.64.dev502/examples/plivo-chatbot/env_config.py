import os
import sys
from typing import Optional

from dotenv import load_dotenv
from loguru import logger  # Import logger
from pydantic_settings import BaseSettings


# Function to read secrets from mounted files
def read_secret(secret_name: str, default: Optional[str] = None) -> Optional[str]:
    secret_path = f"/etc/secrets/{secret_name}"
    try:
        with open(secret_path, "r") as file:
            value = file.read().strip()
            # Return None or default if the file is unexpectedly empty
            return value if value else default
    except FileNotFoundError:
        logger.debug(f"Secret file not found at {secret_path}, using default or None.")
        return default
    except IOError as e:
        logger.error(f"Error reading secret file {secret_path}: {e}")
        return default


# Determine the primary .env file path (local dev vs testing)
if "pytest" in sys.modules:
    _ENV_FILE = "env.TEST"
else:
    _ENV_FILE = ".env"

# Check if running in Kubernetes by looking for the secrets mount path
# and read secrets into environment variables if present.
SECRETS_DIR = "/etc/secrets"
if os.path.isdir(SECRETS_DIR):
    logger.info(f"Secrets directory {SECRETS_DIR} found. Reading secrets into environment.")
    # Define the list of secrets expected to be mounted as files
    secrets_to_read = [
        "OPENAI_API_KEY",
        "EXOTEL_SID",
        "EXOTEL_API_KEY",
        "EXOTEL_API_TOKEN",
        "EXOTEL_REGION",
        "APP_ID",
        "DEEPGRAM_API_KEY",
        "ELEVENLABS_API_KEY",
        "ELEVENLABS_VOICE_ID",
        "AZURE_SPEECH_API_KEY",
        "AZURE_SPEECH_REGION",
        "AZURE_CHATGPT_API_KEY",
        "AZURE_CHATGPT_ENDPOINT",
        "NGROK_URL",
        "PLIVO_AUTH_ID",
        "PLIVO_AUTH_TOKEN",
        "CARTESIA_API_KEY",
        "AWS_ACCESS_KEY_ID",
        "AWS_REGION",
        "AWS_SECRET_ACCESS_KEY",
        "S3_BUCKET_NAME",
        "ENVIRONMENT",
        "REDIS_URL",
        "GLADIA_API_KEY",
        "GROQ_API_KEY",
        "GEMINI_API_KEY",
        "WEAVIATE_CLUSTER_URI",
        "WEAVIATE_CLUSTER_API_KEY",
        "WEAVIATE_COLLECTION_NAME",
        "CALLING_BACKEND_URL",
        "LIVEKIT_URL",
        "LIVEKIT_API_KEY",
        "LIVEKIT_API_SECRET",
        "CALLING_BACKEND_API_KEY",
        "X_API_KEY",
        "WEAVIATE_HOST",
        "TWILIO_ACCOUNT_SID",
        "TWILIO_AUTH_TOKEN",
    ]
    loaded_secrets_count = 0
    for secret_name in secrets_to_read:
        secret_value = read_secret(secret_name)
        if secret_value:
            os.environ[secret_name] = secret_value
            loaded_secrets_count += 1
            logger.debug(f"Loaded secret '{secret_name}' into environment.")
        else:
            logger.warning(f"Secret '{secret_name}' not found in {SECRETS_DIR} or file is empty.")
    logger.info(f"Finished loading {loaded_secrets_count} secrets from {SECRETS_DIR}.")
else:
    logger.info(f"Secrets directory {SECRETS_DIR} not found. Assuming local development.")
    logger.info(f"Loading environment variables from local file: {_ENV_FILE}")
    load_dotenv(dotenv_path=_ENV_FILE, override=True)  # Load .env file if secrets dir doesn't exist


# Pydantic settings will now load from environment variables
# (set either by mounted secrets or local .env file)
class Config(BaseSettings):
    OPENAI_API_KEY: str = "openai_api_key"
    EXOTEL_SID: str = "exotel_sid"
    EXOTEL_API_KEY: str = "exotel_api_key"
    EXOTEL_API_TOKEN: str = "exotel_api_token"
    EXOTEL_REGION: str = "exotel_region"
    APP_ID: str = "app_id"
    DEEPGRAM_API_KEY: str = "deepgram_api_key"
    ELEVENLABS_API_KEY: str = "elevenlabs_api_key"
    ELEVENLABS_VOICE_ID: str = "elevenlabs_voice_id"
    AZURE_SPEECH_API_KEY: str = "azure_speech_api_key"
    AZURE_SPEECH_REGION: str = "azure_speech_region"
    AZURE_CHATGPT_API_KEY: str = "azure_chatgpt_api_key"
    AZURE_CHATGPT_ENDPOINT: str = "azure_chatgpt_endpoint"
    NGROK_URL: str = "ngrok_url"
    PLIVO_AUTH_ID: str = "plivo_auth_id"
    PLIVO_AUTH_TOKEN: str = "plivo_auth_token"
    CARTESIA_API_KEY: str = "cartesia_api_key"
    AWS_ACCESS_KEY_ID: str = "aws_access_key_id"
    AWS_REGION: str = "us-east-1"  # Keep default if desired
    AWS_SECRET_ACCESS_KEY: str = "aws_secret_access_key"
    S3_BUCKET_NAME: str = "s3_bucket_name"
    ENVIRONMENT: str = "development"  # Default environment
    REDIS_URL: str = "redis_url"
    GLADIA_API_KEY: str = "gladia_api_key"
    GROQ_API_KEY: str = "groq_api_key"
    GEMINI_API_KEY: str = "gemini_api_key"
    WEAVIATE_CLUSTER_URI: str = "weaviate_cluster_uri"
    WEAVIATE_CLUSTER_API_KEY: str = "weaviate_cluster_api_key"
    WEAVIATE_COLLECTION_NAME: str = "weaviate_collection_name"
    CALLING_BACKEND_URL: str = "calling_backend_url"
    LIVEKIT_URL: str = "livekit_url"
    LIVEKIT_API_KEY: str = "livekit_api_key"
    LIVEKIT_API_SECRET: str = "livekit_api_secret"
    CALLING_BACKEND_API_KEY: str = "calling_backend_api_key"
    X_API_KEY: str = "x_api_key"
    WEAVIATE_HOST: str = "weaviate_host"
    TWILIO_ACCOUNT_SID: str = "twilio_account_sid"
    TWILIO_AUTH_TOKEN: str = "twilio_auth_token"

    class Config:
        # Keep env_file for local development fallback, although environment vars take precedence.
        env_file: str = _ENV_FILE
        extra = "ignore"


api_config = Config()


# Log loaded config values (excluding sensitive keys)
def log_loaded_config():
    sensitive_keys = {"KEY", "TOKEN", "SECRET", "PASSWORD", "AUTH"}
    config_dict = api_config.model_dump()
    for key, value in config_dict.items():
        is_sensitive = any(sk in key.upper() for sk in sensitive_keys)
        display_value = "****" if is_sensitive and value else value
        logger.debug(f"Config - {key}: {display_value}")


log_loaded_config()
