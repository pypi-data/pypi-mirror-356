"""Test cases for AI Agent functionality."""

import pytest
from unittest.mock import Mock, patch, MagicMock
import json

from ghprai.agents.ai_agent import OllamaAIAgent
from ghprai.core.config import Config
from ghprai.core.models import CodeAnalysis


@pytest.fixture
def config():
    """Create test configuration."""
    return Config(
        github_token="test_token",
        ollama_url="http://localhost:11434",
        ollama_model="codellama:13b"
    )


@pytest.fixture
def ai_agent(config):
    """Create AI agent for testing."""
    return OllamaAIAgent(config)


@pytest.fixture
def mock_ollama_response():
    """Mock successful Ollama API response."""
    return {
        "response": json.dumps({
            "complexity_score": 7,
            "functions": ["calculate", "validate_input"],
            "classes": ["Calculator"],
            "edge_cases": ["division by zero", "invalid input types"],
            "dependencies": ["math"],
            "test_scenarios": ["test positive numbers", "test negative numbers", "test zero"],
            "security_concerns": ["input validation needed"],
            "performance_issues": ["could use caching"]
        })
    }


class TestOllamaAIAgent:
    """Test cases for OllamaAIAgent."""
    
    def test_initialization(self, config):
        """Test agent initialization."""
        agent = OllamaAIAgent(config)
        
        assert agent.config == config
        assert agent.session is not None
        assert agent.template_manager is not None
    
    @patch('requests.Session.post')
    def test_call_ollama_success(self, mock_post, ai_agent, mock_ollama_response):
        """Test successful Ollama API call."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_ollama_response
        mock_post.return_value = mock_response
        
        result = ai_agent._call_ollama("test prompt")
        
        assert result == mock_ollama_response["response"]
        mock_post.assert_called_once()
    
    @patch('requests.Session.post')
    def test_call_ollama_failure(self, mock_post, ai_agent):
        """Test failed Ollama API call."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response
        
        result = ai_agent._call_ollama("test prompt")
        
        assert result == ""
    
    @patch('requests.Session.post')
    def test_analyze_code_intelligence(self, mock_post, ai_agent, mock_ollama_response):
        """Test code intelligence analysis."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_ollama_response
        mock_post.return_value = mock_response
        
        code = """
def calculate(a, b):
    return a + b

class Calculator:
    def add(self, x, y):
        return x + y
"""
        
        analysis = ai_agent.analyze_code_intelligence(code, "test.py")
        
        assert isinstance(analysis, CodeAnalysis)
        assert analysis.file_path == "test.py"
        assert analysis.complexity_score == 7
        assert "calculate" in analysis.functions
        assert "Calculator" in analysis.classes
        assert "division by zero" in analysis.edge_cases
    
    @patch('requests.Session.post')
    def test_analyze_code_fallback(self, mock_post, ai_agent):
        """Test fallback analysis when AI fails."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": "invalid json"}
        mock_post.return_value = mock_response
        
        code = """
def simple_func():
    return "hello"
"""
        
        analysis = ai_agent.analyze_code_intelligence(code, "test.py")
        
        assert isinstance(analysis, CodeAnalysis)
        assert analysis.file_path == "test.py"
        assert analysis.complexity_score == 5  # Default fallback value
        assert "simple_func" in analysis.functions
    
    @patch('requests.Session.post')
    def test_generate_intelligent_tests(self, mock_post, ai_agent):
        """Test test generation."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "response": """```python
import pytest
from test_module import calculate

def test_calculate_positive():
    assert calculate(2, 3) == 5

def test_calculate_negative():
    assert calculate(-1, 1) == 0
```"""
        }
        mock_post.return_value = mock_response
        
        code = "def calculate(a, b): return a + b"
        analysis = CodeAnalysis(
            file_path="test.py",
            complexity_score=3,
            functions=["calculate"]
        )
        
        generated_test = ai_agent.generate_intelligent_tests(code, "test.py", analysis)
        
        assert generated_test is not None
        assert generated_test.source_file == "test.py"
        assert generated_test.test_file == "test_test.py"
        assert "def test_calculate_positive" in generated_test.test_content
        assert generated_test.framework == "pytest"
        assert generated_test.language == "python"
    
    @patch('requests.Session.post')
    def test_suggest_code_improvements(self, mock_post, ai_agent):
        """Test code improvement suggestions."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "response": """1. Add type hints for better readability
2. Implement input validation
3. Add docstrings to functions
4. Use more descriptive variable names
5. Consider error handling for edge cases"""
        }
        mock_post.return_value = mock_response
        
        code = "def calc(a, b): return a + b"
        suggestions = ai_agent.suggest_code_improvements(code, "test.py")
        
        assert len(suggestions) > 0
        assert any("type hints" in suggestion for suggestion in suggestions)
    
    @patch('requests.Session.get')
    def test_health_check_connected(self, mock_get, ai_agent):
        """Test health check when connected."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        health_info = ai_agent.health_check()
        
        assert health_info["ollama_status"] == "connected"
        assert health_info["ollama_url"] == ai_agent.config.ollama_url
        assert health_info["model"] == ai_agent.config.ollama_model
    
    @patch('requests.Session.get')
    def test_health_check_disconnected(self, mock_get, ai_agent):
        """Test health check when disconnected."""
        mock_get.side_effect = Exception("Connection failed")
        
        health_info = ai_agent.health_check()
        
        assert health_info["ollama_status"] == "disconnected"
    
    def test_extract_code_from_response(self, ai_agent):
        """Test code extraction from AI response."""
        response_with_code_blocks = """Here's the test code:

```python
def test_example():
    assert True
```

This should work well."""
        
        extracted = ai_agent._extract_code_from_response(response_with_code_blocks)
        assert "def test_example():" in extracted
        assert "assert True" in extracted
        assert "Here's the test code:" not in extracted
    
    def test_basic_code_analysis_python(self, ai_agent):
        """Test basic code analysis for Python."""
        code = """
def func1():
    pass

class MyClass:
    def method1(self):
        pass
"""
        
        analysis = ai_agent._basic_code_analysis(code, "test.py")
        
        assert analysis.file_path == "test.py"
        assert "func1" in analysis.functions
        assert "MyClass" in analysis.classes
        assert analysis.complexity_score == 5
