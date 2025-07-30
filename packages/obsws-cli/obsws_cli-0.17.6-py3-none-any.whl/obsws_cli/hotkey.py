"""module containing commands for hotkey management."""

from typing import Annotated

import typer
from rich.table import Table

from . import console
from .alias import SubTyperAliasGroup

app = typer.Typer(cls=SubTyperAliasGroup)


@app.callback()
def main():
    """Control hotkeys in OBS."""


@app.command('list | ls')
def list_(
    ctx: typer.Context,
):
    """List all hotkeys."""
    resp = ctx.obj.get_hotkey_list()

    table = Table(title='Hotkeys', padding=(0, 2))
    table.add_column('Hotkey Name', justify='left', style='cyan')

    for hotkey in resp.hotkeys:
        table.add_row(hotkey)

    console.out.print(table)


@app.command('trigger | tr')
def trigger(
    ctx: typer.Context,
    hotkey: Annotated[
        str, typer.Argument(..., show_default=False, help='The hotkey to trigger')
    ],
):
    """Trigger a hotkey by name."""
    ctx.obj.trigger_hotkey_by_name(hotkey)


@app.command('trigger-sequence | trs')
def trigger_sequence(
    ctx: typer.Context,
    key_id: Annotated[
        str,
        typer.Argument(
            ...,
            show_default=False,
            help='The OBS key ID to trigger, see https://github.com/onyx-and-iris/obsws-cli?tab=readme-ov-file#hotkey for more info',
        ),
    ],
    shift: Annotated[
        bool, typer.Option(..., help='Press shift when triggering the hotkey')
    ] = False,
    ctrl: Annotated[
        bool, typer.Option(..., help='Press control when triggering the hotkey')
    ] = False,
    alt: Annotated[
        bool, typer.Option(..., help='Press alt when triggering the hotkey')
    ] = False,
    cmd: Annotated[
        bool, typer.Option(..., help='Press cmd when triggering the hotkey')
    ] = False,
):
    """Trigger a hotkey by sequence."""
    ctx.obj.trigger_hotkey_by_key_sequence(key_id, shift, ctrl, alt, cmd)
