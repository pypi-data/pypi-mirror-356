"""Test cases for CLI functionality."""

import pytest
import tempfile
import os
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

from ghprai.cli import analyze_repository, generate_tests_for_file, health_check
from ghprai.core.config import Config


@pytest.fixture
def config():
    """Create test configuration."""
    return Config(
        github_token="test_token",
        ollama_url="http://localhost:11434",
        ollama_model="codellama:13b"
    )


@pytest.fixture
def temp_repo():
    """Create a temporary repository for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create source directory and files
        src_dir = Path(temp_dir) / "src"
        src_dir.mkdir()
        
        # Create a Python source file
        python_file = src_dir / "calculator.py"
        python_file.write_text("""
def add(a, b):
    '''Add two numbers.'''
    return a + b

def subtract(a, b):
    '''Subtract b from a.'''
    return a - b

class Calculator:
    '''Simple calculator class.'''
    
    def multiply(self, a, b):
        return a * b
""")
        
        # Create a JavaScript file
        js_file = src_dir / "utils.js"
        js_file.write_text("""
function formatString(str) {
    return str.trim().toLowerCase();
}

class StringUtils {
    static isEmpty(str) {
        return !str || str.length === 0;
    }
}
""")
        
        # Create tests directory with one test file
        tests_dir = Path(temp_dir) / "tests"
        tests_dir.mkdir()
        
        test_file = tests_dir / "test_calculator.py"
        test_file.write_text("""
import pytest
from src.calculator import add

def test_add():
    assert add(2, 3) == 5
""")
        
        yield temp_dir


class TestCLIAnalyzeRepository:
    """Test cases for repository analysis CLI command."""
    
    @patch('ghprai.cli.OllamaAIAgent')
    def test_analyze_repository_success(self, mock_ai_agent_class, config, temp_repo, capsys):
        """Test successful repository analysis."""
        # Mock AI agent
        mock_ai_agent = Mock()
        mock_ai_agent.analyze_code_intelligence.return_value = Mock(
            complexity_score=5,
            risk_level="medium",
            security_concerns=[],
            functions=["add", "subtract"],
            classes=["Calculator"]
        )
        mock_ai_agent_class.return_value = mock_ai_agent
        
        # Run analysis
        analyze_repository(temp_repo, config)
        
        # Check output
        captured = capsys.readouterr()
        assert "Analyzing repository" in captured.out
        assert "Found 2 source files" in captured.out
        assert "calculator.py" in captured.out
        assert "utils.js" in captured.out
        assert "Analysis Summary" in captured.out
    
    def test_analyze_repository_nonexistent_path(self, config, capsys):
        """Test analysis with non-existent repository path."""
        with pytest.raises(SystemExit):
            analyze_repository("/nonexistent/path", config)
    
    @patch('ghprai.cli.OllamaAIAgent')
    def test_analyze_repository_no_source_files(self, mock_ai_agent_class, config, capsys):
        """Test analysis with no source files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create empty directory
            analyze_repository(temp_dir, config)
            
            captured = capsys.readouterr()
            assert "No source files found" in captured.out


