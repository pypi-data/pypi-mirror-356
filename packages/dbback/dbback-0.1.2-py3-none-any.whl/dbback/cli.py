import click
from . import configs
from . import connec
from . import snaps
from . import tables
import os   

@click.group()
@click.version_option()
@click.pass_context
def cli(ctx: click.Context):
    ctx.ensure_object(dict)

@cli.group()
@click.pass_context
def connection(ctx):
    metadata = configs.load_metadata()
    ctx.obj['metadata'] = metadata

@cli.group()
@click.pass_context
def table(ctx):
    metadata = configs.load_metadata()
    ctx.obj['metadata'] = metadata

@cli.group()
@click.pass_context
def snapshot(ctx):
    metadata = configs.load_metadata()
    ctx.obj['metadata'] = metadata


connection.add_command(connec.add)
connection.add_command(connec.list)
connection.add_command(connec.delete)

table.add_command(tables.add)
table.add_command(tables.list)
table.add_command(tables.delete)

snapshot.add_command(snaps.add)
snapshot.add_command(snaps.list)
snapshot.add_command(snaps.restore)