"""
BEIREK Content Scout - Claude Session Module
=============================================

Manages Claude CLI session lifecycle for consistent AI interactions.

Features:
- Singleton session management
- System prompt loading
- Query execution with timeout
- Graceful session cleanup
- Fallback for per-request mode
"""

import subprocess
import threading
import time
from pathlib import Path
from typing import Optional
import atexit

from .logger import get_logger
from .config_manager import config

# Module logger
logger = get_logger(__name__)


class ClaudeSessionError(Exception):
    """Base exception for Claude session errors."""
    pass


class ClaudeSession:
    """
    Singleton Claude CLI session manager.

    Maintains a persistent session for efficient Claude interactions.
    Falls back to per-request mode if session fails.
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        """Ensure singleton instance."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize session manager."""
        if self._initialized:
            return

        self._initialized = True
        self.timeout = config.get('claude.timeout_seconds', 180)
        self.max_retries = config.get('claude.max_retries', 3)
        self.session_active = False
        self.system_prompt = None

        # Load system prompt
        self._load_system_prompt()

        # Register cleanup on exit
        atexit.register(self.stop)

        logger.info("Claude session manager initialized")

    def _load_system_prompt(self):
        """Load system prompt from file."""
        prompt_path = config.base_path / "prompts" / "system_prompt.txt"

        if prompt_path.exists():
            with open(prompt_path, 'r', encoding='utf-8') as f:
                self.system_prompt = f.read()
        else:
            self.system_prompt = self._get_default_system_prompt()

    def _get_default_system_prompt(self) -> str:
        """Get default system prompt."""
        return """Sen BEIREK Content Scout icin bir yapay zeka asistanisin.

BEIREK, altyapi ve enerji projelerinde proje yonetimi, finansman ve danismanlik hizmetleri sunan bir sirket.

GOREVLERIN:
1. Haberleri filtrele ve BEIREK icin relevance skorla (0-10)
2. Uygun haberleri BEIREK calisma alanlarina esle (1-8)
3. Icerik onerileri olustur
4. Makale, LinkedIn ve Twitter icerikleri uret

BEIREK CALISMA ALANLARI:
1. Deal & Contract Advisory
2. CEO Office & Governance
3. Development Finance & Compliance
4. Project Development & Finance
5. Engineering & Delivery
6. Asset Management (O&M)
7. GTM & JV Management
8. Digital Platforms

KURALLAR:
- Her zaman Turkce yaz
- Kaynak disinda bilgi ekleme (hallucination)
- Profesyonel ve teknik bir ton kullan
- BEIREK perspektifinden yaz
"""

    def start(self) -> bool:
        """
        Start Claude session.

        Returns:
            True if session started successfully
        """
        if self.session_active:
            return True

        try:
            # Check if Claude CLI is available
            result = subprocess.run(
                ['claude', '--version'],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode != 0:
                raise ClaudeSessionError("Claude CLI not available")

            self.session_active = True
            logger.info("Claude session started successfully")
            return True

        except FileNotFoundError:
            logger.error("Claude CLI not found. Install from https://claude.ai/cli")
            return False
        except subprocess.TimeoutExpired:
            logger.error("Claude CLI check timed out")
            return False
        except Exception as e:
            logger.error(f"Failed to start Claude session: {e}")
            return False

    def stop(self):
        """Stop Claude session and cleanup."""
        if self.session_active:
            self.session_active = False
            logger.info("Claude session stopped")

    def query(self, prompt: str, include_system_prompt: bool = True) -> str:
        """
        Send query to Claude and get response.

        Args:
            prompt: User prompt
            include_system_prompt: Whether to include system prompt

        Returns:
            Claude's response
        """
        if not self.session_active:
            self.start()

        # Build full prompt
        full_prompt = prompt
        if include_system_prompt and self.system_prompt:
            full_prompt = f"{self.system_prompt}\n\n---\n\n{prompt}"

        # Execute query with retries
        for attempt in range(self.max_retries):
            try:
                return self._execute_query(full_prompt)
            except ClaudeSessionError as e:
                if attempt == self.max_retries - 1:
                    raise
                wait_time = 2 ** attempt
                logger.warning(f"Query attempt {attempt + 1} failed, retrying in {wait_time}s: {e}")
                time.sleep(wait_time)

        raise ClaudeSessionError("All query attempts failed")

    def _execute_query(self, prompt: str) -> str:
        """Execute a single query to Claude CLI."""
        process = None
        try:
            process = subprocess.Popen(
                ['claude', '--print'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=False
            )

            stdout, stderr = process.communicate(
                input=prompt,
                timeout=self.timeout
            )

            if process.returncode != 0:
                raise ClaudeSessionError(f"Claude CLI error: {stderr}")

            return stdout.strip()

        except subprocess.TimeoutExpired:
            if process:
                process.kill()
                process.wait()
            raise ClaudeSessionError(f"Query timed out after {self.timeout}s")

        except FileNotFoundError:
            raise ClaudeSessionError("Claude CLI not found")

        except Exception as e:
            if process and process.poll() is None:
                process.kill()
                process.wait()
            raise ClaudeSessionError(f"Query failed: {e}")

    def query_json(self, prompt: str, include_system_prompt: bool = True) -> dict:
        """
        Send query and parse JSON response.

        Args:
            prompt: User prompt (should request JSON output)
            include_system_prompt: Whether to include system prompt

        Returns:
            Parsed JSON dict
        """
        import json
        import re

        response = self.query(prompt, include_system_prompt)

        # Try to extract JSON from response
        # Look for JSON block
        json_match = re.search(r'```json\s*([\s\S]*?)\s*```', response)
        if json_match:
            json_str = json_match.group(1)
        else:
            # Try to find JSON directly
            json_match = re.search(r'[\[{][\s\S]*[\]}]', response)
            if json_match:
                json_str = json_match.group(0)
            else:
                json_str = response

        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse JSON response: {e}")
            return {}

    def is_available(self) -> bool:
        """Check if Claude CLI is available."""
        try:
            result = subprocess.run(
                ['claude', '--version'],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except Exception:
            return False

    def get_version(self) -> str:
        """Get Claude CLI version."""
        try:
            result = subprocess.run(
                ['claude', '--version'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception:
            pass
        return "unknown"


# Global session instance
_session = None


def get_session() -> ClaudeSession:
    """Get or create Claude session instance."""
    global _session
    if _session is None:
        _session = ClaudeSession()
    return _session


def start_session() -> bool:
    """Start the Claude session."""
    return get_session().start()


def stop_session():
    """Stop the Claude session."""
    session = get_session()
    if session:
        session.stop()


def query_claude(prompt: str, include_system_prompt: bool = True) -> str:
    """Quick helper to query Claude."""
    return get_session().query(prompt, include_system_prompt)


def is_cli_available() -> bool:
    """Check if Claude CLI is available."""
    return get_session().is_available()


if __name__ == "__main__":
    print("Testing Claude Session Manager...")

    session = get_session()

    print(f"Claude CLI available: {session.is_available()}")
    print(f"Claude CLI version: {session.get_version()}")

    if session.is_available():
        print("\nStarting session...")
        if session.start():
            print("Session started!")

            # Test query
            print("\nTesting query...")
            try:
                response = session.query("Merhaba, sen BEIREK Content Scout icin bir AI asistanisin. Sadece 'Evet, hazirim.' de.")
                print(f"Response: {response[:100]}...")
            except ClaudeSessionError as e:
                print(f"Query failed: {e}")

            print("\nStopping session...")
            session.stop()
            print("Session stopped!")
    else:
        print("\nClaude CLI not available. Install from https://claude.ai/cli")
