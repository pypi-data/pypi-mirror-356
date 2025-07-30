"""GitHub Pull Request Agent for automated code review and testing."""

import os
import re
import logging
import tempfile
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

from github import Github, Auth
from github.PullRequest import PullRequest
from github.Repository import Repository

from .ai_agent import OllamaAIAgent
from ..core.config import Config
from ..core.models import TestCoverage, TestResult, PRAnalysisResult, GeneratedTest
from ..core.utils import FileAnalyzer
from ..core.dotnet_utils import DotNetAnalyzer

logger = logging.getLogger(__name__)


class GitHubPRAgent:
    """GitHub Pull Request Agent that integrates with Ollama for AI-powered code review."""
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize the GitHub PR Agent.
        
        Args:
            config: Configuration object. If None, loads from environment.
        """
        self.config = config or Config.from_env()
        auth = Auth.Token(self.config.github_token)
        self.github = Github(auth=auth)
        self.ai_agent = OllamaAIAgent(self.config)
        
        # Import here to avoid circular imports
        from .dotnet_agent import DotNetAIAgent
        self.dotnet_agent = DotNetAIAgent(self.config)
    
    def process_pr(self, payload: Dict) -> PRAnalysisResult:
        """Process a GitHub pull request webhook payload.
        
        Args:
            payload: GitHub webhook payload
            
        Returns:
            PRAnalysisResult with complete analysis
        """
        if payload['action'] != 'opened':
            return PRAnalysisResult(
                pr_number=0,
                repository="",
                changed_files=[],
                coverage=TestCoverage(),
                status="ignored"
            )
        
        pr = payload['pull_request']
        repo_name = payload['repository']['full_name']
        pr_number = pr['number']
        
        logger.info(f"🤖 Processing PR #{pr_number} in {repo_name}")
        
        try:
            repo = self.github.get_repo(repo_name)
            pr_obj = repo.get_pull(pr_number)
            
            with tempfile.TemporaryDirectory() as temp_dir:
                self._clone_repo(repo, pr_obj, temp_dir)
                
                # Get changed files
                changed_files = self._get_changed_files(pr_obj)
                if not changed_files:
                    return PRAnalysisResult(
                        pr_number=pr_number,
                        repository=repo_name,
                        changed_files=[],
                        coverage=TestCoverage(),
                        status="skipped"
                    )
                
                # Analyze test coverage
                coverage = self._analyze_test_coverage(temp_dir, changed_files)
                
                # Generate new tests for files without coverage
                generated_tests = self._generate_missing_tests(temp_dir, coverage, changed_files)
                
                # Run tests
                test_results = self._run_tests(temp_dir, coverage, generated_tests)
                coverage.test_results = test_results
                
                # Create new branch for tests if any generated
                new_branch = None
                if generated_tests:
                    new_branch = self._commit_tests(repo, pr_obj, generated_tests, temp_dir)
                
                # Generate analysis report
                report = self._generate_report(coverage, generated_tests, new_branch, temp_dir)
                
                # Post report to PR
                pr_obj.create_issue_comment(report)
                
                return PRAnalysisResult(
                    pr_number=pr_number,
                    repository=repo_name,
                    changed_files=changed_files,
                    coverage=coverage,
                    generated_tests=generated_tests,
                    new_branch=new_branch,
                    report=report,
                    status="completed"
                )
                
        except Exception as e:
            logger.error(f"Error processing PR: {e}")
            return PRAnalysisResult(
                pr_number=pr_number,
                repository=repo_name,
                changed_files=[],
                coverage=TestCoverage(),
                status="failed",
                error_message=str(e)
            )
    
    def _get_changed_files(self, pr: PullRequest) -> List[str]:
        """Get list of changed source code files (excluding tests).
        
        Args:
            pr: GitHub PullRequest object
            
        Returns:
            List of changed source file paths
        """
        changed_files = []
        
        for file in pr.get_files():
            if FileAnalyzer.is_source_file(file.filename) or DotNetAnalyzer.is_dotnet_source_only_file(file.filename):
                changed_files.append(file.filename)
        
        return changed_files
    
    def _analyze_test_coverage(self, temp_dir: str, changed_files: List[str]) -> TestCoverage:
        """Analyze test coverage for changed files.
        
        Args:
            temp_dir: Temporary directory with cloned repo
            changed_files: List of changed source files
            
        Returns:
            TestCoverage object with analysis results
        """
        coverage = TestCoverage()
        
        for file_path in changed_files:
            full_path = os.path.join(temp_dir, file_path)
            if not os.path.exists(full_path):
                continue
            
            logger.info(f"Analyzing test coverage for {file_path}")
            coverage.total_files += 1
            
            # Determine if this is a .NET file
            is_dotnet_file = DotNetAnalyzer.is_dotnet_source_file(file_path)
            
            # Find existing tests
            if is_dotnet_file:
                existing_tests = DotNetAnalyzer.find_test_files_for_source(temp_dir, file_path)
            else:
                existing_tests = FileAnalyzer.find_test_files(temp_dir, file_path)
            
            # Read and analyze source file
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                source_code = f.read()
            
            # Get AI analysis based on file type
            if is_dotnet_file:
                # Find project context for .NET files
                project_path = self.dotnet_agent.find_dotnet_project_context(full_path, temp_dir)
                analysis = self.dotnet_agent.analyze_dotnet_code_intelligence(source_code, file_path, project_path)
            else:
                analysis = self.ai_agent.analyze_code_intelligence(source_code, file_path)
            coverage.source_files[file_path] = analysis
            
            # Update statistics
            coverage.total_functions += len(analysis.functions)
            coverage.total_classes += len(analysis.classes)
            
            if existing_tests:
                coverage.test_files[file_path] = existing_tests
                coverage.files_with_tests += 1
                
                # Analyze test coverage
                covered_functions, covered_classes = self._analyze_existing_tests(
                    existing_tests, analysis
                )
                coverage.covered_functions += len(covered_functions)
                coverage.covered_classes += len(covered_classes)
            else:
                coverage.missing_tests.append(file_path)
        
        return coverage
    
    def _analyze_existing_tests(self, test_files: List[str], analysis) -> tuple:
        """Analyze existing test files to determine coverage.
        
        Args:
            test_files: List of test file paths
            analysis: Code analysis results
            
        Returns:
            Tuple of (covered_functions, covered_classes) as sets
        """
        covered_functions = set()
        covered_classes = set()
        
        for test_file in test_files:
            try:
                with open(test_file, 'r', encoding='utf-8', errors='ignore') as f:
                    test_code = f.read()
                
                # Check which functions/classes are covered
                for func in analysis.functions:
                    if func in test_code:
                        covered_functions.add(func)
                
                for cls in analysis.classes:
                    if cls in test_code:
                        covered_classes.add(cls)
                        
            except Exception as e:
                logger.error(f"Error analyzing test file {test_file}: {e}")
        
        return covered_functions, covered_classes
    
    def _generate_missing_tests(self, temp_dir: str, coverage: TestCoverage, changed_files: List[str]) -> List[GeneratedTest]:
        """Generate tests for files missing test coverage.
        
        Args:
            temp_dir: Temporary directory with cloned repo
            coverage: Current test coverage analysis
            changed_files: List of changed source files
            
        Returns:
            List of GeneratedTest objects
        """
        generated_tests = []
        
        for file_path in coverage.missing_tests:
            if file_path not in changed_files:
                continue
            
            full_path = os.path.join(temp_dir, file_path)
            if not os.path.exists(full_path):
                continue
            
            logger.info(f"Generating tests for {file_path}")
            
            with open(full_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            analysis = coverage.source_files[file_path]
            
            # Generate tests based on file type
            is_dotnet_file = DotNetAnalyzer.is_dotnet_source_file(file_path)
            if is_dotnet_file:
                # Find project context for .NET files
                project_path = self.dotnet_agent.find_dotnet_project_context(full_path, temp_dir)
                generated_test = self.dotnet_agent.generate_dotnet_tests(code, file_path, analysis, project_path)
            else:
                generated_test = self.ai_agent.generate_intelligent_tests(code, file_path, analysis)
            
            if generated_test:
                generated_tests.append(generated_test)
        
        return generated_tests
    
    def _run_tests(self, temp_dir: str, coverage: TestCoverage, generated_tests: List[GeneratedTest]) -> TestResult:
        """Run existing and generated tests.
        
        Args:
            temp_dir: Temporary directory with cloned repo
            coverage: Test coverage information
            generated_tests: List of generated tests
            
        Returns:
            TestResult object with execution results
        """
        all_test_files = []
        
        # Add existing test files
        for test_files in coverage.test_files.values():
            all_test_files.extend(test_files)
        
        # Write and add generated test files
        tests_dir = Path(temp_dir) / "tests"
        tests_dir.mkdir(exist_ok=True)
        
        for gen_test in generated_tests:
            test_path = tests_dir / gen_test.test_file
            # Create parent directories and file if they don't exist
            test_path.parent.mkdir(parents=True, exist_ok=True)
            if not test_path.exists():
                test_path.touch()  # Creates empty file
            with open(test_path, 'w', encoding='utf-8') as f:
                f.write(gen_test.test_content)
            all_test_files.append(str(test_path))
        
        if not all_test_files:
            return TestResult(status="not_run")
        
        try:
            # Determine test command based on file types
            if any(f.endswith('.py') for f in all_test_files):
                cmd = ['pytest'] + all_test_files
            elif any(f.endswith(('.js', '.ts')) for f in all_test_files):
                cmd = ['npm', 'test', '--'] + all_test_files
            elif any(f.endswith('.cs') for f in all_test_files):
                # For .NET tests, try to find and run the test project
                dotnet_projects = DotNetAnalyzer.find_dotnet_projects(temp_dir)
                test_projects = [p for p in dotnet_projects if self._is_test_project(p)]
                if test_projects:
                    cmd = ['dotnet', 'test', test_projects[0]]
                else:
                    # Fallback to building and running tests
                    cmd = ['dotnet', 'test']
            else:
                return TestResult(status="not_run")
            
            result = subprocess.run(
                cmd, 
                cwd=temp_dir, 
                capture_output=True, 
                text=True, 
                timeout=60
            )
            
            output = result.stdout + result.stderr
            status = "passed" if result.returncode == 0 else "failed"
            
            # Parse basic metrics
            passed = len(re.findall(r'passed', output.lower()))
            failed = len(re.findall(r'failed', output.lower()))
            
            return TestResult(
                status=status,
                output=output,
                passed=passed,
                failed=failed,
                test_files=all_test_files
            )
            
        except Exception as e:
            return TestResult(
                status="error",
                output=str(e),
                test_files=all_test_files
            )
    
    def _commit_tests(self, repo: Repository, pr: PullRequest, generated_tests: List[GeneratedTest], temp_dir: str) -> Optional[str]:
        """Commit generated tests to a new branch.
        
        Args:
            repo: GitHub Repository object
            pr: PullRequest object
            generated_tests: List of generated tests
            temp_dir: Temporary directory
            
        Returns:
            New branch name or None if failed
        """
        if not generated_tests:
            return None
        
        logger.info(f"📝 Creating new branch and committing {len(generated_tests)} new test files...")
        
        # Create tests directory
        tests_dir = Path(temp_dir) / "tests"
        tests_dir.mkdir(exist_ok=True)
        
        # Create a new branch for tests
        import time
        timestamp = str(int(time.time()))
        new_branch = f"ai-tests-{timestamp}"
        
        try:
            # Create and checkout new branch
            subprocess.run(['git', 'checkout', '-b', new_branch], cwd=temp_dir, check=True)
            
            # Write test files
            for gen_test in generated_tests:
                test_path = tests_dir / gen_test.test_file
                with open(test_path, 'w', encoding='utf-8') as f:
                    f.write(gen_test.test_content)
            
            # Git operations
            subprocess.run(['git', 'add', 'tests/'], cwd=temp_dir, check=True)
            subprocess.run([
                'git', 'commit', '-m', 
                f"🤖 AI-generated tests for PR #{pr.number}\n\nGenerated by GitHub PR AI Agent"
            ], cwd=temp_dir, check=True)
            
            # Push new branch
            subprocess.run(['git', 'push', 'origin', new_branch], cwd=temp_dir, check=True)
            
            return new_branch
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to commit tests: {e}")
            return None
    
    def _generate_report(self, coverage: TestCoverage, generated_tests: List[GeneratedTest], new_branch: Optional[str], temp_dir: str) -> str:
        """Generate comprehensive analysis report.
        
        Args:
            coverage: Test coverage analysis
            generated_tests: List of generated tests
            new_branch: New branch name if tests were committed
            temp_dir: Temporary directory
            
        Returns:
            Formatted report string
        """
        report = []
        
        # Header
        report.append("# 🤖 AI Agent Analysis Report\n")
        report.append(f"*Powered by Ollama with {self.config.ollama_model}*\n\n")
        
        # Test Coverage Summary
        report.append("## 📊 Test Coverage Analysis\n\n")
        report.append("### Overall Coverage\n")
        report.append(f"- **File Coverage**: {coverage.file_coverage_percent:.1f}% ({coverage.files_with_tests}/{coverage.total_files} files)\n")
        report.append(f"- **Function Coverage**: {coverage.function_coverage_percent:.1f}% ({coverage.covered_functions}/{coverage.total_functions} functions)\n")
        report.append(f"- **Class Coverage**: {coverage.class_coverage_percent:.1f}% ({coverage.covered_classes}/{coverage.total_classes} classes)\n\n")
        
        # Files with Tests
        if coverage.test_files:
            report.append("### 📝 Files with Existing Tests\n")
            for source_file, test_files in coverage.test_files.items():
                report.append(f"\n**{source_file}**\n")
                for test_file in test_files:
                    report.append(f"- `{os.path.relpath(test_file, temp_dir)}`\n")
            report.append("\n")
        
        # Missing Tests
        if coverage.missing_tests:
            report.append("## ⚠️ Missing Test Coverage\n\n")
            for file_path in coverage.missing_tests:
                if file_path in coverage.source_files:
                    analysis = coverage.source_files[file_path]
                    report.append(f"### `{file_path}`\n")
                    if analysis.functions:
                        report.append("**Untested Functions:**\n")
                        for func in analysis.functions:
                            report.append(f"- `{func}`\n")
                    if analysis.classes:
                        report.append("**Untested Classes:**\n")
                        for cls in analysis.classes:
                            report.append(f"- `{cls}`\n")
                    report.append("\n")
        
        # New Tests Generated
        if generated_tests:
            report.append("## ✨ New Tests Generated\n\n")
            if new_branch:
                report.append(f"Generated tests have been pushed to branch `{new_branch}`\n\n")
                report.append("To review and merge these tests:\n")
                report.append("```bash\n")
                report.append(f"git fetch origin {new_branch}\n")
                report.append(f"git checkout {new_branch}\n")
                report.append("```\n\n")
            
            for gen_test in generated_tests:
                report.append(f"- **{gen_test.source_file}** → `{gen_test.test_file}` ({gen_test.framework})\n")
            report.append("\n")
        
        # Test Results
        if coverage.test_results:
            report.append("## 🧪 Test Execution Results\n\n")
            test_results = coverage.test_results
            status_emoji = "✅" if test_results.status == "passed" else "❌"
            report.append(f"{status_emoji} Status: {test_results.status}\n")
            report.append(f"- Passed: {test_results.passed}\n")
            report.append(f"- Failed: {test_results.failed}\n\n")
            
            if test_results.output:
                report.append("<details><summary>Test Output</summary>\n\n```\n")
                report.append(test_results.output)
                report.append("\n```\n</details>\n\n")
        
        # Footer
        report.append("---\n")
        report.append("*This analysis was generated by GitHub PR AI Agent using local LLM via Ollama*")
        
        # Join and truncate if needed
        final_report = "".join(report)
        if len(final_report) > 65000:
            final_report = final_report[:65000] + "\n\n*[Report truncated due to length]*"
        
        return final_report
    
    def _is_test_project(self, project_path: str) -> bool:
        """Check if a .NET project file is a test project.
        
        Args:
            project_path: Path to the .csproj/.fsproj file
            
        Returns:
            True if it's a test project, False otherwise
        """
        project_info = DotNetAnalyzer.get_project_info(project_path)
        return project_info.get('project_type') == 'test' or len(project_info.get('test_frameworks', [])) > 0

    def _clone_repo(self, repo: Repository, pr: PullRequest, temp_dir: str) -> None:
        """Clone PR branch to temp directory.
        
        Args:
            repo: GitHub Repository object
            pr: PullRequest object
            temp_dir: Temporary directory path
        """
        clone_url = repo.clone_url
        branch = pr.head.ref
        
        subprocess.run([
            'git', 'clone', 
            '--branch', branch,
            '--single-branch', '--depth', '1',
            clone_url, temp_dir
        ], check=True)
