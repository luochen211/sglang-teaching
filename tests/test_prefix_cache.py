import unittest

from sglang_teaching.prefix_cache import PrefixCache


class PrefixCacheTests(unittest.TestCase):
    def test_reuses_the_longest_shared_prefix(self) -> None:
        cache = PrefixCache()
        first = cache.process(("system", "You", "are", "helpful"))
        second = cache.process(("system", "You", "are", "brief"))

        self.assertEqual(first.cached_tokens, 0)
        self.assertEqual(first.uncached_tokens, 4)
        self.assertEqual(second.cached_tokens, 3)
        self.assertAlmostEqual(second.hit_rate, 0.75)

    def test_lookup_does_not_mutate_state(self) -> None:
        cache = PrefixCache()
        cache.insert(("a", "b"))

        result = cache.lookup(("a", "c"))
        self.assertEqual(result.cached_tokens, 1)
        self.assertEqual(cache.lookup(("a", "c")).cached_tokens, 1)

    def test_empty_prompt_and_invalid_tokens(self) -> None:
        cache = PrefixCache()
        self.assertEqual(cache.lookup(()).cached_tokens, 0)
        with self.assertRaises(ValueError):
            cache.process(("",))


if __name__ == "__main__":
    unittest.main()

