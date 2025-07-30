"""AI Agent for code analysis and test generation using Ollama."""

import json
import logging
import re
import requests
from typing import Dict, List, Optional

from ..core.config import Config
from ..core.models import CodeAnalysis, GeneratedTest
from ..core.utils import FileAnalyzer, CodeParser, TemplateManager

logger = logging.getLogger(__name__)


class OllamaAIAgent:
    """AI Agent powered by Ollama for code analysis and test generation."""
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize the Ollama AI Agent.
        
        Args:
            config: Configuration object. If None, loads from environment.
        """
        self.config = config or Config.from_env()
        self.session = requests.Session()
        self.template_manager = TemplateManager()
    
    def _call_ollama(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Make API call to Ollama.
        
        Args:
            prompt: The main prompt to send
            system_prompt: Optional system prompt for context
            
        Returns:
            Response text from the model
        """
        try:
            payload = {
                "model": self.config.ollama_model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": self.config.temperature,
                    "top_p": self.config.top_p,
                    "max_tokens": self.config.max_tokens
                }
            }
            
            if system_prompt:
                payload["system"] = system_prompt
            
            response = self.session.post(
                f"{self.config.ollama_url}/api/generate",
                json=payload,
                timeout=self.config.timeout
            )
            
            if response.status_code == 200:
                return response.json().get("response", "")
            else:
                logger.error(f"Ollama API error: {response.status_code}")
                return ""
                
        except Exception as e:
            logger.error(f"Error calling Ollama: {e}")
            return ""
    
    def analyze_code_intelligence(self, code: str, file_path: str) -> CodeAnalysis:
        """Intelligent code analysis using local LLM.
        
        Args:
            code: Source code to analyze
            file_path: Path to the file being analyzed
            
        Returns:
            CodeAnalysis object with detailed analysis results
        """
        language = FileAnalyzer.get_language(file_path)
        
        prompt = self.template_manager.ANALYSIS_TEMPLATE.format(
            file_path=file_path,
            language=language,
            code=code
        )
        
        system_prompt = "You are an expert code analyzer. Analyze code for complexity, testability, and potential issues. Return structured analysis in JSON format."
        
        response = self._call_ollama(prompt, system_prompt)
        
        try:
            # Clean response and parse JSON
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                analysis_data = json.loads(json_str)
                
                return CodeAnalysis(
                    file_path=file_path,
                    complexity_score=analysis_data.get("complexity_score", 5),
                    functions=analysis_data.get("functions", []),
                    classes=analysis_data.get("classes", []),
                    edge_cases=analysis_data.get("edge_cases", []),
                    dependencies=analysis_data.get("dependencies", []),
                    test_scenarios=analysis_data.get("test_scenarios", []),
                    security_concerns=analysis_data.get("security_concerns", []),
                    performance_issues=analysis_data.get("performance_issues", [])
                )
        except Exception as e:
            logger.error(f"Error parsing AI analysis: {e}")
        
        # Fallback to basic analysis
        return self._basic_code_analysis(code, file_path)
    
    def generate_intelligent_tests(self, code: str, file_path: str, analysis: CodeAnalysis) -> Optional[GeneratedTest]:
        """Generate comprehensive tests using AI.
        
        Args:
            code: Source code to generate tests for
            file_path: Path to the source file
            analysis: Code analysis results
            
        Returns:
            GeneratedTest object or None if generation failed
        """
        language = FileAnalyzer.get_language(file_path)
        test_framework = FileAnalyzer.get_test_framework(language)
        
        prompt = self.template_manager.TEST_GENERATION_TEMPLATE.format(
            language=language,
            test_framework=test_framework,
            file_path=file_path,
            code=code,
            analysis=json.dumps({
                "functions": analysis.functions,
                "classes": analysis.classes,
                "edge_cases": analysis.edge_cases,
                "dependencies": analysis.dependencies,
                "test_scenarios": analysis.test_scenarios
            }, indent=2)
        )
        
        system_prompt = f"You are an expert test generator. Generate comprehensive, production-ready unit tests using {test_framework} for {language} code."
        
        response = self._call_ollama(prompt, system_prompt)
        
        if not response:
            return None
        
        # Clean up response to extract just the code
        test_content = self._extract_code_from_response(response)
        
        if not test_content:
            return None
        
        # Generate test filename
        from pathlib import Path
        source_stem = Path(file_path).stem
        test_filename = f"test_{source_stem}.py" if language == "python" else f"{source_stem}.test.js"
        
        return GeneratedTest(
            source_file=file_path,
            test_file=test_filename,
            test_content=test_content,
            framework=test_framework,
            language=language
        )
    
    def suggest_code_improvements(self, code: str, file_path: str) -> List[str]:
        """AI suggestions for code quality improvements.
        
        Args:
            code: Source code to review
            file_path: Path to the file
            
        Returns:
            List of improvement suggestions
        """
        language = FileAnalyzer.get_language(file_path)
        
        prompt = self.template_manager.CODE_REVIEW_TEMPLATE.format(
            file_path=file_path,
            language=language,
            code=code
        )
        
        system_prompt = "You are a senior code reviewer. Provide specific, actionable suggestions for code improvement."
        
        response = self._call_ollama(prompt, system_prompt)
        
        # Extract numbered suggestions
        suggestions = []
        lines = response.split('\n')
        for line in lines:
            line = line.strip()
            if re.match(r'^\d+\.', line) or line.startswith('- '):
                suggestions.append(line.lstrip('0123456789.- '))
        
        return suggestions[:8]  # Limit to 8 suggestions
    
    def _basic_code_analysis(self, code: str, file_path: str) -> CodeAnalysis:
        """Fallback basic analysis without AI.
        
        Args:
            code: Source code to analyze
            file_path: Path to the file
            
        Returns:
            Basic CodeAnalysis object
        """
        language = FileAnalyzer.get_language(file_path)
        symbols = CodeParser.extract_symbols(code, language)
        
        return CodeAnalysis(
            file_path=file_path,
            complexity_score=5,
            functions=symbols.get("functions", []),
            classes=symbols.get("classes", []),
            edge_cases=["null/empty inputs", "boundary conditions"],
            dependencies=[],
            test_scenarios=[f"Test {func}" for func in symbols.get("functions", [])],
            security_concerns=[],
            performance_issues=[]
        )
    
    def _extract_code_from_response(self, response: str) -> str:
        """Extract code from AI response.
        
        Args:
            response: Raw response from AI
            
        Returns:
            Cleaned code content
        """
        # Look for code blocks first
        if "```" in response:
            code_blocks = response.split("```")
            for i, block in enumerate(code_blocks):
                # Skip the first block (before first ```)
                if i == 0:
                    continue
                # Skip language specifier lines
                lines = block.strip().split('\n')
                if lines and any(keyword in lines[0].lower() for keyword in [
                    "python", "javascript", "typescript", "java", "csharp", "fsharp", "vbnet", 
                    "c#", "f#", "vb", "cs", "fs", "vb.net", "go", "rust", "cpp", "c++"
                ]):
                    lines = lines[1:]  # Remove language specifier
                block_content = '\n'.join(lines)
                
                # Check if this looks like test code
                if any(keyword in block_content.lower() for keyword in [
                    "test", "import", "def ", "class ", "it(", "describe(", "using", "[fact]", "[test]"
                ]):
                    return block_content.strip()
        
        # If no code blocks, return the response as-is
        return response.strip()
    
    def health_check(self) -> Dict[str, str]:
        """Check health of Ollama connection.
        
        Returns:
            Dictionary with health status information
        """
        try:
            response = self.session.get(f"{self.config.ollama_url}/api/tags", timeout=5)
            ollama_status = "connected" if response.status_code == 200 else "disconnected"
        except:
            ollama_status = "disconnected"
        
        return {
            "ollama_status": ollama_status,
            "ollama_url": self.config.ollama_url,
            "model": self.config.ollama_model
        }
