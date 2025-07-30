"""Data models for GitHub PR AI Agent."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from pathlib import Path


@dataclass
class CodeAnalysis:
    """Result of AI code analysis."""
    
    file_path: str
    complexity_score: float
    functions: List[str] = field(default_factory=list)
    classes: List[str] = field(default_factory=list)
    edge_cases: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    test_scenarios: List[str] = field(default_factory=list)
    security_concerns: List[str] = field(default_factory=list)
    performance_issues: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    
    @property
    def needs_tests(self) -> bool:
        """Check if this code needs test coverage."""
        return bool(self.functions or self.classes)
    
    @property
    def risk_level(self) -> str:
        """Determine risk level based on complexity and issues."""
        if self.complexity_score >= 8 or self.security_concerns:
            return "high"
        elif self.complexity_score >= 5 or self.performance_issues:
            return "medium"
        else:
            return "low"


@dataclass
class TestResult:
    """Result of test execution."""
    
    status: str  # "passed", "failed", "error", "not_run"
    output: str = ""
    passed: int = 0
    failed: int = 0
    duration: float = 0.0
    test_files: List[str] = field(default_factory=list)


@dataclass
class TestCoverage:
    """Test coverage information for a file or project."""
    
    source_files: Dict[str, CodeAnalysis] = field(default_factory=dict)
    test_files: Dict[str, List[str]] = field(default_factory=dict)  # source -> test files
    missing_tests: List[str] = field(default_factory=list)
    test_results: Optional[TestResult] = None
    
    # Coverage statistics
    total_files: int = 0
    files_with_tests: int = 0
    total_functions: int = 0
    covered_functions: int = 0
    total_classes: int = 0
    covered_classes: int = 0
    
    @property
    def file_coverage_percent(self) -> float:
        """Calculate file coverage percentage."""
        if self.total_files == 0:
            return 0.0
        return (self.files_with_tests / self.total_files) * 100
    
    @property
    def function_coverage_percent(self) -> float:
        """Calculate function coverage percentage."""
        if self.total_functions == 0:
            return 0.0
        return (self.covered_functions / self.total_functions) * 100
    
    @property
    def class_coverage_percent(self) -> float:
        """Calculate class coverage percentage."""
        if self.total_classes == 0:
            return 0.0
        return (self.covered_classes / self.total_classes) * 100


@dataclass
class GeneratedTest:
    """Information about a generated test."""
    
    source_file: str
    test_file: str
    test_content: str
    framework: str
    language: str


@dataclass
class PRAnalysisResult:
    """Complete analysis result for a pull request."""
    
    pr_number: int
    repository: str
    changed_files: List[str]
    coverage: TestCoverage
    generated_tests: List[GeneratedTest] = field(default_factory=list)
    new_branch: Optional[str] = None
    report: str = ""
    status: str = "pending"  # "pending", "completed", "failed"
    error_message: Optional[str] = None
