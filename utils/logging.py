"""Utils for debugging.

Uses django's termcolors.

Available colors:

    color_names =
        'black',
        'red',
        'green',
        'yellow',
        'blue',
        'magenta',
        'cyan', 'white'

"""

from pprint import pprint
from typing import Any

from django.utils.termcolors import colorize


class TerminalLoggingMixin:
    """Mixin for terminal logging."""

    def make_bold(self, text: str, fg="red") -> str:
        """Return text as bolded."""
        return colorize(text, opts=("bold",), fg=fg)

    def pprint_symbols(self, symbol="=", symbol_repetition=42, color="green") -> None:
        """Print colorized symbol repeated."""
        print(
            colorize(symbol * symbol_repetition, opts=("bold",), fg=color, bg="black")
        )

    def pprint_label(
        self,
        label="Data",
        symbol="=",
        symbol_repetition=20,
        fg="green",
        bg="black",
    ) -> None:
        """Prints label string, surrounded by repeated symbols, colorized."""
        symboled_label = "{} {} {}".format(
            symbol * symbol_repetition, label, symbol * symbol_repetition
        )
        print(colorize(symboled_label, opts=("bold",), fg=fg, bg=bg))

    def pprint_data(self, data: Any, label="Data", fg="green", bg="black") -> None:
        """Pretty print data with label."""
        print()
        self.pprint_label(label=label, fg=fg, bg=bg)
        pprint(data)
        print()

    def pprint_response(
        self, response: Any, label="Response", fg="blue", bg="black"
    ) -> None:
        """Pretty print response, a shorthand for pprint_data(data=response, label='Response')"""
        self.pprint_data(data=response, label=label, fg=fg, bg=bg)

    def pprint_exception(
        self, exception: Exception, label="Exception", fg="red", bg="black"
    ) -> None:
        """Pretty print exception string.

        A shorthand for pprint_data(data=str(exception), label='Exception').
        """
        self.pprint_data(data=str(exception), label=label, fg=fg, bg=bg)

    def pprint_type(self, data: Any, label="Type", fg="magenta", bg="black") -> None:
        """Pretty print type of object data."""
        self.pprint_data(type(data), label=label, fg=fg, bg=bg)

    def pprint_dir(self, data: Any, label="dir(data)", fg="cyan", bg="black") -> None:
        """Pretty print dir(data)."""
        try:
            self.pprint_data(dir(data), label=label, fg=fg, bg=bg)
        except Exception:
            self.pprint_label(f"{data} has no .__dir__ attribute")

    def pprint_dict(
        self, data: Any, label="data.__dict__", fg="cyan", bg="black"
    ) -> None:
        """Pretty print data.__dict__."""
        try:
            self.pprint_data(data.__dict__, label=label, fg=fg, bg=bg)
        except Exception:
            self.pprint_label(label=f"{data} has no .__dict__ attribute", bg=bg)

    def pprint_breakpoint(self, label="BREAK POINT", symbol="*") -> None:
        """Print a break point line."""
        print()
        self.pprint_label(label, symbol=symbol, symbol_repetition=30, bg="red")
        print()

    def pprint_locals(self, local_vars: dict, label: str = "Local Variables") -> None:
        """Pretty print local variables `local_vars` from locals() returned dictionary.

        Sample invocation:
            self.pprint_locals(locals())
        """
        self.pprint_data(data=local_vars, label=label)

    def debugger(self, message="Paused in debugger") -> None:
        """Stop execution, mimiced from javascript `debugger` statement."""
        raise RuntimeError(message)

    def pprint_and_debug(self, data: Any, label="Data", fg="green", bg="black") -> None:
        """Pretty print data and raise RuntimeError for debuggin."""
        self.pprint_data(data=data, label=label, fg=fg, bg=bg)
        self.debugger()


terminal_logger = TerminalLoggingMixin()
