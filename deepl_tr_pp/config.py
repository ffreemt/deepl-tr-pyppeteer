"""Configure params DEBUG HEADFUL PROXY."""
from typing import Optional

# import dotenv
from pydantic import BaseSettings, AnyUrl  # pylint: disable=no-name-in-module


class Settings(BaseSettings):  # pylint: disable=too-few-public-methods
    """Configure params DEBUG HEADFUL PROXY."""

    debug: bool = False
    headful: bool = False
    proxy: Optional[AnyUrl] = None

    class Config:  # pylint: disable=too-few-public-methods
        """Config."""

        env_prefix = "deepltr_"
        # extra = "allow"
        env_file = ".env"
        env_file_encoding = "utf-8"  # pydantic doc
