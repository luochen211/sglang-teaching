import unittest

from sglang_teaching.metrics import RequestSample, summarize


class MetricsTests(unittest.TestCase):
    def test_summary_contains_latency_and_throughput(self) -> None:
        result = summarize(
            [
                RequestSample(ttft_ms=10, total_latency_ms=100, output_tokens=20),
                RequestSample(ttft_ms=20, total_latency_ms=200, output_tokens=30),
            ]
        )

        self.assertEqual(result["requests"], 2.0)
        self.assertEqual(result["ttft_p50_ms"], 15.0)
        self.assertEqual(result["latency_p99_ms"], 199.0)
        self.assertAlmostEqual(result["output_tokens_per_second"], 166.6666667)

    def test_empty_summary_is_an_error(self) -> None:
        with self.assertRaises(ValueError):
            summarize([])


if __name__ == "__main__":
    unittest.main()
