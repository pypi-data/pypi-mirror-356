"""Security guardrails for MCP client."""

import re
import asyncio
from typing import List, Dict, Any, Optional, Callable, Awaitable
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class GuardrailResult:
    """Result of a guardrail check."""
    passed: bool
    message: str
    masked_content: Optional[str] = None

class BaseGuardrail:
    """Base class for all guardrails."""
    
    def __init__(self, name: str):
        self.name = name
    
    async def check(self, content: str) -> GuardrailResult:
        """Check content against this guardrail."""
        raise NotImplementedError("Subclasses must implement check()")

class WordMaskGuardrail(BaseGuardrail):
    """Guardrail that masks specific words."""
    
    def __init__(self, name: str, words_to_mask: List[str], replacement: str = "[REDACTED]"):
        super().__init__(name)
        self.words_to_mask = words_to_mask
        self.replacement = replacement
        # Fix: Use word boundaries that work with case-insensitive matching
        pattern_parts = []
        for word in words_to_mask:
            # Escape special regex characters in the word
            escaped_word = re.escape(word)
            # Add word boundaries that work with case-insensitive matching
            pattern_parts.append(f"(?<![a-zA-Z]){escaped_word}(?![a-zA-Z])")
        self.pattern = re.compile('|'.join(pattern_parts), re.IGNORECASE)
    
    async def check(self, content: str) -> GuardrailResult:
        if not content:
            return GuardrailResult(True, "Empty content")
        
        masked_content = self.pattern.sub(self.replacement, content)
        if masked_content != content:
            return GuardrailResult(
                False,
                f"Found masked words in content",
                masked_content
            )
        return GuardrailResult(True, "No masked words found")

class ResponseBlockGuardrail(BaseGuardrail):
    """Guardrail that blocks responses containing specific words/phrases and returns a standardized response."""
    
    def __init__(self, name: str, blocked_words: List[str], standardized_response: str = "I apologize, but I cannot provide that information."):
        super().__init__(name)
        self.blocked_words = blocked_words
        self.standardized_response = standardized_response
        # Create pattern for blocked words with word boundaries
        pattern_parts = []
        for word in blocked_words:
            # Escape special regex characters in the word
            escaped_word = re.escape(word)
            # Add word boundaries that work with case-insensitive matching
            # This will match the word as a whole word or as part of another word
            pattern_parts.append(f"\\b{escaped_word}\\b|{escaped_word}")
        self.pattern = re.compile('|'.join(pattern_parts), re.IGNORECASE)
    
    async def check(self, content: str) -> GuardrailResult:
        if not content:
            return GuardrailResult(True, "Empty content")
        
        # Check if any blocked words are present
        if self.pattern.search(content):
            return GuardrailResult(
                False,
                f"Response contains blocked words/phrases",
                self.standardized_response
            )
        return GuardrailResult(True, "No blocked words found in response")

class PIIGuardrail(BaseGuardrail):
    """Guardrail that detects and masks PII."""
    
    def __init__(self, name: str):
        super().__init__(name)
        # Common PII patterns
        self.patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\+?1?\s*\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b',
            'ssn': r'\b[0-9]{3}-[0-9]{2}-[0-9]{4}\b',
            'credit_card': r'\b[0-9]{4}[- ]?[0-9]{4}[- ]?[0-9]{4}[- ]?[0-9]{4}\b'
        }
    
    async def check(self, content: str) -> GuardrailResult:
        if not content:
            return GuardrailResult(True, "Empty content")
        
        masked_content = content
        found_pii = []
        
        for pii_type, pattern in self.patterns.items():
            matches = re.finditer(pattern, content)
            for match in matches:
                found_pii.append(pii_type)
                masked_content = masked_content.replace(match.group(), "[REDACTED]")
        
        if found_pii:
            return GuardrailResult(
                False,
                f"Found PII: {', '.join(set(found_pii))}",
                masked_content
            )
        return GuardrailResult(True, "No PII found")

class InjectionGuardrail(BaseGuardrail):
    """Guardrail that detects potential injection attacks."""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.patterns = {
            'xss': r'<script.*?>.*?</script>|<.*?javascript:.*?>|<.*?\\s+on.*?=.*?>',
            'sql': r'\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|ALTER|EXEC|DECLARE)\b.*?[\'"]',
            'shell': r'[;&|`\$]|\b(cat|chmod|curl|wget|bash|sh|python|perl|ruby)\b',
            'path_traversal': r'\.\.\/|\.\.\\'
        }
    
    async def check(self, content: str) -> GuardrailResult:
        if not content:
            return GuardrailResult(True, "Empty content")
        
        found_injections = []
        
        for injection_type, pattern in self.patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                found_injections.append(injection_type)
        
        if found_injections:
            return GuardrailResult(
                False,
                f"Potential injection detected: {', '.join(found_injections)}",
                None
            )
        return GuardrailResult(True, "No injection patterns found")

class GuardrailManager:
    """Manager for multiple guardrails."""
    
    def __init__(self):
        self.guardrails: List[BaseGuardrail] = []
    
    def add_guardrail(self, guardrail: BaseGuardrail):
        """Add a guardrail to the manager."""
        self.guardrails.append(guardrail)
    
    async def check_all(self, content: str) -> List[GuardrailResult]:
        """Run all guardrails against the content."""
        if not content:
            return [GuardrailResult(True, "Empty content")]
        
        tasks = [guardrail.check(content) for guardrail in self.guardrails]
        results = await asyncio.gather(*tasks)
        
        # Apply masking in sequence if multiple guardrails mask content
        masked_content = content
        for result in results:
            if result.masked_content:
                masked_content = result.masked_content
        
        # Update masked content in results
        for result in results:
            if result.masked_content:
                result.masked_content = masked_content
        
        return results
    
    def get_guardrail(self, name: str) -> Optional[BaseGuardrail]:
        """Get a guardrail by name."""
        for guardrail in self.guardrails:
            if guardrail.name == name:
                return guardrail
        return None 