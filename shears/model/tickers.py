"""Library for dealing with stock tickers.
"""
from collections import Counter
from collections.abc import Callable, Iterable
import string
from typing import Optional, TypeVar


# A stock ticker symbol.
Ticker = str

_A = TypeVar('A')
_B = TypeVar('B')


def _map_optional(
    f: Callable[[_A], Optional[_B]],
    it: Iterable[_A]
) -> Iterable[_B]:
    """Given f: a -> Optional[b] and [a], returns [b].

    Applies f on it and filters empty optionals.
    """
    return filter(lambda x: x is not None, map(f, it))


def scrape_tickers(text: str) -> Counter[Ticker]:
    """Aggregates ticker mentions from a body of text.
    """
    def _scrape_ticker(token: str) -> Optional[Ticker]:
        if 1 <= len(token) <= 4 and token.isalpha() and token.isupper():
            return token
    text = text.translate(str.maketrans('', '', string.punctuation))
    counts = Counter()
    counts.update(_map_optional(_scrape_ticker, text.split()))
    return counts
