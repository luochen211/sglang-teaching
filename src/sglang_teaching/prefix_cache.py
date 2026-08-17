"""A CPU-only prefix-cache model used to teach cache reuse.

This is deliberately small and is not SGLang's production implementation. It
models the observable idea behind a radix/prefix cache: requests sharing a
prefix can reuse the already processed prefix tokens.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence


Token = str


@dataclass(frozen=True)
class CacheLookup:
    """The result of looking up one prompt in the teaching cache."""

    prompt_tokens: int
    cached_tokens: int

    @property
    def uncached_tokens(self) -> int:
        """Number of tokens that still need to be processed."""

        return self.prompt_tokens - self.cached_tokens

    @property
    def hit_rate(self) -> float:
        """Fraction of prompt tokens found in the cache."""

        if self.prompt_tokens == 0:
            return 0.0
        return self.cached_tokens / self.prompt_tokens


class PrefixCache:
    """A deterministic set-based model of a prefix trie.

    Every inserted prompt contributes all of its prefixes. A later request
    receives the longest prefix that has already been inserted. Keeping this
    model set-based makes the lesson about the scheduling/cache invariant
    visible without requiring CUDA, a model download, or a tokenizer.
    """

    def __init__(self) -> None:
        self._prefixes: set[tuple[Token, ...]] = {()}

    @staticmethod
    def _normalise(tokens: Iterable[Token]) -> tuple[Token, ...]:
        normalised = tuple(tokens)
        if any(not isinstance(token, str) or not token for token in normalised):
            raise ValueError("tokens must be non-empty strings")
        return normalised

    def lookup(self, tokens: Sequence[Token]) -> CacheLookup:
        """Return the longest cached prefix without changing cache state."""

        prompt = self._normalise(tokens)
        longest = 0
        for end in range(1, len(prompt) + 1):
            if prompt[:end] not in self._prefixes:
                break
            longest = end
        return CacheLookup(prompt_tokens=len(prompt), cached_tokens=longest)

    def insert(self, tokens: Sequence[Token]) -> None:
        """Insert every prefix of a prompt into the cache."""

        prompt = self._normalise(tokens)
        self._prefixes.update(prompt[:end] for end in range(1, len(prompt) + 1))

    def process(self, tokens: Sequence[Token]) -> CacheLookup:
        """Look up and then insert a request, returning its cache result."""

        result = self.lookup(tokens)
        self.insert(tokens)
        return result

    def clear(self) -> None:
        """Drop all reusable prefixes."""

        self._prefixes = {()}

