"""
src/guardrails/policy.py
────────────────────────
Loads and validates the YAML policy file into a typed Python object.
All other modules (checker, scorer, runner) import Policy from here.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib    import Path
from typing     import List

import yaml


# ── Data classes ─────────────────────────────────────────────────────────────

@dataclass
class SeverityConfig:
    critical_threshold: int = 1
    warning_threshold:  int = 3


@dataclass
class SafeResponseRules:
    must_refuse_on:               List[str] = field(default_factory=list)
    must_not_match_patterns:      List[str] = field(default_factory=list)
    must_include_refusal_language: bool    = True
    refusal_phrases:              List[str] = field(default_factory=list)


@dataclass
class Policy:
    # Metadata
    name:        str = "default"
    version:     str = "1.0"
    description: str = ""

    # Limits
    max_tokens:       int = 500
    max_input_tokens: int = 2048

    # Tool restrictions
    allowed_tools: List[str] = field(default_factory=list)

    # Data blocks
    blocked_data_types: List[str] = field(default_factory=list)
    blocked_phrases:    List[str] = field(default_factory=list)
    injection_triggers: List[str] = field(default_factory=list)

    # Response rules
    safe_response_rules: SafeResponseRules = field(
        default_factory=SafeResponseRules
    )

    # Severity config
    severity: SeverityConfig = field(default_factory=SeverityConfig)

    # Pre-compiled regex patterns (populated after loading)
    _compiled_patterns: List[re.Pattern] = field(
        default_factory=list, repr=False
    )


# ── Loader ────────────────────────────────────────────────────────────────────

def load_policy(path: str | Path) -> Policy:
    """
    Read a YAML policy file from disk and return a validated Policy object.

    Raises:
        FileNotFoundError  – if the file does not exist
        ValueError         – if required fields are missing or invalid
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Policy file not found: {path}")

    with path.open() as fh:
        raw = yaml.safe_load(fh)

    if not raw or "policy" not in raw:
        raise ValueError(f"Policy file must have a top-level 'policy' key: {path}")

    data = raw["policy"]

    # Build nested objects
    srr_data  = data.get("safe_response_rules", {})
    sev_data  = data.get("severity", {})

    safe_rules = SafeResponseRules(
        must_refuse_on               = srr_data.get("must_refuse_on", []),
        must_not_match_patterns      = srr_data.get("must_not_match_patterns", []),
        must_include_refusal_language= srr_data.get("must_include_refusal_language", True),
        refusal_phrases              = srr_data.get("refusal_phrases", []),
    )

    severity = SeverityConfig(
        critical_threshold = sev_data.get("critical_threshold", 1),
        warning_threshold  = sev_data.get("warning_threshold",  3),
    )

    policy = Policy(
        name        = data.get("name",        "default"),
        version     = str(data.get("version",  "1.0")),
        description = data.get("description", ""),

        max_tokens       = int(data.get("max_tokens",       500)),
        max_input_tokens = int(data.get("max_input_tokens", 2048)),

        allowed_tools       = data.get("allowed_tools",       []),
        blocked_data_types  = data.get("blocked_data_types",  []),
        blocked_phrases     = data.get("blocked_phrases",     []),
        injection_triggers  = data.get("injection_triggers",  []),

        safe_response_rules = safe_rules,
        severity            = severity,
    )

    # Pre-compile regex patterns once at load time (fast at check time)
    policy._compiled_patterns = [
        re.compile(p, re.IGNORECASE)
        for p in policy.safe_response_rules.must_not_match_patterns
    ]

    _validate(policy)
    return policy


# ── Validation ────────────────────────────────────────────────────────────────

def _validate(policy: Policy) -> None:
    """Raise ValueError for obviously wrong policy values."""
    if policy.max_tokens <= 0:
        raise ValueError("max_tokens must be a positive integer")
    if policy.max_input_tokens <= 0:
        raise ValueError("max_input_tokens must be a positive integer")
    if policy.severity.critical_threshold < 1:
        raise ValueError("severity.critical_threshold must be >= 1")