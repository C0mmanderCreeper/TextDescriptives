import string
import random
from typing import List, Union, cast

from spacy.tokens import Span
from textdescriptives.components.quality import symbol_to_word_ratio


class FakeToken:
    def __init__(self, text: str):
        self.text = text
        # A token is considered whitespace if it consists solely of whitespace.
        self.is_space = text.isspace()
        # A token is considered punctuation if all characters are in string.punctuation.
        self.is_punct = all(char in string.punctuation for char in text) if text else False

    def __repr__(self):
        return f"FakeToken({self.text!r})"


class FakeSpan:
    def __init__(self, tokens: List[FakeToken]):
        self.tokens = tokens
        # We set span.text as the concatenation of the individual token texts, separated by a space.
        self.text = " ".join(token.text for token in tokens)

    def __iter__(self):
        return iter(self.tokens)

    def __repr__(self):
        return f"FakeSpan({self.tokens!r})"


def create_fake_span(text: str) -> FakeSpan:
    """
    Creates a FakeSpan by splitting the input text on whitespace.
    Each substring is treated as a FakeToken.
    """
    # Simply split by whitespace – a basic tokenization.
    tokens = [FakeToken(token) for token in text.split()]
    return FakeSpan(tokens)


def fuzz_function(iterations: int = 1000, text_max_size: int = 100):
    error_count = 0
    for i in range(iterations):
        # Generate a random text of length between 0 and text_max_size characters from string.printable.
        random_text = ''.join(random.choices(string.printable, k=random.randint(0, text_max_size)))
        # Select a random symbol from string.printable.
        random_symbol = random.choice(string.printable)
        span = create_fake_span(random_text)
        try:
            # Cast FakeSpan to Span for the type checker.
            result = symbol_to_word_ratio(cast(Span, span), random_symbol)
        except Exception as e:
            error_count += 1
            print(f"[Error] Iteration {i}: text={random_text!r}, symbol={random_symbol!r} -> Exception: {e}")
        else:
            print(f"Iteration {i}: text={random_text!r}, symbol={random_symbol!r} -> Result: {result}")
    print(f"\nFuzzing completed. Erroneous runs: {error_count} out of {iterations}")


if __name__ == '__main__':
    fuzz_function(100000, 1000)
