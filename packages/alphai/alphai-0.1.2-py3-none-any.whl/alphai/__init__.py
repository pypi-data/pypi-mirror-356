"""alphai - A CLI tool and Python package for the runalph.ai platform."""

__version__ = "0.1.2"
__author__ = "American Data Science"
__email__ = "support@americandatascience.com"

from .client import AlphAIClient
from .config import Config

__all__ = ["AlphAIClient", "Config", "__version__"]
