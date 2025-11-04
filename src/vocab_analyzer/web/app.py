"""Flask application factory for vocabulary analyzer web interface.

This module provides the Flask app factory function for creating
configured Flask instances with error handlers and cleanup scheduling.
"""

import logging
from pathlib import Path
from typing import Optional

from flask import Flask, jsonify

from .session import cleanup_expired_sessions


def _initialize_translation_system(app: Flask) -> None:
    """
    Initialize translation system on application startup.

    This function attempts to automatically install and configure:
    - Argos Translate English→Chinese model
    - ECDICT dictionary (optional)

    If automatic installation fails, a warning is logged and the app continues.
    Users can still use the app but translation features will show errors.
    """
    try:
        app.logger.info("="*70)
        app.logger.info("Initializing Translation System...")
        app.logger.info("="*70)

        from ..translation.auto_setup import auto_setup, get_setup_instructions

        # Run automatic setup (non-blocking, won't crash the app)
        status = auto_setup()

        # Log results
        if status['argos_installed']:
            app.logger.info("✅ Argos Translate: Ready")
        else:
            app.logger.warning("⚠️  Argos Translate: Not available")
            app.logger.warning(f"   {status['argos_message']}")

        if status['ecdict_installed']:
            app.logger.info("✅ ECDICT Dictionary: Ready")
        else:
            app.logger.info("ℹ️  ECDICT Dictionary: Not available (optional)")
            app.logger.info(f"   {status['ecdict_message']}")

        if status['ready']:
            app.logger.info("="*70)
            app.logger.info("✅ Translation System Ready!")
            app.logger.info("="*70)
        else:
            app.logger.warning("="*70)
            app.logger.warning("⚠️  Translation System Incomplete")
            app.logger.warning("="*70)
            app.logger.warning("Translation features may not work properly.")
            app.logger.warning("For manual setup instructions, see:")
            app.logger.warning("  python -m vocab_analyzer.translation.auto_setup")
            app.logger.warning("="*70)

    except Exception as e:
        app.logger.error(f"Error initializing translation system: {e}")
        app.logger.error("Translation features may not work, but app will continue.")
        app.logger.error("For manual setup: python -m vocab_analyzer.translation.auto_setup")


def create_app(config: Optional[dict] = None) -> Flask:
    """Create and configure a Flask application instance.

    Args:
        config: Optional configuration dictionary

    Returns:
        Configured Flask application
    """
    # Create Flask app
    app = Flask(
        __name__,
        static_folder=str(Path(__file__).parent / "static"),
        template_folder=str(Path(__file__).parent / "templates")
    )

    # Default configuration
    app.config.update({
        "MAX_CONTENT_LENGTH": 50 * 1024 * 1024,  # 50MB max upload
        "SECRET_KEY": "dev-secret-key-change-in-production",
        "UPLOAD_FOLDER": Path(__file__).parent.parent.parent.parent / "tmp" / "uploads",
    })

    # Apply custom configuration if provided
    if config:
        app.config.update(config)

    # Ensure upload folder exists
    upload_folder = Path(app.config["UPLOAD_FOLDER"])
    upload_folder.mkdir(parents=True, exist_ok=True)

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Initialize translation system on first startup
    _initialize_translation_system(app)

    # Register error handlers
    @app.errorhandler(413)
    def file_too_large(error):
        """Handle file too large errors."""
        return jsonify({
            "error": "FILE_TOO_LARGE",
            "message": "File size exceeds 50MB limit"
        }), 413

    @app.errorhandler(404)
    def not_found(error):
        """Handle not found errors."""
        return jsonify({
            "error": "NOT_FOUND",
            "message": "Resource not found"
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Handle internal server errors."""
        app.logger.error(f"Internal server error: {error}")
        return jsonify({
            "error": "INTERNAL_ERROR",
            "message": "An internal server error occurred"
        }), 500

    # Register cleanup hooks
    @app.before_request
    def cleanup_sessions():
        """Clean up expired sessions before each request."""
        cleaned = cleanup_expired_sessions()
        if cleaned > 0:
            app.logger.info(f"Cleaned up {cleaned} expired sessions")

    # Register routes blueprint
    from .routes import web_bp
    app.register_blueprint(web_bp)

    return app


if __name__ == "__main__":
    # Development server
    app = create_app()
    app.run(debug=True, host="127.0.0.1", port=5000)
