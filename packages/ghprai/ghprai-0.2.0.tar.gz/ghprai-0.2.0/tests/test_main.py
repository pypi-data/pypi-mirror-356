import os
import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

from ghprai import OllamaAIAgent, GitHubPRAgent
from ghprai.core.config import Config
from ghprai.server.app import create_app


@pytest.fixture
def config():
    """Create test configuration."""
    return Config(
        github_token="test_token",
        ollama_url="http://localhost:11434",
        ollama_model="codellama:13b"
    )


@pytest.fixture
def client(config):
    """Create test client."""
    app = create_app(config)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_ollama_agent():
    """Mock Ollama AI Agent."""
    with patch('ghprai.agents.ai_agent.OllamaAIAgent') as mock:
        mock_instance = Mock()
        mock_instance.health_check.return_value = {
            "ollama_status": "connected",
            "ollama_url": "http://localhost:11434",
            "model": "codellama:13b"
        }
        mock.return_value = mock_instance
        yield mock_instance


def test_health_check(client, mock_ollama_agent):
    """Test the health check endpoint."""
    response = client.get('/health')
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['status'] == 'healthy'
    assert 'ollama' in data
    assert data['model'] == 'codellama:13b'


def test_webhook_no_pr_event(client):
    """Test webhook endpoint with non-PR event."""
    response = client.post('/webhook', json={'action': 'opened'})
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['status'] == 'ignored'
    assert data['reason'] == 'Not a PR event'


@pytest.mark.asyncio
async def test_ollama_ai_agent(config):
    """Test OllamaAIAgent functionality."""
    with patch('requests.Session') as mock_session:
        # Mock successful Ollama response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "response": '{"complexity_score": 3, "functions": ["add"], "classes": [], "edge_cases": ["null inputs"], "dependencies": [], "test_scenarios": ["Test add"], "security_concerns": [], "performance_issues": []}'
        }
        mock_session.return_value.post.return_value = mock_response
        
        agent = OllamaAIAgent(config)
        
        # Test code analysis
        code = """
def add(a: int, b: int) -> int:
    return a + b
"""
        analysis = agent.analyze_code_intelligence(code, 'test.py')
        
        assert analysis.file_path == 'test.py'
        assert analysis.complexity_score == 3
        assert 'add' in analysis.functions


def test_github_pr_agent_initialization(config):
    """Test GitHubPRAgent initialization."""
    with patch('github.Github'):
        agent = GitHubPRAgent(config)
        
        assert agent.config == config
        assert agent.ai_agent is not None
        assert isinstance(agent.ai_agent, OllamaAIAgent)


def test_test_ai_endpoint(client):
    """Test the test-ai endpoint."""
    with patch('ghprai.agents.ai_agent.OllamaAIAgent.analyze_code_intelligence') as mock_analyze:
        from ghprai.core.models import CodeAnalysis
        
        mock_analyze.return_value = CodeAnalysis(
            file_path="test.py",
            complexity_score=5,
            functions=["test_func"],
            classes=[],
            edge_cases=["null input"],
            test_scenarios=["Test function"]
        )
        
        response = client.post('/test-ai', json={
            'code': 'def test_func(): pass',
            'file_path': 'test.py'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'analysis' in data
        assert data['analysis']['complexity_score'] == 5
        assert 'test_func' in data['analysis']['functions']


def test_config_from_env():
    """Test configuration loading from environment."""
    with patch.dict(os.environ, {
        'GITHUB_TOKEN': 'test_token',
        'OLLAMA_URL': 'http://test:11434',
        'OLLAMA_MODEL': 'test-model'
    }):
        config = Config.from_env()
        
        assert config.github_token == 'test_token'
        assert config.ollama_url == 'http://test:11434'
        assert config.ollama_model == 'test-model'


def test_config_validation(config):
    """Test configuration validation."""
    # Valid config should not raise
    config.validate()
    
    # Invalid config should raise
    config.github_token = ""
    with pytest.raises(ValueError):
        config.validate()
