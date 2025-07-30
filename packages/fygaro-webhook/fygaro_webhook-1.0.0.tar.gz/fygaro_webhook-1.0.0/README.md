# fygaro-webhook

> **Webhook signature verification for Fygaro — pure Python stdlib, zero runtime deps**

This helper validates the `Fygaro-Signature` header of incoming webhooks.
It supports secret rotation (multiple active secrets) and is ready for future
hash algorithms.

---

## Installation

```bash
pip install fygaro-webhook
```

Requires Python ≥ 3.8.

---

## Quick start

```python
from fygaro.webhook import FygaroWebhookValidator

# Load your current and (optionally) previous secrets
validator = FygaroWebhookValidator(
    secrets=[
        b"my-primary-secret",     # bytes or str → utf-8 encoded
    ],
    # max_age_seconds=300     # optional, default = 5 min
)

# In your view / handler
if not validator.verify_signature(
    signature_header=request.headers["Fygaro-Signature"],
    body=request.body,          # raw bytes exactly as sent
):
    raise ValueError("Invalid signature")

# ...process JSON, return 200...
```

---

## API reference (detailed)

### `class FygaroWebhookValidator`

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `secrets` | `Sequence[str \| bytes]` | ✔ | —  | One or more active webhook secrets. Provide **all currently valid** secrets during a rotation window. Each secret can be a UTF-8 `str` or raw `bytes`. |
| `max_age_seconds` | `int` | ✖ | `300` | Maximum allowable clock skew (in seconds) between the timestamp in the header and the server time. A low value mitigates replay attacks. |

```python
validator = FygaroWebhookValidator(
    secrets=["primary"],        # Add multiple for rotation: secrets=["primary", "previous"]
)
```

---

#### `validator.verify_signature(signature_header: str, body: bytes) -> bool`

| Argument | Type | Description |
|----------|------|-------------|
| `signature_header` | `str` | The exact value of the incoming **Fygaro-Signature** HTTP header. |
| `body` | `bytes` | The unmodified request body (raw bytes). **Do not** `.decode()` or re-serialize. |

Return value:

* `True` — signature is valid **and** timestamp is within `max_age_seconds`.
* `False` — signature mismatch, stale timestamp, or malformed header.

```python
is_valid = validator.verify_signature(sig_header, raw_body)
```

---

## License

MIT © Fygaro — support: [support@fygaro.com](mailto:support@fygaro.com)
