import re
import typing as t

import click
from click import version_option as click_version_option

from .utils import _colorize

FC = t.TypeVar("FC", bound=t.Union[t.Callable[..., t.Any], click.Command])


def version_option(
    version: t.Optional[str] = None,
    prog_name: t.Optional[str] = None,
    message: str = "%(prog)s, version %(version)s",
    message_color: t.Optional[str] = None,
    prog_name_color: t.Optional[str] = None,
    version_color: t.Optional[str] = None,
    **kwargs: t.Any,
) -> t.Callable[[FC], FC]:
    """
    :param prog_name_color: color of the prog_name.
    :param version_color: color of the version.
    :param message_color: default color of the message.

    for other params see Click's version_option decorator:
    https://click.palletsprojects.com/en/7.x/api/#click.version_option
    """
    msg_parts = []
    for s in re.split(r"(%\(version\)s|%\(prog\)s)", message):
        if s == "%(prog)s":
            msg_parts.append(_colorize(prog_name, prog_name_color or message_color))
        elif s == "%(version)s":
            msg_parts.append(_colorize(version, version_color or message_color))
        else:
            msg_parts.append(_colorize(s, message_color))
    message = "".join(msg_parts)

    return click_version_option(
        version=version, prog_name=prog_name, message=message, **kwargs
    )
