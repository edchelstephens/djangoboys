"""Numbers and calculation utils."""


class NumbersUtilMixin:
    """Numbers util mixin."""

    def is_even(self, number: int) -> bool:
        """Check if number is even."""
        return number % 2 == 0

    def is_odd(self, number: int) -> bool:
        """Check if number is odd."""
        return not self.is_even(number)


number_utils = NumbersUtilMixin()
