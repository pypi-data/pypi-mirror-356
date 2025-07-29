"""Test cases for core utilities."""

import pytest
import tempfile
import os
from pathlib import Path

from ghprai.core.utils import FileAnalyzer, CodeParser, TemplateManager
from ghprai.core.models import CodeAnalysis


class TestFileAnalyzer:
    """Test cases for FileAnalyzer utility."""
    
    def test_is_code_file(self):
        """Test code file detection."""
        assert FileAnalyzer.is_code_file("src/main.py")
        assert FileAnalyzer.is_code_file("app.js")
        assert FileAnalyzer.is_code_file("component.tsx")
        assert FileAnalyzer.is_code_file("MyClass.java")
        
        assert not FileAnalyzer.is_code_file("README.md")
        assert not FileAnalyzer.is_code_file("package.json")
        assert not FileAnalyzer.is_code_file("style.css")
    
    def test_is_test_file(self):
        """Test test file detection."""
        assert FileAnalyzer.is_test_file("test_main.py")
        assert FileAnalyzer.is_test_file("main_test.py")
        assert FileAnalyzer.is_test_file("main.test.js")
        assert FileAnalyzer.is_test_file("tests/test_utils.py")
        assert FileAnalyzer.is_test_file("__tests__/component.test.tsx")
        
        assert not FileAnalyzer.is_test_file("main.py")
        assert not FileAnalyzer.is_test_file("src/utils.js")
        assert not FileAnalyzer.is_test_file("lib/component.tsx")
    
    def test_is_source_file(self):
        """Test source file detection."""
        assert FileAnalyzer.is_source_file("src/main.py")
        assert FileAnalyzer.is_source_file("lib/utils.js")
        assert FileAnalyzer.is_source_file("app/component.tsx")
        
        assert not FileAnalyzer.is_source_file("test_main.py")
        assert not FileAnalyzer.is_source_file("tests/utils.py")
        assert not FileAnalyzer.is_source_file("README.md")
    
    def test_get_language(self):
        """Test language detection."""
        assert FileAnalyzer.get_language("main.py") == "python"
        assert FileAnalyzer.get_language("app.js") == "javascript"
        assert FileAnalyzer.get_language("component.ts") == "typescript"
        assert FileAnalyzer.get_language("Main.java") == "java"
        assert FileAnalyzer.get_language("main.go") == "go"
        assert FileAnalyzer.get_language("lib.rs") == "rust"
        assert FileAnalyzer.get_language("program.cpp") == "cpp"
        assert FileAnalyzer.get_language("header.h") == "c"
        assert FileAnalyzer.get_language("unknown.xyz") == "unknown"
    
    def test_get_test_framework(self):
        """Test test framework selection."""
        assert FileAnalyzer.get_test_framework("python") == "pytest"
        assert FileAnalyzer.get_test_framework("javascript") == "Jest"
        assert FileAnalyzer.get_test_framework("typescript") == "Jest"
        assert FileAnalyzer.get_test_framework("java") == "JUnit 5"
        assert FileAnalyzer.get_test_framework("go") == "Go testing"
        assert FileAnalyzer.get_test_framework("rust") == "Rust test"
        assert "testing" in FileAnalyzer.get_test_framework("unknown")
    
    def test_find_test_files(self):
        """Test finding test files in a directory structure."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create directory structure
            src_dir = Path(temp_dir) / "src"
            test_dir = Path(temp_dir) / "tests"
            src_dir.mkdir()
            test_dir.mkdir()
            
            # Create source file
            source_file = src_dir / "calculator.py"
            source_file.write_text("def add(a, b): return a + b")
            
            # Create corresponding test file
            test_file = test_dir / "test_calculator.py"
            test_file.write_text("def test_add(): pass")
            
            # Find test files
            found_tests = FileAnalyzer.find_test_files(temp_dir, "src/calculator.py")
            
            assert len(found_tests) == 1
            assert "test_calculator.py" in found_tests[0]


class TestCodeParser:
    """Test cases for CodeParser utility."""
    
    def test_extract_python_symbols(self):
        """Test Python symbol extraction."""
        code = """
def function1():
    pass

def function2(arg):
    return arg

class MyClass:
    def method1(self):
        pass

class AnotherClass:
    pass
"""
        
        symbols = CodeParser.extract_python_symbols(code)
        
        assert "function1" in symbols["functions"]
        assert "function2" in symbols["functions"]
        assert "MyClass" in symbols["classes"]
        assert "AnotherClass" in symbols["classes"]
        assert "method1" in symbols["functions"]  # Methods are also functions
    
    def test_extract_javascript_symbols(self):
        """Test JavaScript symbol extraction."""
        code = """
function regularFunction() {
    return true;
}

const arrowFunction = () => {
    return false;
};

class MyComponent {
    render() {
        return null;
    }
}

interface ApiResponse {
    data: any;
}
"""
        
        symbols = CodeParser.extract_javascript_symbols(code)
        
        assert "regularFunction" in symbols["functions"]
        assert "arrowFunction" in symbols["functions"]
        assert "MyComponent" in symbols["classes"]
        assert "ApiResponse" in symbols["classes"]
    
    def test_extract_python_symbols_with_syntax_error(self):
        """Test Python symbol extraction with syntax error."""
        code = "def invalid_syntax( return"
        
        symbols = CodeParser.extract_python_symbols(code)
        
        # Should return empty lists on syntax error
        assert symbols["functions"] == []
        assert symbols["classes"] == []
    
    def test_extract_symbols_unknown_language(self):
        """Test symbol extraction for unknown language."""
        code = """
function test() {
    return true;
}

class TestClass {
}
"""
        
        symbols = CodeParser.extract_symbols(code, "unknown")
        
        # Should fall back to generic regex
        assert "test" in symbols["functions"]
        assert "TestClass" in symbols["classes"]


class TestTemplateManager:
    """Test cases for TemplateManager."""
    
    def test_analysis_template_formatting(self):
        """Test analysis template formatting."""
        template = TemplateManager.ANALYSIS_TEMPLATE
        
        formatted = template.format(
            file_path="test.py",
            language="python",
            code="def test(): pass"
        )
        
        assert "test.py" in formatted
        assert "python" in formatted
        assert "def test(): pass" in formatted
        assert "complexity_score" in formatted
        assert "functions" in formatted
    
    def test_test_generation_template_formatting(self):
        """Test test generation template formatting."""
        template = TemplateManager.TEST_GENERATION_TEMPLATE
        
        formatted = template.format(
            test_framework="pytest",
            language="python",
            file_path="test.py",
            code="def add(a, b): return a + b",
            analysis='{"functions": ["add"]}'
        )
        
        assert "pytest" in formatted
        assert "python" in formatted
        assert "test.py" in formatted
        assert "def add(a, b): return a + b" in formatted
        assert "functions" in formatted
    
    def test_code_review_template_formatting(self):
        """Test code review template formatting."""
        template = TemplateManager.CODE_REVIEW_TEMPLATE
        
        formatted = template.format(
            file_path="test.py",
            language="python",
            code="def poorly_named_func(x): return x * 2"
        )
        
        assert "test.py" in formatted
        assert "python" in formatted
        assert "poorly_named_func" in formatted
        assert "Code quality" in formatted
        assert "Performance" in formatted
