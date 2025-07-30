import hmac, hashlib, json, time
from typing import Optional

from fygaro.webhook import FygaroWebhookValidator


def _make_header(secret: bytes, body: bytes, ts: Optional[int] = None) -> str:
    ts = ts or int(time.time())
    sig = hmac.new(secret, f"{ts}".encode() + b"." + body, hashlib.sha256).hexdigest()
    return f"t={ts},v1={sig}"


def test_validator_accepts_valid_signature():
    secret_current, secret_prev = b"current", b"prev"
    body = json.dumps({"ok": True}).encode()

    header = _make_header(secret_prev, body)

    validator = FygaroWebhookValidator(secrets=[secret_current, secret_prev])
    assert validator.verify_signature(header, body)


def test_validator_rejects_invalid_signature():
    secret_current, secret_prev = b"current", b"prev"
    body = json.dumps({"ok": True}).encode()

    bad_header = _make_header(b"invalid", body)

    validator = FygaroWebhookValidator(secrets=[secret_current, secret_prev])
    assert not validator.verify_signature(bad_header, body)
