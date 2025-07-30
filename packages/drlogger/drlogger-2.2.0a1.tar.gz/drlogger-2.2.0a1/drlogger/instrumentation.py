"""instrumentation.py"""

import typing as t

__all__ = ["get_current_span", "get_tracer_provider"]

try:
    from opentelemetry.trace import (
        get_current_span,
        get_tracer_provider,
    )
except ModuleNotFoundError:

    def get_current_span() -> t.Optional[t.Any]:
        """dummy current span"""
        return None

    def get_tracer_provider() -> t.Optional[t.Any]:
        """dummy trace provider"""
        return None
