import click
import sys
from rich.console import Console
from rich.table import Table
import mysql.connector
from collections import deque
from . import configs

@click.command()
@click.option("--name",prompt='Project Name')
@click.option("--type",prompt='DBMS Name')
@click.option("--table",prompt='Table Name')
@click.pass_context
def add(ctx:click.Context,name,type,table):
    '''Add a new table to a present '''    
    name = name.lower()
    type = type.lower()
    table = table.lower()
    metadata = ctx.obj['metadata']
    dbmslis = metadata.get('connections',{})
    projects = dbmslis.get(name,{})
    specific_project = projects.get(type,{})

    #Checking if such a project exists
    if len(specific_project) == 0:
        click.echo(f"Given Project {name} or DBMS {type} is not tracked.")
        sys.exit(1)
    
    #Checking if table exists in DB
    if checking_tables(specific_project['type'],specific_project,table):
        if table in specific_project['tables']:
            click.echo(f"Given table {table} exists in Project {name}.")
        else:
            metadata['connections'][name][type]['tables'][table] = []
            configs.save_metadata(metadata)
            click.echo(f"Table {table} added successfully")
    else:
        click.echo(f"Given {table} doesnt exist in DB")

@click.command()
@click.option("--name",prompt='Project Name')
@click.option("--type",prompt='DBMS Name')
@click.pass_context
def list(ctx:click.Context,name,type):
    '''List all tables that have been added to a particular Project'''
    name = name.lower()
    type = type.lower()
    metadata = ctx.obj['metadata']
    dbmslis = metadata.get('connections',{})
    projects = dbmslis.get(name,{})
    specific_project = projects.get(type,{})
    if len(specific_project) == 0:
        click.echo(f"Given Project {name} or DBMS {type} is not tracked.")
        sys.exit(1)
    
    table = Table(title=f"Tables tracked in {name}")
    table.add_column('Name of Table')
    table.add_column('No of Snapshots')
    table.add_column('Last Snapshot Date and Time')
    for i in specific_project['tables']:
        table_snap_details = specific_project['tables'][i]
        table.add_row(i,str(len(table_snap_details)),(table_snap_details[-1] if len(table_snap_details) > 0 else "None"))
    console = Console()
    console.log(table)

@click.command()
@click.option("--name",prompt="Project Name")
@click.option("--type",prompt='DBMS type')
@click.option("--table",prompt="Table Name")
@click.pass_context
def delete(ctx:click.Context,name,type,table):
    name = name.lower()
    type = type.lower()
    table = table.lower()
    metadata = ctx.obj['metadata']
    connec = metadata.get('connections',{})
    specific_connection = connec.get(name,{})
    specific_project = specific_connection.get(type,{})
    tables_set =specific_project.get('tables',{})
    if len(tables_set) == 0:
        click.echo('Project or DBMS type doesnt exist')
        sys.exit(1)
        return
    
    if table not in tables_set:
        click.echo('Specified table not tracked')
        sys.exit(1)
        return
    
    vals = len(tables_set[table])
    if(click.confirm(f"Deleting table, will delete {vals} snapshots.")):
        del metadata['connections'][name][type]['tables'][table]
        configs.save_metadata(metadata)
    else:
        click.echo('Exiting .....')


def checking_tables(type,details,tablename):
    try:
        if type=='mysql':
            conn = mysql.connector.connect(host=details['host'], user=details['user'], password=details['password'], database=details['database'])
            cursor = conn.cursor()
            query = f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{tablename}' AND TABLE_SCHEMA = '{details['database']}';"
            cursor.execute(query)
            value = cursor.fetchone()
            conn.close()
            if value[0] == 0:
                return False
            return True
    except Exception as e:
        return False
