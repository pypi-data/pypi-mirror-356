"""Configuration management for GitHub PR AI Agent."""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class Config:
    """Configuration settings for the GitHub PR AI Agent."""
    
    # GitHub settings
    github_token: str
    
    # Ollama settings
    ollama_url: str = "http://localhost:11434"
    ollama_model: str = "codellama:13b"
    
    # Server settings
    port: int = 5000
    host: str = "0.0.0.0"
    debug: bool = False
    
    # AI settings
    temperature: float = 0.1
    top_p: float = 0.9
    max_tokens: int = 2000
    timeout: int = 120
    
    @classmethod
    def from_env(cls) -> "Config":
        """Create configuration from environment variables."""
        github_token = os.getenv("GITHUB_TOKEN")
        if not github_token:
            raise ValueError("GITHUB_TOKEN environment variable is required")
        
        return cls(
            github_token=github_token,
            ollama_url=os.getenv("OLLAMA_URL", "http://localhost:11434"),
            ollama_model=os.getenv("OLLAMA_MODEL", "codellama:13b"),
            port=int(os.getenv("PORT", "5000")),
            host=os.getenv("HOST", "0.0.0.0"),
            debug=os.getenv("DEBUG", "").lower() in ("true", "1", "yes"),
            temperature=float(os.getenv("TEMPERATURE", "0.1")),
            top_p=float(os.getenv("TOP_P", "0.9")),
            max_tokens=int(os.getenv("MAX_TOKENS", "2000")),
            timeout=int(os.getenv("TIMEOUT", "120")),
        )
    
    def validate(self) -> None:
        """Validate configuration settings."""
        if not self.github_token:
            raise ValueError("GitHub token is required")
        
        if not self.ollama_url:
            raise ValueError("Ollama URL is required")
        
        if not self.ollama_model:
            raise ValueError("Ollama model is required")
        
        if self.port < 1 or self.port > 65535:
            raise ValueError("Port must be between 1 and 65535")
        
        if self.temperature < 0 or self.temperature > 2:
            raise ValueError("Temperature must be between 0 and 2")
        
        if self.top_p < 0 or self.top_p > 1:
            raise ValueError("Top-p must be between 0 and 1")
        
        if self.max_tokens < 1:
            raise ValueError("Max tokens must be positive")
        
        if self.timeout < 1:
            raise ValueError("Timeout must be positive")
