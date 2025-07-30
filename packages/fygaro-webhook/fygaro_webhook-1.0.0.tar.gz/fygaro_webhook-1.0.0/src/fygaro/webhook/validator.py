"""
validator.py - single-class API for Fygaro webhook validation.

• Pure standard library (hashlib, hmac, time)
• Handles multiple secrets (rotation) and multiple v1= entries
• Constant-time comparisons via hmac.compare_digest
• Ready for future algorithm tags by extending _HASH_FUNCTIONS
"""

from __future__ import annotations

import hashlib
import hmac
import time
from typing import Dict, Final, List, Mapping, Sequence, Union, Optional

# ------------------------------------------------------------------ #
# Configuration
# ------------------------------------------------------------------ #
DEFAULT_MAX_AGE_SECONDS: Final[int] = 5 * 60  # five minutes
_HASH_FUNCTIONS: Dict[str, callable] = {
    "v1": hashlib.sha256,  # current production hash
    # "v2": hashlib.sha512,  # example future upgrade
}
_HEADER_TS_KEY: Final[str] = "t"


def _parse_header(header: str) -> Mapping[str, List[str]]:
    """t=123,v1=a,v1=b → {'t':['123'], 'v1':['a','b']}"""
    parsed: Dict[str, List[str]] = {}
    for token in header.split(","):
        if "=" in token:
            k, v = token.split("=", 1)
            parsed.setdefault(k.strip(), []).append(v.strip())

    return parsed


def _normalize_secret(secret: Union[bytes, str]) -> bytes:
    """Accept bytes or UTF-8 str. Strings are encoded to bytes."""
    return secret if isinstance(secret, bytes) else secret.encode()


class FygaroWebhookValidator:
    """
    Reusable validator.

    Example 1
    -------
    >>> validator = FygaroWebhookValidator(secrets=[PRIMARY])
    >>> if not validator.verify_signature(sig_header, body):
    ...     raise ValueError("invalid signature")

    Example 2
    -------
    >>> validator = FygaroWebhookValidator(secrets=[PRIMARY, OLD])
    >>> if not validator.verify_signature(sig_header, body):
    ...     raise ValueError("invalid signature")
    """

    __slots__ = ("_secret_bytes", "_max_age")

    def __init__(
        self,
        *,
        secrets: Sequence[Union[bytes, str]],
        max_age_seconds: int = DEFAULT_MAX_AGE_SECONDS,
    ) -> None:
        self._secret_bytes: List[bytes] = [_normalize_secret(s) for s in secrets]
        self._max_age: int = max_age_seconds

    # ---------------------------------------------------------- #
    def verify_signature(self, signature_header: Optional[str], body: bytes) -> bool:
        if signature_header is None:
            return False

        parsed = _parse_header(signature_header)

        # timestamp freshness
        try:
            ts = int(parsed[_HEADER_TS_KEY][0])

        except (KeyError, ValueError, IndexError):
            return False

        if abs(time.time() - ts) > self._max_age:
            return False

        # evaluate every secret × algorithm × candidate combination
        for secret in self._secret_bytes:
            for version, hash_fn in _HASH_FUNCTIONS.items():
                if version not in parsed:
                    continue

                expected = hmac.new(
                    secret,
                    f"{ts}".encode() + b"." + body,
                    hash_fn,
                ).hexdigest()

                if any(
                    hmac.compare_digest(expected, candidate)
                    for candidate in parsed[version]
                ):
                    return True

        return False
