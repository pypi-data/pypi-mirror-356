"""DotNet-specific utilities for code analysis and test generation."""

import os
import re
import xml.etree.ElementTree as ET
import logging
from pathlib import Path
from typing import List, Set, Dict, Optional, Tuple

logger = logging.getLogger(__name__)


class DotNetAnalyzer:
    """Utility class for analyzing .NET projects and solutions."""
    
    # .NET file extensions
    DOTNET_EXTENSIONS = {'.cs', '.fs', '.vb', '.csproj', '.fsproj', '.vbproj', '.sln'}
    
    # C# specific extensions
    CSHARP_EXTENSIONS = {'.cs'}
    
    # F# specific extensions  
    FSHARP_EXTENSIONS = {'.fs'}
    
    # VB.NET specific extensions
    VBNET_EXTENSIONS = {'.vb'}
    
    # Project file extensions
    PROJECT_EXTENSIONS = {'.csproj', '.fsproj', '.vbproj'}
    
    # Solution file extensions
    SOLUTION_EXTENSIONS = {'.sln'}
    
    # Common .NET source folder patterns
    DOTNET_SOURCE_FOLDERS = {'src', 'source', 'lib', 'libraries', 'core', 'shared', 'common'}
    
    # Common .NET test folder patterns
    DOTNET_TEST_FOLDERS = {'test', 'tests', 'testing', 'specs', 'unit', 'integration', 'functional'}
    
    # Common .NET test file patterns
    DOTNET_TEST_PATTERNS = {
        'test', 'tests', 'spec', 'specs', 'unittest', 'integrationtest',
        '.test', '.tests', '.spec', '.specs', 'test_', '_test', '_tests'
    }
    
    @classmethod
    def is_dotnet_file(cls, file_path: str) -> bool:
        """Check if file is a .NET file."""
        return Path(file_path).suffix.lower() in cls.DOTNET_EXTENSIONS
    
    @classmethod
    def is_dotnet_source_file(cls, file_path: str) -> bool:
        """Check if file is a .NET source code file (not project/solution)."""
        ext = Path(file_path).suffix.lower()
        return ext in (cls.CSHARP_EXTENSIONS | cls.FSHARP_EXTENSIONS | cls.VBNET_EXTENSIONS)
    
    @classmethod
    def is_dotnet_project_file(cls, file_path: str) -> bool:
        """Check if file is a .NET project file."""
        return Path(file_path).suffix.lower() in cls.PROJECT_EXTENSIONS
    
    @classmethod
    def is_dotnet_solution_file(cls, file_path: str) -> bool:
        """Check if file is a .NET solution file."""
        return Path(file_path).suffix.lower() in cls.SOLUTION_EXTENSIONS
    
    @classmethod
    def is_dotnet_test_file(cls, file_path: str) -> bool:
        """Check if file is a .NET test file."""
        if not cls.is_dotnet_source_file(file_path):
            return False
            
        file_path_obj = Path(file_path)
        path_parts = file_path_obj.parts
        file_name = file_path_obj.name.lower()
        
        # Check filename patterns
        if any(pattern in file_name for pattern in cls.DOTNET_TEST_PATTERNS):
            return True
            
        # Check directory patterns
        if any(pattern in part.lower() for part in path_parts for pattern in cls.DOTNET_TEST_FOLDERS):
            return True
            
        return False
    
    @classmethod
    def is_dotnet_source_only_file(cls, file_path: str) -> bool:
        """Check if file is a .NET source file (not test)."""
        if not cls.is_dotnet_source_file(file_path):
            return False
            
        if cls.is_dotnet_test_file(file_path):
            return False
            
        return True
    
    @classmethod
    def get_dotnet_language(cls, file_path: str) -> str:
        """Get .NET programming language from file extension."""
        ext = Path(file_path).suffix.lower()
        mapping = {
            '.cs': 'csharp',
            '.fs': 'fsharp', 
            '.vb': 'vbnet'
        }
        return mapping.get(ext, 'unknown')
    
    @classmethod
    def get_dotnet_test_framework(cls, language: str, project_path: str = None) -> str:
        """Get recommended test framework for .NET language."""
        # Try to detect from project file if provided
        if project_path and cls.is_dotnet_project_file(project_path):
            detected_framework = cls._detect_test_framework_from_project(project_path)
            if detected_framework:
                return detected_framework
        
        # Default frameworks by language
        frameworks = {
            'csharp': 'xUnit',
            'fsharp': 'xUnit', 
            'vbnet': 'xUnit'
        }
        return frameworks.get(language, 'xUnit')
    
    @classmethod
    def find_dotnet_projects(cls, directory: str) -> List[str]:
        """Find all .NET project files in directory tree."""
        projects = []
        for root, _, files in os.walk(directory):
            for file in files:
                if cls.is_dotnet_project_file(file):
                    projects.append(os.path.join(root, file))
        return projects
    
    @classmethod
    def find_dotnet_solutions(cls, directory: str) -> List[str]:
        """Find all .NET solution files in directory tree."""
        solutions = []
        for root, _, files in os.walk(directory):
            for file in files:
                if cls.is_dotnet_solution_file(file):
                    solutions.append(os.path.join(root, file))
        return solutions
    
    @classmethod
    def get_project_info(cls, project_path: str) -> Dict[str, any]:
        """Extract information from .NET project file."""
        if not cls.is_dotnet_project_file(project_path):
            return {}
            
        try:
            tree = ET.parse(project_path)
            root = tree.getroot()
            
            info = {
                'target_framework': None,
                'project_type': None,
                'package_references': [],
                'test_frameworks': [],
                'output_type': None
            }
            
            # Extract TargetFramework
            target_framework = root.find('.//TargetFramework')
            if target_framework is not None:
                info['target_framework'] = target_framework.text
            
            # Extract OutputType
            output_type = root.find('.//OutputType')
            if output_type is not None:
                info['output_type'] = output_type.text
                
            # Extract PackageReferences
            for package_ref in root.findall('.//PackageReference'):
                include = package_ref.get('Include')
                version = package_ref.get('Version')
                if include:
                    info['package_references'].append({
                        'name': include,
                        'version': version
                    })
                    
                    # Detect test frameworks
                    if include.lower() in ['xunit', 'xunit.runner.visualstudio']:
                        info['test_frameworks'].append('xUnit')
                    elif include.lower() in ['nunit', 'nunit3testadapter']:
                        info['test_frameworks'].append('NUnit')
                    elif include.lower() in ['mstest.testframework', 'mstest.testadapter']:
                        info['test_frameworks'].append('MSTest')
            
            # Determine project type
            if info['test_frameworks']:
                info['project_type'] = 'test'
            elif info['output_type'] and info['output_type'].lower() == 'exe':
                info['project_type'] = 'console'
            elif info['output_type'] and info['output_type'].lower() == 'library':
                info['project_type'] = 'library'
            else:
                info['project_type'] = 'unknown'
                
            return info
            
        except Exception as e:
            logger.warning(f"Failed to parse project file {project_path}: {e}")
            return {}
    
    @classmethod
    def find_test_files_for_source(cls, temp_dir: str, source_file: str) -> List[str]:
        """Find existing test files for a .NET source file."""
        source_path = Path(source_file)
        source_stem = source_path.stem
        source_ext = source_path.suffix
        
        existing_tests = []
        
        # Common .NET test naming patterns
        test_patterns = [
            f"{source_stem}Test{source_ext}",
            f"{source_stem}Tests{source_ext}",
            f"{source_stem}Spec{source_ext}",
            f"{source_stem}Specs{source_ext}",
            f"Test{source_stem}{source_ext}",
            f"Tests{source_stem}{source_ext}",
            f"{source_stem}UnitTest{source_ext}",
            f"{source_stem}UnitTests{source_ext}"
        ]
        
        # Walk through the entire directory structure
        for root, _, files in os.walk(temp_dir):
            # Check if this is a test directory
            if cls._is_dotnet_test_directory(root):
                # Look for matching test files
                for pattern in test_patterns:
                    matches = [f for f in files if f.lower() == pattern.lower()]
                    for match in matches:
                        test_path = os.path.join(root, match)
                        logger.info(f"Found test file {test_path} for {source_file}")
                        existing_tests.append(test_path)
        
        return existing_tests
    
    @classmethod
    def get_test_file_path(cls, source_file: str, test_directory: str = None) -> str:
        """Generate appropriate test file path for a .NET source file."""
        source_path = Path(source_file)
        
        # Default test file name
        test_name = f"{source_path.stem}Tests{source_path.suffix}"
        
        if test_directory:
            return os.path.join(test_directory, test_name)
        else:
            # Place in Tests subdirectory relative to source
            source_dir = source_path.parent
            test_dir = source_dir / "Tests"
            return str(test_dir / test_name)
    
    @classmethod
    def _detect_test_framework_from_project(cls, project_path: str) -> Optional[str]:
        """Detect test framework from project file."""
        project_info = cls.get_project_info(project_path)
        test_frameworks = project_info.get('test_frameworks', [])
        
        if 'xUnit' in test_frameworks:
            return 'xUnit'
        elif 'NUnit' in test_frameworks:
            return 'NUnit'
        elif 'MSTest' in test_frameworks:
            return 'MSTest'
        
        return None
    
    @classmethod
    def _is_dotnet_test_directory(cls, directory_path: str) -> bool:
        """Check if directory is a .NET test directory."""
        dir_name = os.path.basename(directory_path).lower()
        return any(pattern in dir_name for pattern in cls.DOTNET_TEST_FOLDERS)


