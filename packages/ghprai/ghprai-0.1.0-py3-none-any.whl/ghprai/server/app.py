"""Flask application for GitHub PR AI Agent webhook server."""

import logging
from flask import Flask, request, jsonify
from typing import Optional

from ..agents.github_agent import GitHubPRAgent
from ..core.config import Config

logger = logging.getLogger(__name__)


def create_app(config: Optional[Config] = None) -> Flask:
    """Create and configure Flask application.
    
    Args:
        config: Configuration object. If None, loads from environment.
        
    Returns:
        Configured Flask application
    """
    app = Flask(__name__)
    
    # Load configuration
    if config is None:
        config = Config.from_env()
    
    config.validate()
    app.config.update(config.__dict__)
    
    # Initialize GitHub agent
    github_agent = GitHubPRAgent(config)
    
    @app.route('/webhook', methods=['POST'])
    def github_webhook():
        """Handle GitHub webhook events."""
        try:
            payload = request.json
            
            if not payload.get('pull_request'):
                return jsonify({"status": "ignored", "reason": "Not a PR event"})
            
            result = github_agent.process_pr(payload)
            
            return jsonify({
                "status": result.status,
                "pr_number": result.pr_number,
                "repository": result.repository,
                "analyzed_files": len(result.changed_files),
                "new_tests": len(result.generated_tests),
                "test_status": result.coverage.test_results.status if result.coverage.test_results else "not_run",
                "new_branch": result.new_branch
            })
            
        except Exception as e:
            logger.error(f"Webhook error: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint."""
        health_info = github_agent.ai_agent.health_check()
        
        return jsonify({
            "status": "healthy",
            "ollama": health_info["ollama_status"],
            "model": health_info["model"],
            "url": health_info["ollama_url"]
        })
    
    @app.route('/test-ai', methods=['POST'])
    def test_ai():
        """Test AI agent functionality."""
        try:
            data = request.json or {}
            code = data.get('code', 'def hello(): return "world"')
            file_path = data.get('file_path', 'test.py')
            
            analysis = github_agent.ai_agent.analyze_code_intelligence(code, file_path)
            
            return jsonify({
                "analysis": {
                    "file_path": analysis.file_path,
                    "complexity_score": analysis.complexity_score,
                    "functions": analysis.functions,
                    "classes": analysis.classes,
                    "edge_cases": analysis.edge_cases,
                    "test_scenarios": analysis.test_scenarios,
                    "risk_level": analysis.risk_level
                }
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route('/generate-test', methods=['POST'])
    def generate_test():
        """Generate test for provided code."""
        try:
            data = request.json or {}
            code = data.get('code', '')
            file_path = data.get('file_path', 'test.py')
            
            if not code:
                return jsonify({"error": "Code is required"}), 400
            
            # First analyze the code
            analysis = github_agent.ai_agent.analyze_code_intelligence(code, file_path)
            
            # Then generate tests
            generated_test = github_agent.ai_agent.generate_intelligent_tests(code, file_path, analysis)
            
            if generated_test:
                return jsonify({
                    "test_file": generated_test.test_file,
                    "test_content": generated_test.test_content,
                    "framework": generated_test.framework,
                    "language": generated_test.language
                })
            else:
                return jsonify({"error": "Failed to generate test"}), 500
                
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route('/review-code', methods=['POST'])
    def review_code():
        """Get AI code review suggestions."""
        try:
            data = request.json or {}
            code = data.get('code', '')
            file_path = data.get('file_path', 'test.py')
            
            if not code:
                return jsonify({"error": "Code is required"}), 400
            
            suggestions = github_agent.ai_agent.suggest_code_improvements(code, file_path)
            
            return jsonify({
                "suggestions": suggestions,
                "file_path": file_path
            })
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return app


def main():
    """Main entry point for the server."""
    import argparse
    
    parser = argparse.ArgumentParser(description='GitHub PR AI Agent Server')
    parser.add_argument('--port', type=int, help='Port to run the server on')
    parser.add_argument('--host', type=str, help='Host to bind the server to')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    # Load configuration
    config = Config.from_env()
    
    # Override with command line arguments
    if args.port:
        config.port = args.port
    if args.host:
        config.host = args.host
    if args.debug:
        config.debug = True
    
    # Create app
    app = create_app(config)
    
    # Configure logging
    log_level = logging.DEBUG if config.debug else logging.INFO
    logging.basicConfig(level=log_level)
    
    logger.info(f"Starting GitHub PR AI Agent server on {config.host}:{config.port}")
    logger.info(f"Using Ollama at {config.ollama_url} with model {config.ollama_model}")
    
    # Run the app
    app.run(host=config.host, port=config.port, debug=config.debug)


if __name__ == '__main__':
    main()
