"""Generate a simple gradient of text with two colors.

This module provides the `SimpleGradient` class that generates a gradient of text with two colors.

"""

# ruff: noqa: F401
import re
from functools import partial
from typing import Dict, Iterable, List, Literal, Optional, Tuple, Union

import rich.style
from rich import get_console
from rich.cells import cell_len
from rich.color import Color as RichColor
from rich.console import Console, ConsoleOptions, JustifyMethod, OverflowMethod, RenderableType
from rich.control import strip_control_codes
from rich.measure import Measurement
from rich.segment import Segment
from rich.style import Style, StyleType
from rich.text import Span, Text
from operator import itemgetter

from rich_gradient.color import Color, ColorType

# ColorType = Union[ColorTuple, str, BaseColor, Color]
GradientMethod = Literal["default", "list", "mono", "rainbow"]
DEFAULT_JUSTIFY: JustifyMethod = "default"
DEFAULT_OVERFLOW: OverflowMethod = "fold"
WHITESPACE_REGEX = re.compile(r"^\s+$")
ColorInput = Union[ColorType, "Color"]
VERBOSE: bool = False


def pick_bool(*args):
    for arg in args:
        if arg is not None:
            return arg
    return False


class SimpleGradient(Text):
    """
    Text with gradient with two colors.

    Args:
        text (Text|str): The text to print. Defaults to `""`.
        color1 (ColorType): The first color.
        color2 (ColorType): The second color.
        justify (JustifyMethod, optional): Justify method. Defaults to "default".
        overflow (OverflowMethod, optional): Overflow method. Defaults to "crop".
        no_wrap (bool, optional): Disable wrapping. Defaults to False.
        style (StyleType, optional): The style of the gradient text. Defaults to None.
        end (str, optional): The end character. Defaults to " ".
    """

    __slots__ = (
        "color1",
        "color2",
        "_text",
        "_length",
        "_spans",
        "end",
        "verbose",
        "_style"
    )

    def __init__(
        self,
        renderable: RenderableType = "",
        *,
        color1: ColorType | Color,
        color2: ColorType | Color,
        justify: JustifyMethod = "default",
        overflow: OverflowMethod = "fold",
        no_wrap: bool = False,
        style: StyleType = Style.null(),
        end: str = "",
        spans: Optional[List[Span]] = None,
        verbose: bool = False,
    ) -> None:
        self.verbose = verbose
        console = get_console()
        # If already a Text, use as is, else extract as Text using console
        text_obj: Text
        if isinstance(renderable, Text):
            text_obj = renderable
        else:
            # Render the renderable to a Text object using console
            text_obj = console.render_str(str(renderable))
        # Now, set up self._text, self._length, self._spans
        self._length = text_obj._length
        self._text = text_obj._text
        self._spans = text_obj.spans
        _style = Style.parse(style) if isinstance(style, str) else style

        super().__init__(
            text=self.plain,
            style=_style,
            justify=justify,
            overflow=overflow,
            no_wrap=no_wrap,
            end=end,
            spans=spans,
        )

        if not isinstance(color1, Color):
            color1 = Color(color1)  # type: ignore
        if not isinstance(color2, Color):
            color2 = Color(color2)  # type: ignore

        self.color1 = Color(color1)  # type: ignore
        self.color2 = Color(color2)  # type: ignore
        self._spans = list(self.generate_spans())

    def __len__(self) -> int:
        """Return the length of the text.

        Returns:
            int: The length of the text.
        """
        return self._length

    def __repr__(self) -> str:
        """Return the string representation of the SimpleGradient.

        Returns:
            str: The string representation of the SimpleGradient.
        """
        return f"SimpleGradient({self.plain!r}, {self.color1.as_named()!r}, {self.color2.as_named()!r})"

    def __add__(self, other) -> "Text":
        """Add two Text objects together.

        Args:
            other (Any): The other object to add.

        Returns:
            Text: The concatenated Text object.
        """
        if isinstance(other, str):
            new_text = self.text + other
            return SimpleGradient(
                new_text,
                color1=self.color1,
                color2=self.color2,
                style=self.style,
                justify=self.justify or DEFAULT_JUSTIFY,
                overflow=self.overflow or DEFAULT_OVERFLOW,
                no_wrap=self.no_wrap or False,
                end=self.end,
            )
        if isinstance(other, (Text)):
            result = self.copy()
            result.append(other)
            return result
        return NotImplemented

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Text):
            return NotImplemented
        return self.plain == other.plain and self._spans == other._spans

    @property
    def text(self) -> str:
        """
        Returns the concatenated string representation of the `_text` attribute.

        Returns:
            str: The concatenated string representation of the `_text` attribute.
        """
        return "".join(self._text)

    @text.setter
    def text(self, value: str | Text) -> None:
        """
        Setter for the text attribute.

        Args:
            value (str|Text): The value to set for the text attribute.

        Returns:
            None
        """
        if isinstance(value, list):
            value = "".join(value)
        if isinstance(value, Text):
            sanitized_text = strip_control_codes(value.plain)
            self._length = value._length
            self._text = value._text
            self._spans = value.spans
        elif isinstance(value, str):
            if value == "":
                raise ValueError("Text cannot be empty.")
            sanitized_text = strip_control_codes(value)
            self._length = len(sanitized_text)
            self._text = list(sanitized_text)
        elif value is None:
            raise ValueError("Text cannot be None.")
        else:
            raise TypeError(f"Text must be a string or Text, not {type(value)}")

    @property  # type: ignore
    def style(self) -> Style:
        """The style of the gradient."""
        return self._style

    @style.setter
    def style(self, style: StyleType) -> None:
        """
        Setter for the style attribute.

        Args:
            style (StyleType): The value to set for the style attribute.
        """
        if style is None:
            self._style: Style = Style.null()
        elif isinstance(style, rich.style.Style):
            self._style = style
        else:
            self._style = Style.parse(style)

    def generate_spans(self):
        """
        Generate the gradient's spans.

        Args:
            None

        Returns:
            List[Span]: The gradient's spans
        """
        if self.verbose:
            console.log("Entered generate_gradient")
        triplet1 = self.color1.as_triplet()
        r1, g1, b1 = triplet1
        triplet2 = self.color2.as_triplet()
        r2, g2, b2 = triplet2
        dr: int = r2 - r1
        dg: int = g2 - g1
        db: int = b2 - b1

        for index in range(self._length):
            blend: float = index / self._length
            red: int = int(r1 + (dr * blend))
            green: int = int(g1 + (dg * blend))
            blue: int = int(b1 + (db * blend))
            hex_str: str = f"#{red:02X}{green:02X}{blue:02X}"
            style = Style(color=hex_str) + self.style
            yield Span(index, index + 1, style)

    def __rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> Iterable[Segment]:
        tab_size: int = console.tab_size or self.tab_size or 8
        justify = self.justify or options.justify or DEFAULT_JUSTIFY

        overflow = self.overflow or options.overflow or DEFAULT_OVERFLOW

        lines = self.wrap(
            console,
            options.max_width,
            justify=justify,
            overflow=overflow,
            tab_size=tab_size or 8,
            no_wrap=pick_bool(self.no_wrap, options.no_wrap, False),  # type: ignore
        )
        all_lines = Text("\n").join(lines)
        yield from all_lines.render(console, end=self.end)

    def __rich_measure__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> Measurement:
        text: str = self.plain
        lines: List[str] = text.splitlines()
        max_text_width = max(cell_len(line) for line in lines) if lines else 0
        words = text.split()
        min_text_width = (
            max(cell_len(word) for word in words) if words else max_text_width
        )
        return Measurement(min_text_width, max_text_width)

    def render(self, console: "Console", end: str = "") -> Iterable["Segment"]:
        """Render the text as Segments.

        Args:
            console (Console): Console instance.
            end (Optional[str], optional): Optional end character.

        Returns:
            Iterable[Segment]: Result of render that may be written to the console.
        """
        _Segment = Segment
        text = str.strip(self.plain)
        if not self._spans:
            yield Segment(text)
            if end:
                yield _Segment(end)
            return
        get_style = partial(console.get_style, default=Style.null())

        enumerated_spans = list(enumerate(self._spans, 1))
        style_map = {index: get_style(span.style) for index, span in enumerated_spans}
        style_map[0] = get_style(self.style)

        spans = [
            (0, False, 0),
            *((span.start, False, index) for index, span in enumerated_spans),
            *((span.end, True, index) for index, span in enumerated_spans),
            (len(text), True, 0),
        ]
        spans.sort(key=itemgetter(0, 1))

        stack: List[int] = []
        stack_append = stack.append
        stack_pop = stack.remove

        style_cache: Dict[Tuple[Style, ...], Style] = {}
        style_cache_get = style_cache.get
        combine = Style.combine

        def get_current_style() -> Style:
            """Construct current style from stack."""
            styles = tuple(style_map[_style_id] for _style_id in sorted(stack))
            cached_style = style_cache_get(styles)
            if cached_style is not None:
                return cached_style
            current_style = combine(styles)
            style_cache[styles] = current_style
            return current_style

        for (offset, leaving, style_id), (next_offset, _, _) in zip(spans, spans[1:]):
            if leaving:
                stack_pop(style_id)
            else:
                stack_append(style_id)
            if next_offset > offset:
                yield _Segment(text[offset:next_offset], get_current_style())
        if end:
            yield _Segment(end)

    def as_text(self, style: StyleType, end: str = "") -> Text:
        return Text(self.plain, spans=self._spans, style=style, end=end)


if __name__ == "__main__":  # pragma: no cover
    from rich.panel import Panel

    from rich_gradient.theme import GRADIENT_TERMINAL_THEME

    console = Console(width=64, record=True)
    sample_text = "SimpleGradient is a class that prints a `string` \nor `rich.text.Text` object as a gradient from \ncolor1 to color2 with an optional style."
    gradient = SimpleGradient(
        sample_text, color1="green", color2="cyan", style="bold", justify="center"
    )  # type: ignore
    gradient.highlight_regex(r"(`.+`)", "#af00ff")
    console.line()
    console.print(
        Panel(
            gradient,
            padding=(1, 4),
            title=SimpleGradient(
                "SimpleGradient", color1="#ff9900", color2="#ffff00", style="bold"
            ),
        ),
        justify="center",
    )
    console.line()
    console.save_svg(
        "docs/img/simple_gradient.svg",
        title="Rich Gradient",
        theme=GRADIENT_TERMINAL_THEME,
    )