class DotNetCodeParser:
    """Utility class for parsing .NET code and extracting information."""
    
    @classmethod
    def extract_csharp_symbols(cls, code: str) -> Dict[str, List[str]]:
        """Extract classes, methods, and properties from C# code."""
        symbols = {
            'classes': [],
            'interfaces': [],
            'methods': [],
            'properties': [],
            'namespaces': []
        }
        
        try:
            # Namespace pattern - simple and reliable
            namespace_pattern = r'namespace\s+([A-Za-z_][\w.]*)'
            symbols['namespaces'] = re.findall(namespace_pattern, code)
            
            # Class pattern - simplified to catch most cases
            class_pattern = r'class\s+([A-Za-z_]\w*)'
            symbols['classes'] = re.findall(class_pattern, code)
            
            # Interface pattern
            interface_pattern = r'interface\s+([A-Za-z_]\w*)'
            symbols['interfaces'] = re.findall(interface_pattern, code)
            
            # Method pattern - improved to handle async and different return types
            method_pattern = r'(?:public|private|protected|internal)\s+(?:static\s+)?(?:virtual\s+|override\s+|abstract\s+)?(?:async\s+)?(?:\w+\s+|Task\s*<\w+>\s+|Task\s+)([A-Za-z_]\w*)\s*\('
            symbols['methods'] = re.findall(method_pattern, code)
            
            # Property pattern - simplified
            property_pattern = r'(?:public|private|protected|internal)\s+(?:static\s+)?\w+\s+([A-Za-z_]\w*)\s*{'
            symbols['properties'] = re.findall(property_pattern, code)
            
            # Remove duplicates while preserving order
            for key in symbols:
                symbols[key] = list(dict.fromkeys(symbols[key]))
                
        except Exception as e:
            logger.warning(f"Failed to parse C# code: {e}")
        
        return symbols
    
    @classmethod
    def extract_fsharp_symbols(cls, code: str) -> Dict[str, List[str]]:
        """Extract modules, functions, and types from F# code."""
        symbols = {
            'modules': [],
            'functions': [],
            'types': [],
            'values': []
        }
        
        try:
            # Module pattern
            module_pattern = r'module\s+([A-Za-z_]\w*)'
            symbols['modules'] = re.findall(module_pattern, code)
            
            # Function patterns (simplified)
            function_patterns = [
                r'let\s+([A-Za-z_]\w*)\s+\w+',  # let funcName param 
                r'let\s+rec\s+([A-Za-z_]\w*)\s+\w+',  # let rec funcName param
            ]
            
            for pattern in function_patterns:
                symbols['functions'].extend(re.findall(pattern, code))
            
            # Type pattern
            type_pattern = r'type\s+([A-Za-z_]\w*)'
            symbols['types'] = re.findall(type_pattern, code)
            
            # Value pattern (let bindings without parameters)
            value_pattern = r'let\s+([A-Za-z_]\w*)\s*='
            potential_values = re.findall(value_pattern, code)
            
            # Filter out functions that were already captured
            for val in potential_values:
                if val not in symbols['functions']:
                    symbols['values'].append(val)
            
            # Remove duplicates while preserving order
            for key in symbols:
                symbols[key] = list(dict.fromkeys(symbols[key]))
                
        except Exception as e:
            logger.warning(f"Failed to parse F# code: {e}")
        
        return symbols
    
    @classmethod
    def extract_dotnet_symbols(cls, code: str, language: str) -> Dict[str, List[str]]:
        """Extract symbols from .NET code based on language."""
        if language == "csharp":
            return cls.extract_csharp_symbols(code)
        elif language == "fsharp":
            return cls.extract_fsharp_symbols(code)
        elif language == "vbnet":
            # For VB.NET, use basic patterns for now
            symbols = {
                'classes': re.findall(r'Class\s+([A-Za-z_][A-Za-z0-9_]*)', code, re.IGNORECASE),
                'methods': re.findall(r'(?:Public|Private|Protected|Friend)?\s*(?:Sub|Function)\s+([A-Za-z_][A-Za-z0-9_]*)', code, re.IGNORECASE),
                'properties': []
            }
            return symbols
        else:
            return {'classes': [], 'methods': [], 'properties': []}


