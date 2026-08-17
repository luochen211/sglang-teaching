"""Tiny metrics helpers for the benchmark lesson."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class RequestSample:
    """Measurements collected for one completed streaming request."""

    ttft_ms: float
    total_latency_ms: float
    output_tokens: int

    def __post_init__(self) -> None:
        if self.ttft_ms < 0 or self.total_latency_ms < 0:
            raise ValueError("latencies must be non-negative")
        if self.output_tokens < 1:
            raise ValueError("output_tokens must be positive")


def _percentile(values: list[float], percentile: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = (len(ordered) - 1) * percentile
    lower = int(index)
    upper = min(lower + 1, len(ordered) - 1)
    fraction = index - lower
    return ordered[lower] + (ordered[upper] - ordered[lower]) * fraction


def summarize(samples: Iterable[RequestSample]) -> dict[str, float]:
    """Return stable, JSON-friendly latency and throughput summaries.

    ``output_tokens_per_second`` is intentionally based on the sum of output
    tokens divided by the sum of request durations. A real online benchmark
    should also report wall-clock throughput and concurrency separately.
    """

    rows = list(samples)
    if not rows:
        raise ValueError("at least one sample is required")
    ttft = [row.ttft_ms for row in rows]
    total = [row.total_latency_ms for row in rows]
    token_count = sum(row.output_tokens for row in rows)
    elapsed_seconds = sum(total) / 1000
    return {
        "requests": float(len(rows)),
        "ttft_p50_ms": _percentile(ttft, 0.50),
        "ttft_p99_ms": _percentile(ttft, 0.99),
        "latency_p50_ms": _percentile(total, 0.50),
        "latency_p99_ms": _percentile(total, 0.99),
        "output_tokens": float(token_count),
        "output_tokens_per_second": token_count / elapsed_seconds
        if elapsed_seconds
        else 0.0,
    }

