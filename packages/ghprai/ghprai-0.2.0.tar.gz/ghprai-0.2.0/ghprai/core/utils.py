"""Core utilities and helpers."""

import os
import re
import ast
import logging
from pathlib import Path
from typing import List, Set, Dict, Optional

logger = logging.getLogger(__name__)


class FileAnalyzer:
    """Utility class for analyzing files and detecting patterns."""
    
    # File extensions for different languages
    CODE_EXTENSIONS = {'.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.go', '.rs', '.cpp', '.c', '.h', '.cs', '.fs', '.vb'}
    
    # Common source folder patterns
    SOURCE_FOLDERS = {'src', 'lib', 'app', 'source', 'main', 'core', 'shared', 'common'}
    
    # Common test file/folder patterns
    TEST_PATTERNS = {
        'test', 'tests', 'spec', 'specs', '__tests__', 
        'test_', '_test', '.test', '.spec', 'unittest', 'integrationtest'
    }
    
    @classmethod
    def is_code_file(cls, file_path: str) -> bool:
        """Check if file is a source code file."""
        return Path(file_path).suffix.lower() in cls.CODE_EXTENSIONS
    
    @classmethod
    def is_test_file(cls, file_path: str) -> bool:
        """Check if file is a test file."""
        file_path_obj = Path(file_path)
        path_parts = file_path_obj.parts
        
        return any(
            pattern in file_path_obj.name.lower() or 
            pattern in str(file_path_obj).lower() or
            any(pattern in part.lower() for part in path_parts)
            for pattern in cls.TEST_PATTERNS
        )
    
    @classmethod
    def is_source_file(cls, file_path: str) -> bool:
        """Check if file is in source folders (not test)."""
        if not cls.is_code_file(file_path):
            return False
        
        if cls.is_test_file(file_path):
            return False
        
        path_parts = Path(file_path).parts
        return any(part in cls.SOURCE_FOLDERS for part in path_parts)
    
    @classmethod
    def get_language(cls, file_path: str) -> str:
        """Get programming language from file extension."""
        ext = Path(file_path).suffix.lower()
        mapping = {
            '.py': 'python', 
            '.js': 'javascript', 
            '.ts': 'typescript',
            '.java': 'java', 
            '.go': 'go', 
            '.rs': 'rust',
            '.cpp': 'cpp',
            '.c': 'c',
            '.h': 'c',
            '.cs': 'csharp',
            '.fs': 'fsharp',
            '.vb': 'vbnet'
        }
        return mapping.get(ext, 'unknown')
    
    @classmethod
    def get_test_framework(cls, language: str) -> str:
        """Get recommended test framework for language."""
        frameworks = {
            'python': 'pytest',
            'javascript': 'Jest',
            'typescript': 'Jest',
            'java': 'JUnit 5',
            'go': 'Go testing',
            'rust': 'Rust test',
            'cpp': 'Google Test',
            'c': 'Unity',
            'csharp': 'xUnit',
            'fsharp': 'xUnit',
            'vbnet': 'xUnit'
        }
        return frameworks.get(language, 'unit testing framework')
    
    @classmethod
    def find_test_files(cls, temp_dir: str, source_file: str) -> List[str]:
        """Find existing test files for a source file."""
        source_stem = Path(source_file).stem
        existing_tests = []
        
        test_patterns = [
            f"test_{source_stem}.py",
            f"{source_stem}_test.py",
            f"{source_stem}.test.py",
            f"{source_stem}.spec.py",
            f"{source_stem}_spec.py",
            f"{source_stem}.test.js",
            f"{source_stem}.spec.js"
        ]
        
        # Walk through the entire directory structure
        for root, _, files in os.walk(temp_dir):
            # Check if this is a test directory
            if cls._is_test_directory(root):
                # Look for matching test files
                for pattern in test_patterns:
                    matches = [f for f in files if f.lower() == pattern.lower()]
                    for match in matches:
                        test_path = os.path.join(root, match)
                        logger.info(f"Found test file {test_path} for {source_file}")
                        existing_tests.append(test_path)
        
        return existing_tests
    
    @classmethod
    def _is_test_directory(cls, directory_path: str) -> bool:
        """Check if directory is a test directory."""
        dir_name = os.path.basename(directory_path).lower()
        return any(pattern in dir_name for pattern in cls.TEST_PATTERNS)