class DotNetTemplateManager:
    """Manages .NET-specific prompt templates for AI interactions."""
    
    DOTNET_ANALYSIS_TEMPLATE = """You are an expert .NET code analyzer. Analyze C#/F#/VB.NET code for complexity, 
testability, and potential issues. Return structured analysis in JSON format.

Analyze this .NET code file: {file_path}
Language: {language}
Target Framework: {target_framework}

Code:
```{language}
{code}
```

Provide analysis in JSON format with:
1. "complexity_score": 1-10 rating
2. "classes": list of class names that need testing
3. "interfaces": list of interface names
4. "methods": list of method names that need testing  
5. "properties": list of property names that need testing
6. "edge_cases": list of potential edge cases to test
7. "dependencies": external dependencies that need mocking
8. "test_scenarios": suggested test scenarios
9. "security_concerns": potential security issues (SQL injection, XSS, etc.)
10. "performance_issues": performance optimization suggestions
11. "dotnet_specific_issues": .NET-specific concerns (disposal, async/await, etc.)

Return only valid JSON."""
    
    DOTNET_TEST_GENERATION_TEMPLATE = """You are an expert .NET test generator. Generate comprehensive, 
production-ready unit tests using {test_framework} for {language} code.

Generate complete unit tests for this {language} code:

File: {file_path}
Target Framework: {target_framework}
Test Framework: {test_framework}

Code:
```{language}
{code}
```

Analysis Context:
{analysis}

Requirements:
1. Use {test_framework} framework with proper attributes
2. Test all public classes, methods, and properties from analysis
3. Include edge cases and error handling tests
4. Mock external dependencies using appropriate .NET mocking frameworks
5. Add setup/teardown methods if needed (Constructor/Dispose for xUnit, SetUp/TearDown for NUnit)
6. Use descriptive test method names following .NET conventions
7. Include both positive and negative test cases
8. Add async test methods for async code
9. Test exception scenarios with proper exception assertions
10. Include performance tests if applicable
11. Use appropriate assertions for the test framework
12. Follow .NET naming conventions and best practices

Generate ONLY the complete test file code with proper using statements, no explanations."""
    
    DOTNET_CODE_REVIEW_TEMPLATE = """You are a senior .NET code reviewer. Provide specific, 
actionable suggestions for .NET code improvement.

Review this {language} code and suggest improvements:

File: {file_path}
Target Framework: {target_framework}

```{language}
{code}
```

Focus on:
1. .NET-specific best practices and conventions
2. Performance optimizations (async/await, LINQ, collections)
3. Security best practices (input validation, SQL injection prevention)
4. Memory management and disposal patterns
5. Exception handling and error scenarios
6. Testability and dependency injection
7. Code readability and maintainability
8. Framework-specific optimizations

Provide 5-8 specific, actionable suggestions as a numbered list."""
