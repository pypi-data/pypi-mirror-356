from __future__ import annotations
import os
import logging
import torch
from transformers.integrations.bitsandbytes import (
    _validate_bnb_multi_backend_availability,
)
import importlib.metadata

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def _is_bnb_installed() -> bool:
    """Return True if the bitsandbytes package is installed."""
    try:
        importlib.metadata.version("bitsandbytes")
        return True
    except importlib.metadata.PackageNotFoundError:
        return False
    except Exception:
        return False


def detect_device_and_quant(user_opt_out: bool) -> tuple[dict | str, torch.dtype, bool]:
    """Detect device and desired quantisation settings.

    Returns
    -------
    device_map : dict | str
        Mapping passed to Transformers ``from_pretrained``.
    torch_dtype : torch.dtype
        Precision to load weights with.
    use_4bit : bool
        Whether to attempt 4-bit quantisation via bitsandbytes.
    """
    if user_opt_out:
        return "cpu", torch.float32, False

    if torch.cuda.is_available():
        if _is_bnb_installed():
            try:
                _validate_bnb_multi_backend_availability(raise_exception=True)
                return "auto", torch.bfloat16, True
            except Exception as exc:
                logger.debug("bitsandbytes backend unavailable: %s", exc)
        return "auto", torch.float16, False

    if torch.backends.mps.is_available():
        return {"": "mps"}, torch.float16, False

    return "cpu", torch.float32, False