class TestCLIGenerateTests:
    """Test cases for test generation CLI command."""
    
    @patch('ghprai.cli.OllamaAIAgent')
    def test_generate_tests_for_file_success(self, mock_ai_agent_class, config, temp_repo, capsys):
        """Test successful test generation."""
        # Mock AI agent
        mock_ai_agent = Mock()
        mock_analysis = Mock(
            complexity_score=4,
            functions=["add", "subtract"],
            classes=["Calculator"]
        )
        mock_generated_test = Mock(
            test_file="test_calculator.py",
            test_content="def test_add(): assert add(1, 2) == 3",
            framework="pytest",
            language="python"
        )
        
        mock_ai_agent.analyze_code_intelligence.return_value = mock_analysis
        mock_ai_agent.generate_intelligent_tests.return_value = mock_generated_test
        mock_ai_agent_class.return_value = mock_ai_agent
        
        # Create source file path
        source_file = os.path.join(temp_repo, "src", "calculator.py")
        
        # Run test generation
        generate_tests_for_file(source_file, config)
        
        # Check output
        captured = capsys.readouterr()
        assert "Generating tests for" in captured.out
        assert "Analyzing code" in captured.out
        assert "Test file generated" in captured.out
        assert "pytest" in captured.out
    
    def test_generate_tests_nonexistent_file(self, config):
        """Test test generation with non-existent file."""
        with pytest.raises(SystemExit):
            generate_tests_for_file("/nonexistent/file.py", config)
    
    def test_generate_tests_non_source_file(self, config):
        """Test test generation with non-source file."""
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as temp_file:
            temp_file.write(b"This is not a source file")
            temp_file.flush()
            
            try:
                with pytest.raises(SystemExit):
                    generate_tests_for_file(temp_file.name, config)
            finally:
                os.unlink(temp_file.name)
    
    @patch('ghprai.cli.OllamaAIAgent')
    def test_generate_tests_ai_failure(self, mock_ai_agent_class, config, temp_repo, capsys):
        """Test test generation when AI fails."""
        # Mock AI agent that fails to generate tests
        mock_ai_agent = Mock()
        mock_analysis = Mock(complexity_score=3, functions=["add"], classes=[])
        mock_ai_agent.analyze_code_intelligence.return_value = mock_analysis
        mock_ai_agent.generate_intelligent_tests.return_value = None
        mock_ai_agent_class.return_value = mock_ai_agent
        
        source_file = os.path.join(temp_repo, "src", "calculator.py")
        
        generate_tests_for_file(source_file, config)
        
        captured = capsys.readouterr()
        assert "Failed to generate tests" in captured.out


class TestCLIHealthCheck:
    """Test cases for health check CLI command."""
    
    @patch('ghprai.cli.OllamaAIAgent')
    def test_health_check_success(self, mock_ai_agent_class, config, capsys):
        """Test successful health check."""
        # Mock AI agent with successful health check
        mock_ai_agent = Mock()
        mock_ai_agent.health_check.return_value = {
            "ollama_status": "connected",
            "ollama_url": "http://localhost:11434",
            "model": "codellama:13b"
        }
        mock_analysis = Mock(functions=["test_func"])
        mock_ai_agent.analyze_code_intelligence.return_value = mock_analysis
        mock_ai_agent_class.return_value = mock_ai_agent
        
        health_check(config)
        
        captured = capsys.readouterr()
        assert "Health Check" in captured.out
        assert "Ollama connected" in captured.out
        assert "codellama:13b" in captured.out
        assert "AI analysis working" in captured.out
    
    @patch('ghprai.cli.OllamaAIAgent')
    def test_health_check_ollama_disconnected(self, mock_ai_agent_class, config, capsys):
        """Test health check with Ollama disconnected."""
        # Mock AI agent with failed health check
        mock_ai_agent = Mock()
        mock_ai_agent.health_check.return_value = {
            "ollama_status": "disconnected",
            "ollama_url": "http://localhost:11434",
            "model": "codellama:13b"
        }
        mock_ai_agent_class.return_value = mock_ai_agent
        
        health_check(config)
        
        captured = capsys.readouterr()
        assert "Ollama not connected" in captured.out
        assert "ollama serve" in captured.out
    
    @patch('ghprai.cli.OllamaAIAgent')
    def test_health_check_ai_test_failure(self, mock_ai_agent_class, config, capsys):
        """Test health check with AI test failure."""
        # Mock AI agent with successful connection but failed AI test
        mock_ai_agent = Mock()
        mock_ai_agent.health_check.return_value = {
            "ollama_status": "connected",
            "ollama_url": "http://localhost:11434",
            "model": "codellama:13b"
        }
        mock_ai_agent.analyze_code_intelligence.side_effect = Exception("AI test failed")
        mock_ai_agent_class.return_value = mock_ai_agent
        
        health_check(config)
        
        captured = capsys.readouterr()
        assert "AI test failed" in captured.out
