"""Command line interface for GitHub PR AI Agent."""

import os
import sys
import argparse
import logging
from pathlib import Path
from typing import List, Optional

from .agents.ai_agent import OllamaAIAgent
from .agents.github_agent import GitHubPRAgent
from .core.config import Config
from .core.utils import FileAnalyzer

logger = logging.getLogger(__name__)


def setup_logging(verbose: bool = False):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def analyze_repository(repo_path: str, config: Config) -> None:
    """Analyze a local repository for code quality and test coverage.
    
    Args:
        repo_path: Path to the repository
        config: Configuration object
    """
    if not os.path.exists(repo_path):
        print(f"Error: Repository path '{repo_path}' does not exist")
        sys.exit(1)
    
    print(f"🔍 Analyzing repository: {repo_path}")
    
    # Initialize AI agent
    ai_agent = OllamaAIAgent(config)
    
    # Find all source files
    source_files = []
    for root, dirs, files in os.walk(repo_path):
        # Skip hidden directories and common build directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'build', 'dist']]
        
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, repo_path)
            
            if FileAnalyzer.is_source_file(rel_path):
                source_files.append(file_path)
    
    if not source_files:
        print("No source files found to analyze")
        return
    
    print(f"Found {len(source_files)} source files")
    
    # Analyze each file
    total_complexity = 0
    total_files = 0
    files_with_tests = 0
    high_risk_files = []
    
    for file_path in source_files:
        rel_path = os.path.relpath(file_path, repo_path)
        print(f"  📄 Analyzing {rel_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                code = f.read()
            
            analysis = ai_agent.analyze_code_intelligence(code, rel_path)
            
            total_complexity += analysis.complexity_score
            total_files += 1
            
            # Check for existing tests
            existing_tests = FileAnalyzer.find_test_files(repo_path, rel_path)
            if existing_tests:
                files_with_tests += 1
                print(f"    ✅ Has tests: {len(existing_tests)} test files")
            else:
                print(f"    ⚠️  No tests found")
            
            # Check risk level
            if analysis.risk_level == "high":
                high_risk_files.append((rel_path, analysis))
                print(f"    🚨 High risk (complexity: {analysis.complexity_score})")
            elif analysis.complexity_score > 6:
                print(f"    ⚡ Medium complexity: {analysis.complexity_score}")
            
            # Show security concerns
            if analysis.security_concerns:
                print(f"    🔒 Security concerns: {len(analysis.security_concerns)}")
            
        except Exception as e:
            print(f"    ❌ Error analyzing {rel_path}: {e}")
    
    # Summary
    print(f"\n📊 Analysis Summary:")
    print(f"  Files analyzed: {total_files}")
    print(f"  Average complexity: {total_complexity / total_files:.1f}")
    print(f"  Test coverage: {files_with_tests}/{total_files} files ({files_with_tests/total_files*100:.1f}%)")
    print(f"  High risk files: {len(high_risk_files)}")
    
    if high_risk_files:
        print(f"\n🚨 High Risk Files:")
        for file_path, analysis in high_risk_files:
            print(f"  - {file_path} (complexity: {analysis.complexity_score})")
            if analysis.security_concerns:
                for concern in analysis.security_concerns:
                    print(f"    🔒 {concern}")


def generate_tests_for_file(file_path: str, config: Config) -> None:
    """Generate tests for a specific file.
    
    Args:
        file_path: Path to the source file
        config: Configuration object
    """
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist")
        sys.exit(1)
    
    if not FileAnalyzer.is_source_file(file_path):
        print(f"Error: '{file_path}' is not a recognized source file")
        sys.exit(1)
    
    print(f"🧪 Generating tests for: {file_path}")
    
    # Initialize AI agent
    ai_agent = OllamaAIAgent(config)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Analyze the code
        print("  🔍 Analyzing code...")
        analysis = ai_agent.analyze_code_intelligence(code, file_path)
        
        print(f"  📊 Complexity score: {analysis.complexity_score}")
        print(f"  🔧 Functions found: {len(analysis.functions)}")
        print(f"  🏗️  Classes found: {len(analysis.classes)}")
        
        # Generate tests
        print("  🤖 Generating tests...")
        generated_test = ai_agent.generate_intelligent_tests(code, file_path, analysis)
        
        if generated_test:
            # Write test file
            test_file_path = generated_test.test_file
            with open(test_file_path, 'w', encoding='utf-8') as f:
                f.write(generated_test.test_content)
            
            print(f"  ✅ Test file generated: {test_file_path}")
            print(f"  🔧 Framework: {generated_test.framework}")
            print(f"  📝 Language: {generated_test.language}")
        else:
            print("  ❌ Failed to generate tests")
            
    except Exception as e:
        print(f"Error generating tests: {e}")
        sys.exit(1)


def health_check(config: Config) -> None:
    """Check health of AI agent and dependencies.
    
    Args:
        config: Configuration object
    """
    print("🏥 Health Check")
    
    # Check Ollama connection
    print(f"  🤖 Checking Ollama at {config.ollama_url}")
    ai_agent = OllamaAIAgent(config)
    health_info = ai_agent.health_check()
    
    if health_info["ollama_status"] == "connected":
        print(f"  ✅ Ollama connected")
        print(f"  📋 Model: {health_info['model']}")
    else:
        print(f"  ❌ Ollama not connected")
        print(f"  💡 Make sure Ollama is running: ollama serve")
        return
    
    # Test AI functionality
    print("  🧠 Testing AI functionality...")
    try:
        test_code = "def add(a, b): return a + b"
        analysis = ai_agent.analyze_code_intelligence(test_code, "test.py")
        
        if analysis.functions:
            print(f"  ✅ AI analysis working")
        else:
            print(f"  ⚠️  AI analysis returned empty results")
            
    except Exception as e:
        print(f"  ❌ AI test failed: {e}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description='GitHub PR AI Agent CLI')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze a repository')
    analyze_parser.add_argument('path', help='Path to the repository')
    
    # Generate tests command
    generate_parser = subparsers.add_parser('generate-tests', help='Generate tests for a file')
    generate_parser.add_argument('file', help='Path to the source file')
    
    # Health check command
    subparsers.add_parser('health', help='Check health of AI agent')
    
    # Server command
    server_parser = subparsers.add_parser('server', help='Start webhook server')
    server_parser.add_argument('--port', type=int, help='Port to run server on')
    server_parser.add_argument('--host', type=str, help='Host to bind server to')
    server_parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        # Load configuration
        config = Config.from_env()
        
        if args.command == 'analyze':
            analyze_repository(args.path, config)
        elif args.command == 'generate-tests':
            generate_tests_for_file(args.file, config)
        elif args.command == 'health':
            health_check(config)
        elif args.command == 'server':
            # Import here to avoid circular imports
            from .server.app import main as server_main
            
            # Override config with CLI args
            if args.port:
                config.port = args.port
            if args.host:
                config.host = args.host
            if args.debug:
                config.debug = True
            
            server_main()
        
    except ValueError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        if args.verbose:
            raise
        sys.exit(1)


if __name__ == '__main__':
    main()
