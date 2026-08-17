"""Run the CPU-only prefix-cache experiment from lesson 02."""

from sglang_teaching.prefix_cache import PrefixCache


REQUESTS = [
    ("system", "You", "are", "a", "helpful", "teacher"),
    ("system", "You", "are", "a", "helpful", "reviewer"),
    ("system", "You", "are", "a", "concise", "teacher"),
    ("new", "conversation", "with", "no", "shared", "prefix"),
]


def main() -> None:
    cache = PrefixCache()
    for index, prompt in enumerate(REQUESTS, start=1):
        result = cache.process(prompt)
        print(
            f"request={index} prompt_tokens={result.prompt_tokens} "
            f"cached_tokens={result.cached_tokens} "
            f"uncached_tokens={result.uncached_tokens} "
            f"hit_rate={result.hit_rate:.1%}"
        )


if __name__ == "__main__":
    main()

