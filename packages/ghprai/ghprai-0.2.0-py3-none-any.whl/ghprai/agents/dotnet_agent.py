"""DotNet-specific AI Agent for code analysis and test generation."""

import json
import logging
import os
from typing import Dict, List, Optional
from pathlib import Path

from ..core.config import Config
from ..core.models import CodeAnalysis, GeneratedTest
from ..core.utils import FileAnalyzer
from ..core.dotnet_utils import DotNetAnalyzer, DotNetCodeParser, DotNetTemplateManager
from .ai_agent import OllamaAIAgent

logger = logging.getLogger(__name__)


class DotNetAIAgent(OllamaAIAgent):
    """AI Agent specialized for .NET code analysis and test generation."""
    
    def __init__(self, config: Config):
        super().__init__(config)
        self.dotnet_template_manager = DotNetTemplateManager()
    
    def analyze_dotnet_code_intelligence(self, code: str, file_path: str, project_path: str = None) -> CodeAnalysis:
        """Analyze .NET code with enhanced intelligence.
        
        Args:
            code: Source code to analyze
            file_path: Path to the source file
            project_path: Optional path to .csproj/.fsproj file for context
            
        Returns:
            CodeAnalysis object with detailed results
        """
        language = DotNetAnalyzer.get_dotnet_language(file_path)
        target_framework = "Unknown"
        
        # Extract project information if available
        if project_path and DotNetAnalyzer.is_dotnet_project_file(project_path):
            project_info = DotNetAnalyzer.get_project_info(project_path)
            target_framework = project_info.get('target_framework', 'Unknown')
        
        prompt = self.dotnet_template_manager.DOTNET_ANALYSIS_TEMPLATE.format(
            language=language,
            file_path=file_path,
            target_framework=target_framework,
            code=code
        )
        
        system_prompt = f"You are an expert .NET code analyzer specializing in {language}. Analyze code for complexity, testability, and .NET-specific issues."
        
        response = self._call_ollama(prompt, system_prompt)
        
        if not response:
            return self._basic_dotnet_code_analysis(code, file_path)
        
        try:
            # Try to parse JSON response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                analysis_data = json.loads(json_str)
                
                return CodeAnalysis(
                    file_path=file_path,
                    complexity_score=analysis_data.get("complexity_score", 5),
                    functions=analysis_data.get("methods", []) + analysis_data.get("functions", []),
                    classes=analysis_data.get("classes", []) + analysis_data.get("interfaces", []),
                    edge_cases=analysis_data.get("edge_cases", []),
                    dependencies=analysis_data.get("dependencies", []),
                    test_scenarios=analysis_data.get("test_scenarios", []),
                    security_concerns=analysis_data.get("security_concerns", []),
                    performance_issues=analysis_data.get("performance_issues", [])
                )
        except Exception as e:
            logger.error(f"Error parsing .NET AI analysis: {e}")
        
        # Fallback to basic analysis
        return self._basic_dotnet_code_analysis(code, file_path)
    
    def generate_dotnet_tests(self, code: str, file_path: str, analysis: CodeAnalysis, 
                             project_path: str = None) -> Optional[GeneratedTest]:
        """Generate comprehensive .NET tests using AI.
        
        Args:
            code: Source code to generate tests for
            file_path: Path to the source file
            analysis: Code analysis results
            project_path: Optional path to .csproj/.fsproj file for context
            
        Returns:
            GeneratedTest object or None if generation failed
        """
        language = DotNetAnalyzer.get_dotnet_language(file_path)
        target_framework = "net6.0"  # Default
        test_framework = DotNetAnalyzer.get_dotnet_test_framework(language, project_path)
        
        # Extract project information if available
        if project_path and DotNetAnalyzer.is_dotnet_project_file(project_path):
            project_info = DotNetAnalyzer.get_project_info(project_path)
            target_framework = project_info.get('target_framework', 'net6.0')
            
            # Use detected test framework if available
            detected_frameworks = project_info.get('test_frameworks', [])
            if detected_frameworks:
                test_framework = detected_frameworks[0]
        
        prompt = self.dotnet_template_manager.DOTNET_TEST_GENERATION_TEMPLATE.format(
            language=language,
            test_framework=test_framework,
            target_framework=target_framework,
            file_path=file_path,
            code=code,
            analysis=json.dumps({
                "classes": analysis.classes,
                "functions": analysis.functions,
                "edge_cases": analysis.edge_cases,
                "dependencies": analysis.dependencies,
                "test_scenarios": analysis.test_scenarios
            }, indent=2)
        )
        
        system_prompt = f"You are an expert .NET test generator. Generate comprehensive, production-ready unit tests using {test_framework} for {language} code targeting {target_framework}."
        
        response = self._call_ollama(prompt, system_prompt)
        
        if not response:
            return None
        
        # Clean and extract test code
        test_content = self._extract_code_from_response(response)
        
        if not test_content:
            return None
        
        # Generate test file path
        test_file = self._generate_dotnet_test_file_path(file_path, language)
        
        return GeneratedTest(
            source_file=file_path,
            test_file=test_file,
            test_content=test_content,
            framework=test_framework,
            language=language
        )
    
    def suggest_dotnet_code_improvements(self, code: str, file_path: str, project_path: str = None) -> List[str]:
        """Generate .NET-specific code improvement suggestions.
        
        Args:
            code: Source code to review
            file_path: Path to the source file
            project_path: Optional path to .csproj/.fsproj file for context
            
        Returns:
            List of improvement suggestions
        """
        language = DotNetAnalyzer.get_dotnet_language(file_path)
        target_framework = "Unknown"
        
        # Extract project information if available
        if project_path and DotNetAnalyzer.is_dotnet_project_file(project_path):
            project_info = DotNetAnalyzer.get_project_info(project_path)
            target_framework = project_info.get('target_framework', 'Unknown')
        
        prompt = self.dotnet_template_manager.DOTNET_CODE_REVIEW_TEMPLATE.format(
            language=language,
            file_path=file_path,
            target_framework=target_framework,
            code=code
        )
        
        system_prompt = f"You are a senior .NET code reviewer specializing in {language}. Provide specific, actionable suggestions."
        
        response = self._call_ollama(prompt, system_prompt)
        
        if not response:
            return ["Unable to generate improvement suggestions at this time."]
        
        # Parse suggestions from response
        suggestions = []
        lines = response.split('\n')
        
        for line in lines:
            line = line.strip()
            if line and any(line.startswith(prefix) for prefix in ['1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '-', '*']):
                suggestions.append(line.lstrip('0123456789.- '))
        
        return suggestions[:8]  # Limit to 8 suggestions
    
    def find_dotnet_project_context(self, file_path: str, temp_dir: str) -> Optional[str]:
        """Find the relevant .NET project file for a source file.
        
        Args:
            file_path: Path to the source file
            temp_dir: Temporary directory containing the repository
            
        Returns:
            Path to the project file or None if not found
        """
        file_dir = os.path.dirname(file_path)
        
        # Search upward from the file location
        current_dir = file_dir
        while current_dir and current_dir != temp_dir:
            # Check for project files in current directory
            for file in os.listdir(current_dir):
                if DotNetAnalyzer.is_dotnet_project_file(file):
                    project_path = os.path.join(current_dir, file)
                    logger.info(f"Found project file {project_path} for {file_path}")
                    return project_path
            
            # Move up one directory
            parent_dir = os.path.dirname(current_dir)
            if parent_dir == current_dir:  # Reached root
                break
            current_dir = parent_dir
        
        # If no project file found, look for any project file in the repository
        all_projects = DotNetAnalyzer.find_dotnet_projects(temp_dir)
        if all_projects:
            logger.info(f"Using fallback project file {all_projects[0]} for {file_path}")
            return all_projects[0]
        
        return None
    
    def _basic_dotnet_code_analysis(self, code: str, file_path: str) -> CodeAnalysis:
        """Fallback analysis for .NET code when AI is unavailable."""
        language = DotNetAnalyzer.get_dotnet_language(file_path)
        symbols = DotNetCodeParser.extract_dotnet_symbols(code, language)
        
        # Extract relevant symbols based on language
        if language == "csharp":
            functions = symbols.get('methods', [])
            classes = symbols.get('classes', []) + symbols.get('interfaces', [])
        elif language == "fsharp":
            functions = symbols.get('functions', []) + symbols.get('values', [])
            classes = symbols.get('types', []) + symbols.get('modules', [])
        else:  # vbnet
            functions = symbols.get('methods', [])
            classes = symbols.get('classes', [])
        
        # Basic complexity estimation
        complexity_score = min(10, max(1, len(functions) + len(classes)))
        
        return CodeAnalysis(
            file_path=file_path,
            complexity_score=complexity_score,
            functions=functions,
            classes=classes,
            edge_cases=[],
            dependencies=[],
            test_scenarios=[],
            security_concerns=[],
            performance_issues=[]
        )
    
    def _generate_dotnet_test_file_path(self, source_file: str, language: str) -> str:
        """Generate appropriate test file path for .NET source file."""
        source_path = Path(source_file)
        
        # Common .NET test naming convention
        test_name = f"{source_path.stem}Tests{source_path.suffix}"
        
        # Try to find the repository root by looking for solution files or going up directories
        repo_root = self._find_repository_root(source_file)
        
        # Look for existing test projects in the repository
        test_project_dir = self._find_test_project_directory(repo_root, source_file)
        
        if test_project_dir:
            # Use the existing test project directory
            test_dir = Path(test_project_dir).parent if test_project_dir.endswith(('.csproj', '.fsproj', '.vbproj')) else Path(test_project_dir)
        else:
            # Look for conventional test directories in the repository
            test_dir = self._find_or_create_test_directory(repo_root, source_path)
        
        test_file_path = test_dir / test_name
        
        # Ensure the directory exists
        test_dir.mkdir(parents=True, exist_ok=True)
        
        return str(test_file_path)
    
    def _find_repository_root(self, file_path: str) -> Path:
        """Find the repository root by looking for common indicators."""
        current_path = Path(file_path).parent
        
        # Look for common repository indicators
        repo_indicators = ['.git', '.sln', 'README.md', 'pyproject.toml', 'package.json']
        
        while current_path.parent != current_path:  # Not at filesystem root
            if any((current_path / indicator).exists() for indicator in repo_indicators):
                return current_path
            current_path = current_path.parent
        
        # If no indicators found, use the parent directory of the source file
        return Path(file_path).parent
    
    def _find_test_project_directory(self, repo_root: Path, source_file: str) -> Optional[str]:
        """Find existing test project directory in the repository."""
        # Look for test projects in common locations
        test_patterns = ['*test*', '*Test*', '*tests*', '*Tests*']
        
        for pattern in test_patterns:
            # Search for test project files first (most specific)
            for test_project in repo_root.rglob(f'{pattern}.*proj'):
                if test_project.is_file():
                    logger.info(f"Found test project: {test_project}")
                    return str(test_project)
        
        # Search for test directories with project files
        for pattern in test_patterns:
            for test_dir in repo_root.rglob(pattern):
                if test_dir.is_dir() and not test_dir.name.startswith('.'):  # Exclude hidden directories
                    # Check if this directory contains test project files
                    for proj_file in test_dir.glob('*.*proj'):
                        if proj_file.is_file():
                            logger.info(f"Found test project in directory: {proj_file}")
                            return str(proj_file)
        
        # Finally, look for test directories without project files
        for pattern in test_patterns:
            for test_dir in repo_root.rglob(pattern):
                if (test_dir.is_dir() and 
                    not test_dir.name.startswith('.') and  # Exclude hidden directories
                    any(test_word in test_dir.name.lower() for test_word in ['test', 'spec', 'unit']) and
                    'cache' not in test_dir.name.lower()):  # Exclude cache directories
                    logger.info(f"Found test directory: {test_dir}")
                    return str(test_dir)
        
        return None
    
    def _find_or_create_test_directory(self, repo_root: Path, source_path: Path) -> Path:
        """Find or create an appropriate test directory."""
        # Common test directory names in order of preference
        test_dir_names = ['tests', 'test', 'Tests', 'Test', 'UnitTests']
        
        # First, look for existing test directories in the repository
        for test_dir_name in test_dir_names:
            potential_test_dir = repo_root / test_dir_name
            if potential_test_dir.exists() and potential_test_dir.is_dir():
                logger.info(f"Using existing test directory: {potential_test_dir}")
                return potential_test_dir
        
        # If no existing test directory, check if we're in a typical project structure
        # Look for src directory and create parallel tests directory
        if 'src' in source_path.parts:
            # Find the src directory in the path and create parallel tests directory
            parts = list(source_path.parts)
            try:
                src_index = parts.index('src')
                test_parts = parts[:src_index] + ['tests'] + parts[src_index+1:-1]  # Remove filename
                test_dir = Path(*test_parts)
                logger.info(f"Creating parallel test directory to src: {test_dir}")
                return test_dir
            except ValueError:
                pass
        
        # Default: create tests directory in repository root
        default_test_dir = repo_root / 'tests'
        logger.info(f"Using default test directory: {default_test_dir}")
        return default_test_dir
