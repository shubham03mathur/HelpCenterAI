import re


# This is an early safety gate, not a replacement for model instructions.
# Any match causes the workflow to stop before an LLM sees the request.
UNSAFE_REQUEST = re.compile(
    r"(?:"
    r"ignore\s+(?:all\s+)?(?:previous|prior|above)\s+instructions|"
    r"(?:system|developer|hidden|internal)\s+(?:prompt|instruction)s?|"
    r"(?:reveal|show|tell|provide|share|give|list|expose|print|output|disclose|"
    r"know|see|access)\b.{0,100}\b(?:system|developer|hidden|internal)\b.{0,60}\b"
    r"(?:prompt|instruction)s?|"
    r"(?:api|access|auth|private|secret)\s*(?:key|token|credential)s?|"
    r"(?:show|reveal|provide|share|give|list|dump|print|output)\b.{0,80}\b"
    r"(?:password|secret|credential)s?|"
    r"jailbreak|"
    r"(?:write|generate|debug|run|execute)\s+(?:some\s+)?"
    r"(?:code|python|javascript|sql)"
    r")",
    re.IGNORECASE,
)

def is_unsafe_request(message: str) -> bool:
    """Return true for requests that must not be partially answered."""
    return bool(UNSAFE_REQUEST.search(message))
