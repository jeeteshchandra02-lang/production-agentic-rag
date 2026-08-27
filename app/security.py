import re


SUSPICIOUS_PATTERNS = [
    r"ignore (all|any|the) previous instructions",
    r"reveal (the )?(system|developer) prompt",
    r"show (me )?(your )?hidden instructions",
    r"bypass (the )?(rules|guardrails|policy)",
]


def detect_prompt_injection(text: str) -> bool:
    lowered = text.lower()

    return any(
        re.search(pattern, lowered)
        for pattern in SUSPICIOUS_PATTERNS
    )
