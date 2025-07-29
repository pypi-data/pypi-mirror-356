from __future__ import annotations

import os
from typing import Any

import click

import greennode

from greennode.constants import TIMEOUT_SECS, MAX_RETRIES


def print_version(ctx: click.Context, params: Any, value: Any) -> None:
    if not value or ctx.resilient_parsing:
        return
    click.echo(f"Version {greennode.version}")
    ctx.exit()


@click.group()
@click.pass_context
@click.option(
    "--api-key",
    type=str,
    help="API Key. Defaults to environment variable `GREENNODE_API_KEY`",
    default=os.getenv("GREENNODE_API_KEY"),
)
@click.option(
    "--base-url", type=str, help="API Base URL. Defaults to GreenNode AI Platform endpoint."
)
@click.option(
    "--timeout", type=int, help=f"Request timeout. Defaults to {TIMEOUT_SECS} seconds"
)
@click.option(
    "--max-retries",
    type=int,
    help=f"Maximum number of HTTP retries. Defaults to {MAX_RETRIES}.",
)
@click.option(
    "--version",
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
    help="Print version",
)
@click.option("--debug", help="Debug mode", is_flag=True)
def main(ctx: click.Context,
         api_key: str | None,
         base_url: str | None,
         timeout: int | None,
         max_retries: int | None,
         debug: bool | None, ) -> None:
    """This is a sample CLI tool."""
    greennode.log = "debug" if debug else None
    ctx.obj = greennode.GreenNode(
        api_key=api_key, base_url=base_url, timeout=timeout, max_retries=max_retries
    )
    pass


if __name__ == "__main__":
    main()