class CodeParser:
    """Utility class for parsing code and extracting information."""
    
    @classmethod
    def extract_python_symbols(cls, code: str) -> Dict[str, List[str]]:
        """Extract functions and classes from Python code."""
        functions = []
        classes = []
        
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
                elif isinstance(node, ast.ClassDef):
                    classes.append(node.name)
        except SyntaxError as e:
            logger.warning(f"Failed to parse Python code: {e}")
        
        return {"functions": functions, "classes": classes}
    
    @classmethod
    def extract_javascript_symbols(cls, code: str) -> Dict[str, List[str]]:
        """Extract functions and classes from JavaScript/TypeScript code."""
        functions = []
        classes = []
        
        # Basic regex patterns for JS/TS
        function_patterns = [
            r'function\s+(\w+)',
            r'const\s+(\w+)\s*=\s*(?:function|\([^)]*\)\s*=>)',
            r'(\w+)\s*:\s*(?:function|\([^)]*\)\s*=>)',
        ]
        
        class_patterns = [
            r'class\s+(\w+)',
            r'interface\s+(\w+)',
        ]
        
        for pattern in function_patterns:
            functions.extend(re.findall(pattern, code))
        
        for pattern in class_patterns:
            classes.extend(re.findall(pattern, code))
        
        return {"functions": functions, "classes": classes}
    
    @classmethod
    def extract_symbols(cls, code: str, language: str) -> Dict[str, List[str]]:
        """Extract symbols (functions, classes) from code based on language."""
        if language == "python":
            return cls.extract_python_symbols(code)
        elif language in ("javascript", "typescript"):
            return cls.extract_javascript_symbols(code)
        elif language in ("csharp", "fsharp", "vbnet"):
            return cls.extract_dotnet_symbols(code, language)
        else:
            # Generic extraction for other languages
            functions = re.findall(r'function\s+(\w+)', code)
            classes = re.findall(r'class\s+(\w+)', code)
            return {"functions": functions, "classes": classes}
    
    @classmethod
    def extract_dotnet_symbols(cls, code: str, language: str) -> Dict[str, List[str]]:
        """Extract symbols from .NET code."""
        # Import here to avoid circular imports
        from .dotnet_utils import DotNetCodeParser
        return DotNetCodeParser.extract_dotnet_symbols(code, language)


class TemplateManager:
    """Manages prompt templates for AI interactions."""
    
    ANALYSIS_TEMPLATE = """You are an expert code analyzer. Analyze code for complexity, 
testability, and potential issues. Return structured analysis in JSON format.

Analyze this code file: {file_path}

Code:
```{language}
{code}
```

Provide analysis in JSON format with:
1. "complexity_score": 1-10 rating
2. "functions": list of function names that need testing
3. "classes": list of class names that need testing
4. "edge_cases": list of potential edge cases to test
5. "dependencies": external dependencies that need mocking
6. "test_scenarios": suggested test scenarios
7. "security_concerns": potential security issues
8. "performance_issues": performance optimization suggestions

Return only valid JSON."""
    
    TEST_GENERATION_TEMPLATE = """You are an expert test generator. Generate comprehensive, 
production-ready unit tests using {test_framework} for {language} code.

Generate complete unit tests for this {language} code:

File: {file_path}
Code:
```{language}
{code}
```

Analysis Context:
{analysis}

Requirements:
1. Use {test_framework} framework
2. Test all public functions from analysis
3. Include edge cases and error handling
4. Mock external dependencies
5. Add setup/teardown if needed
6. Use descriptive test names and assertions
7. Include both positive and negative test cases
8. Add performance tests if applicable

Generate ONLY the complete test file code, no explanations."""
    
    CODE_REVIEW_TEMPLATE = """You are a senior code reviewer. Provide specific, 
actionable suggestions for code improvement.

Review this code and suggest improvements:

File: {file_path}
```{language}
{code}
```

Focus on:
1. Code quality and readability
2. Performance optimizations
3. Security best practices
4. Error handling
5. Testability improvements

Provide 5-8 specific, actionable suggestions as a numbered list."""
