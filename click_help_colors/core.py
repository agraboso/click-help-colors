import re
import typing as t

import click

from .utils import _colorize, _extend_instance


class HelpColorsFormatter(click.HelpFormatter):
    options_regex = re.compile(r"-{1,2}[\w\-]+")

    def __init__(
        self,
        headers_color: t.Optional[str] = None,
        options_color: t.Optional[str] = None,
        options_custom_colors: t.Optional[t.Dict[str, str]] = None,
        *args: t.Any,
        **kwargs: t.Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self.headers_color = headers_color
        self.options_color = options_color
        self.options_custom_colors = options_custom_colors

    def _get_opt_names(self, option_name: str) -> t.List[str]:
        opts = self.options_regex.findall(option_name)
        if not opts:
            return [option_name]
        else:
            # Include this for backwards compatibility
            opts.append(option_name.split()[0])
            return opts

    def _pick_color(self, option_name: str) -> t.Optional[str]:
        opts = self._get_opt_names(option_name)
        for opt in opts:
            if self.options_custom_colors and (
                opt in self.options_custom_colors.keys()
            ):
                return self.options_custom_colors[opt]
        return self.options_color

    def write_usage(
        self, prog: str, args: str = "", prefix: t.Optional[str] = "Usage"
    ) -> None:
        colorized_prefix = _colorize(
            prefix if prefix is not None else "Usage",
            color=self.headers_color,
            suffix=": ",
        )
        super().write_usage(prog, args, prefix=colorized_prefix)

    def write_heading(self, heading: str) -> None:
        colorized_heading = _colorize(heading, color=self.headers_color)
        super().write_heading(colorized_heading)

    def write_dl(
        self, rows: t.Sequence[t.Tuple[str, str]], *args: t.Any, **kwargs: t.Any
    ) -> None:
        colorized_rows = [
            (_colorize(row[0], self._pick_color(row[0])), row[1]) for row in rows
        ]
        super().write_dl(colorized_rows, *args, **kwargs)


class HelpColorsCommand(click.Command):
    def __init__(
        self,
        help_headers_color: t.Optional[str] = None,
        help_options_color: t.Optional[str] = None,
        help_options_custom_colors: t.Optional[t.Dict[str, str]] = None,
        *args: t.Any,
        **kwargs: t.Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self.help_headers_color = help_headers_color
        self.help_options_color = help_options_color
        self.help_options_custom_colors = help_options_custom_colors

    def get_help(self, ctx: click.Context) -> str:
        formatter = HelpColorsFormatter(
            width=ctx.terminal_width,
            max_width=ctx.max_content_width,
            headers_color=self.help_headers_color,
            options_color=self.help_options_color,
            options_custom_colors=self.help_options_custom_colors,
        )
        self.format_help(ctx, formatter)
        return formatter.getvalue().rstrip("\n")


class HelpColorsGroup(HelpColorsCommand, click.Group):
    def command(self, *args: t.Any, **kwargs: t.Any) -> t.Any:
        kwargs.setdefault("cls", HelpColorsCommand)
        kwargs.setdefault("help_headers_color", self.help_headers_color)
        kwargs.setdefault("help_options_color", self.help_options_color)
        kwargs.setdefault("help_options_custom_colors", self.help_options_custom_colors)
        return super().command(*args, **kwargs)

    def group(self, *args: t.Any, **kwargs: t.Any) -> t.Any:
        kwargs.setdefault("cls", HelpColorsGroup)
        kwargs.setdefault("help_headers_color", self.help_headers_color)
        kwargs.setdefault("help_options_color", self.help_options_color)
        kwargs.setdefault("help_options_custom_colors", self.help_options_custom_colors)
        return super().group(*args, **kwargs)


class HelpColorsMultiCommand(HelpColorsCommand, click.MultiCommand):
    def resolve_command(
        self, ctx: click.Context, args: t.List[str]
    ) -> t.Tuple[t.Optional[str], t.Optional[click.Command], t.List[str]]:
        cmd_name, cmd, args[1:] = super().resolve_command(ctx, args)

        if not isinstance(cmd, HelpColorsCommand):
            if isinstance(cmd, click.Group):
                _extend_instance(cmd, HelpColorsGroup)
            if isinstance(cmd, click.Command):
                _extend_instance(cmd, HelpColorsCommand)

        if not getattr(cmd, "help_headers_color", None):
            cmd.help_headers_color = self.help_headers_color
        if not getattr(cmd, "help_options_color", None):
            cmd.help_options_color = self.help_options_color
        if not getattr(cmd, "help_options_custom_colors", None):
            cmd.help_options_custom_colors = self.help_options_custom_colors

        return cmd_name, cmd, args[1:]
