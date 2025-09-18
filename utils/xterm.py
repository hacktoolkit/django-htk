class AnsiColor:
    """ANSI color/styling helpers for terminal output."""

    # Control
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"
    INVERT = "\033[7m"

    # Foreground (normal)
    FG = {
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
    }

    # Foreground (bright)
    FG_BRIGHT = {
        "black": "\033[90m",
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
    }

    # Background (normal)
    BG = {
        "black": "\033[40m",
        "red": "\033[41m",
        "green": "\033[42m",
        "yellow": "\033[43m",
        "blue": "\033[44m",
        "magenta": "\033[45m",
        "cyan": "\033[46m",
        "white": "\033[47m",
    }

    # Background (bright)
    BG_BRIGHT = {
        "black": "\033[100m",
        "red": "\033[101m",
        "green": "\033[102m",
        "yellow": "\033[103m",
        "blue": "\033[104m",
        "magenta": "\033[105m",
        "cyan": "\033[106m",
        "white": "\033[107m",
    }

    @classmethod
    def code_fg(cls, name: str | None, *, bright: bool = False) -> str:
        """Return the ANSI code for a foreground color; unknown names -> ''."""
        if not name:
            return ""
        name = name.lower()
        return (cls.FG_BRIGHT if bright else cls.FG).get(name, "")

    @classmethod
    def code_bg(cls, name: str | None, *, bright: bool = False) -> str:
        """Return the ANSI code for a background color; unknown names -> ''."""
        if not name:
            return ""
        name = name.lower()
        return (cls.BG_BRIGHT if bright else cls.BG).get(name, "")

    @classmethod
    def style(
        cls,
        *,
        bold: bool = False,
        dim: bool = False,
        underline: bool = False,
        invert: bool = False,
    ) -> str:
        """Return style codes composed; omit any that are False."""
        parts = []
        if bold:
            parts.append(cls.BOLD)
        if dim:
            parts.append(cls.DIM)
        if underline:
            parts.append(cls.UNDERLINE)
        if invert:
            parts.append(cls.INVERT)
        return "".join(parts)

    @classmethod
    def colorize(
        cls,
        text: str,
        *,
        fg: str | None = None,
        bg: str | None = None,
        fg_bright: bool = False,
        bg_bright: bool = False,
        bold: bool = False,
        dim: bool = False,
        underline: bool = False,
        invert: bool = False,
        reset: bool = True,
    ) -> str:
        """
        Wrap `text` with ANSI codes. Unknown color names are ignored (sensible default).
        By default, appends RESET to avoid leaking styles into subsequent output.
        """
        prefix = "".join(
            (
                cls.code_fg(fg, bright=fg_bright),
                cls.code_bg(bg, bright=bg_bright),
                cls.style(
                    bold=bold, dim=dim, underline=underline, invert=invert
                ),
            )
        )
        suffix = cls.RESET if reset else ""
        return f"{prefix}{text}{suffix}"

    @classmethod
    def c(cls, text: str, *args, **kwargs) -> str:
        """Colorize text with ANSI codes."""
        return cls.colorize(text, *args, **kwargs)
