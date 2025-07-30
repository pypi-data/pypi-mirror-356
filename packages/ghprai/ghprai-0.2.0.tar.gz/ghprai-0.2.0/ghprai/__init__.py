"""GitHub PR AI Agent - AI-powered code review and test generation."""

from .agents.ai_agent import OllamaAIAgent
from .agents.dotnet_agent import DotNetAIAgent
from .agents.github_agent import GitHubPRAgent
from .core.models import CodeAnalysis, TestCoverage
from .core.config import Config

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

__all__ = [
    "OllamaAIAgent",
    "DotNetAIAgent",
    "GitHubPRAgent", 
    "CodeAnalysis",
    "TestCoverage",
    "Config",
]
