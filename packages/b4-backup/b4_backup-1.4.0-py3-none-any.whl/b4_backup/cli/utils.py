import json
import logging
import os
import shlex
from collections.abc import Generator
from contextlib import contextmanager
from enum import Enum
from pathlib import Path, PurePath
from typing import Any

import click
import rich
import typer
from rich.table import Table

from b4_backup import utils
from b4_backup.cli.init import app, init
from b4_backup.config_schema import DEFAULT, BaseConfig
from b4_backup.exceptions import BaseBtrfsBackupError
from b4_backup.main.dataclass import Snapshot

log = logging.getLogger("b4_backup.cli")


def validate_target(ctx: typer.Context, values: list[str]) -> list[str]:
    """A handler to validate target types."""
    config: BaseConfig = ctx.obj

    options = set(config.backup_targets) - {DEFAULT}
    for value in values:
        if value is not None and not any(PurePath(x).is_relative_to(value) for x in options):
            raise typer.BadParameter(f"Unknown target. Available targets are: {', '.join(options)}")

    return values


def _parse_arg(param: click.Argument | click.Option, args: list[str]) -> Any | list[Any]:
    args = list(args)
    parsed_arg = []

    if not any(opt in args for opt in param.opts):
        return param.default

    while any(opt in args for opt in param.opts):
        for opt in param.opts:
            if opt not in args:
                continue

            idx = args.index(opt)
            value = args[idx + 1]

            # Hacky conversion, because I just don't get what's going on in these click types
            if isinstance(param.type, click.types.Path):
                value = Path(value)

            parsed_arg.append(value)
            del args[idx]
            del args[idx]

    if param.multiple:
        return parsed_arg

    return parsed_arg[-1]


def parse_callback_args(app: typer.Typer, args: list[str]) -> dict[str, Any]:
    """
    Extract and parse args from the callback function.

    This function is a workaround to this issue:
    https://github.com/tiangolo/typer/issues/259
    tl;dr: Callback is not called before autocomplete functions, so we need to do it manually

    Args:
        app: Typer CLI instance
        args: Raw cli args

    Returns:
        Parsed parameters from callback
    """
    assert app.registered_callback is not None
    params = typer.main.get_params_convertors_ctx_param_name_from_function(
        app.registered_callback.callback
    )[0]

    parsed_args = {}
    for param in params:
        parsed_args[param.name] = _parse_arg(param, args)

    return parsed_args


def complete_target(ctx: typer.Context, incomplete: str) -> Generator[str, None, None]:
    """A handler to provide autocomplete for target types."""
    args = shlex.split(os.getenv("_TYPER_COMPLETE_ARGS", ""))
    parsed_args = parse_callback_args(app, args)
    init(ctx, **parsed_args)
    config: BaseConfig = ctx.obj

    options = set()
    for target in set(config.backup_targets) - {DEFAULT}:
        options.add(target)
        options |= {str(x) for x in PurePath(target).parents}

    options = sorted(options)
    taken_targets = ctx.params.get("target") or []
    for target in options:
        if str(target).startswith(incomplete) and target not in taken_targets:
            yield target


class ErrorHandler:
    """Handles errors during execution."""

    errors: list[Exception]

    def __init__(self) -> None:  # noqa: D107
        self.errors = []

    def add(self, exc: Exception) -> None:
        """
        Add exception to list.

        Args:
            exc: Exception to add
        """
        log.exception(exc)
        self.errors.append(exc)

    def finalize(self) -> None:
        """Raise errors if any exist."""
        if self.errors:
            raise ExceptionGroup("Errors during loop execution", self.errors)


@contextmanager
def error_handler():
    """A wrapper around the CLI error handler."""
    try:
        err_handler = ErrorHandler()
        yield err_handler
        err_handler.finalize()

    except BaseBtrfsBackupError as exc:
        log.debug("An error occured (%s)", type(exc).__name__, exc_info=exc)
        rich.print(f"[red]An error occured ({type(exc).__name__})")
        rich.print(exc)
        raise typer.Exit(1) from exc
    except Exception as exc:
        log.exception("An unknown error occured (%s)", type(exc).__name__)
        rich.print(f"[red]An unknown error occured ({type(exc).__name__})")
        rich.print(exc)
        raise typer.Exit(1) from exc


class OutputFormat(str, Enum):
    """An enumeration of supported output formats."""

    RICH = "rich"
    JSON = "json"
    RAW = "raw"

    @classmethod
    def output(
        cls,
        snapshots: dict[str, Snapshot],
        title: str,
        output_format: "OutputFormat",
    ) -> None:
        """
        Output the snapshots in the specified format.

        Args:
            snapshots: The snapshots to output
            title: The title of the output
            output_format: The format to output the snapshots in
        """
        if output_format == OutputFormat.RICH:
            cls.output_rich(snapshots, title)
        elif output_format == OutputFormat.JSON:
            cls.output_json(snapshots, title)
        else:
            cls.output_raw(snapshots, title)

    @classmethod
    def output_rich(cls, snapshots: dict[str, Snapshot], title: str) -> None:
        """Output the snapshots in a rich format."""
        table = Table(title=title)

        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("Subvolumes", style="magenta")

        for snapshot_name in sorted(snapshots, reverse=True):
            table.add_row(
                snapshot_name,
                "\n".join(
                    [str(PurePath("/") / x) for x in snapshots[snapshot_name].subvolumes_unescaped]
                ),
            )

        utils.CONSOLE.print(table)

    @classmethod
    def output_json(cls, snapshots: dict[str, Snapshot], title: str) -> None:
        """Output the snapshots in a JSON format."""
        utils.CONSOLE.print(
            json.dumps(
                {
                    "host": title.lower(),
                    "snapshots": {
                        snapshot_name: [
                            str(PurePath("/") / x) for x in snapshot.subvolumes_unescaped
                        ]
                        for snapshot_name, snapshot in snapshots.items()
                    },
                },
                sort_keys=True,
                indent=2,
            )
        )

    @classmethod
    def output_raw(cls, snapshots: dict[str, Snapshot], title: str) -> None:
        """Output the snapshots in a raw format."""
        utils.CONSOLE.print(
            "\n".join(
                [
                    f"{title.lower()} {snapshot_name} {str(PurePath(' / ') / subvolume)}"
                    for snapshot_name, snapshot in snapshots.items()
                    for subvolume in snapshot.subvolumes_unescaped
                ]
            )
        )
