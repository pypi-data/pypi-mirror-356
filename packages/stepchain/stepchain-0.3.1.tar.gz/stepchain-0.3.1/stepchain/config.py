"""Configuration management for StepChain.

Simple configuration using environment variables with validation.
"""

import os
from pathlib import Path

from pydantic import BaseModel, Field, field_validator

from stepchain.utils.logging import setup_logging


class Config(BaseModel):
    """Configuration for StepChain.
    
    All settings can be overridden via environment variables.
    """
    
    # OpenAI settings
    openai_api_key: str | None = Field(None)
    openai_model: str = Field("gpt-4o-mini")
    openai_timeout: int = Field(30, ge=1, le=300)
    
    # Execution settings
    max_retries: int = Field(3, ge=0, le=10)
    max_concurrent_steps: int = Field(5, ge=1, le=20)
    
    # Storage settings
    storage_path: str | Path = Field(".stepchain")
    
    # Decomposition settings
    max_steps_per_plan: int = Field(20, ge=1, le=50)
    
    # Feature flags
    enable_telemetry: bool = Field(False)
    debug_mode: bool = Field(False)
    
    # Additional settings for compatibility
    log_level: str = Field("INFO")
    llm_model: str = Field("gpt-4")
    base_delay: float = Field(1.0)
    max_delay: float = Field(60.0)
    timeout_seconds: int = Field(300)
    
    @classmethod
    def from_env(cls) -> "Config":
        """Create config from environment variables."""
        return cls(
            openai_api_key=os.environ.get("OPENAI_API_KEY"),
            openai_model=os.environ.get("STEPCHAIN_MODEL", "gpt-4o-mini"),
            openai_timeout=int(os.environ.get("STEPCHAIN_TIMEOUT", "30")),
            max_retries=int(os.environ.get("STEPCHAIN_MAX_RETRIES", "3")),
            max_concurrent_steps=int(os.environ.get("STEPCHAIN_MAX_CONCURRENT", "5")),
            storage_path=os.environ.get("STEPCHAIN_STORAGE_PATH", ".stepchain"),
            max_steps_per_plan=int(os.environ.get("STEPCHAIN_MAX_STEPS", "20")),
            enable_telemetry=os.environ.get("STEPCHAIN_TELEMETRY", "").lower()
                in ("true", "1", "yes"),
            debug_mode=os.environ.get("STEPCHAIN_DEBUG", "").lower() in ("true", "1", "yes"),
            log_level=os.environ.get("STEPCHAIN_LOG_LEVEL", "INFO"),
            base_delay=float(os.environ.get("STEPCHAIN_BASE_DELAY", "1.0")),
            max_delay=float(os.environ.get("STEPCHAIN_MAX_DELAY", "60.0")),
        )
    
    @field_validator("openai_api_key", mode="before")
    @classmethod
    def validate_api_key(cls, v: str | None) -> str | None:
        """Validate API key is set when needed."""
        # Don't fail here - let it fail when actually needed
        return v
    
    def validate_on_init(self) -> None:
        """Validate configuration on initialization."""
        if not self.openai_api_key and not os.environ.get("OPENAI_API_KEY"):
            raise ValueError(
                "OpenAI API key not found. Set OPENAI_API_KEY environment variable "
                "or pass api_key to setup_stepchain()"
            )
        
        # Create storage directory if it doesn't exist
        Path(self.storage_path).mkdir(parents=True, exist_ok=True)
        
        # Set up logging based on debug mode
        setup_logging(debug=self.debug_mode)
    


# Global config instance
_config: Config | None = None


def get_config() -> Config:
    """Get the global configuration instance.
    
    Creates a singleton instance on first call.
    """
    global _config
    if _config is None:
        _config = Config.from_env()
    return _config


def reset_config() -> None:
    """Reset the configuration (mainly for testing)."""
    global _config
    _config = None


def setup_stepchain(
    api_key: str | None = None,
    model: str = "gpt-4o-mini",
    storage_path: str = ".stepchain",
    enable_telemetry: bool = False,
    debug: bool = False,
) -> Config:
    """Simple setup helper for StepChain.
    
    Args:
        api_key: OpenAI API key (defaults to env var)
        model: Model to use (default: gpt-4o-mini)
        storage_path: Path for storing results
        enable_telemetry: Enable telemetry collection
        debug: Enable debug mode
        
    Returns:
        Configured Config instance
        
    Example:
        >>> from stepchain import setup_stepchain
        >>> config = setup_stepchain(api_key="sk-...")
    """
    # Set environment variables if provided
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
    
    os.environ["STEPCHAIN_MODEL"] = model
    os.environ["STEPCHAIN_STORAGE_PATH"] = storage_path
    os.environ["STEPCHAIN_TELEMETRY"] = "true" if enable_telemetry else "false"
    os.environ["STEPCHAIN_DEBUG"] = "true" if debug else "false"
    
    # Reset and get new config
    reset_config()
    config = get_config()
    
    # Validate configuration
    config.validate_on_init()
    
    return config