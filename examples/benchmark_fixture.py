"""Summarise a small fixture, so the metrics lesson works without a GPU."""

from sglang_teaching.metrics import RequestSample, summarize


def main() -> None:
    samples = [
        RequestSample(ttft_ms=82, total_latency_ms=410, output_tokens=96),
        RequestSample(ttft_ms=77, total_latency_ms=384, output_tokens=96),
        RequestSample(ttft_ms=95, total_latency_ms=452, output_tokens=96),
    ]
    for name, value in summarize(samples).items():
        print(f"{name}: {value:.2f}")


if __name__ == "__main__":
    main()

