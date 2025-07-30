import click
from . import configs
from rich.console import Console
from rich.table import Table
import sys
import asyncio
import asyncpg
import mysql.connector

@click.command()
@click.option("--name", prompt="Project Name", help="A short unique name for this DB connection")
@click.option("--type", prompt="Database type (postgres/mysql)", help="Type of database")
@click.option("--host", prompt="Host", help="Hostname or IP",default='localhost')
@click.option("--port", prompt="Port", type=int, help="Database port")
@click.option("--user", prompt="Username", help="DB username", default='root')
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True, help="DB password")
@click.option("--database", prompt="Database name", help="Name of the DB to connect")
@click.pass_context
def add(ctx:click.Context,name:str, type:str, host:str, port:int, user:str, password:str, database:str):
    """Add a new database connection"""
    name = name.lower()
    type = type.lower()
    host = host.lower()
    user = user.lower()
    password = password.lower()
    database = database.lower()

    #Mimiking a json -> Will obtain via
    metadata = ctx.obj['metadata']
    connections = metadata.get("connections", {})
    if name in connections and type in connections[name]:
        click.echo(f"A project under the database {type} already exists. Choose another name.")
        return
    
    valtoadd = {
        "name":name,
        "type": type,
        "host": host,
        "port": port,
        "user": user,
        "password": password,
        "database": database,
        "tables":{},
    }

    result = checking_connections(type,valtoadd)
    if result:
        if name not in connections:
            connections[name] = {}
        connections[name][type] = valtoadd
        
        metadata['connections'] = connections
        configs.save_metadata(metadata)
        click.echo(f"Connection '{name}' saved successfully.")
    else:
        click.echo("There are no projects with given details in DB")


@click.command()
@click.pass_context
def list(ctx):
    '''Listing the various different connections enabled'''
    projectlist = []
    metadata = ctx.obj['metadata']
    connections = metadata.get('connections',{})
    for i in connections:
        projectlist.append(i)


    click.echo('Please choose from the give option to list')
    for i,n in enumerate(projectlist):
        click.echo(f"{i+1}.{n.title()}")
    listlen = len(projectlist) + 1
    click.echo(str(listlen) + ".All")

    val = click.prompt('Please enter the option',default=listlen)
    while val > listlen or val<=0:
        val = click.prompt('Please enter a proper option',default=listlen)
    
    
    colname = ['Name','Type','Host','Port','User','Database Name']
    if val == listlen:
        for i in connections:
            table = Table(title=f"{i} Connections")
            for j in colname:
                table.add_column(j)
            
            projects = connections.get(i)
            for k in projects:
                table.add_row(projects[k]['name'].title()
                              ,projects[k]['type'].title()
                              ,projects[k]['host'].title()
                              ,str(projects[k]['port'])
                              ,projects[k]['user'].title()
                              ,projects[k]['database'].title()
                              )
            console = Console()
            console.print(table)
            console.print("\n")
    else:
        for i,n in enumerate(connections):
            if i+1==val:
                table = Table(title=f"{n} Connections")
                for j in colname:
                    table.add_column(j)
                
                projects = connections.get(n)
                for k in projects:
                    table.add_row(projects[k]['name'].title()
                              ,projects[k]['type'].title()
                              ,projects[k]['host'].title()
                              ,str(projects[k]['port'])
                              ,projects[k]['user'].title()
                              ,projects[k]['database'].title()
                              )
                console = Console()
                console.print(table)
                console.print("\n")


@click.command()
@click.option("--name",prompt='Enter the Name of the Project')
@click.option("--type",prompt='Enter the DBMS',default='Mysql,Postgresql,MongoDB')
@click.pass_context
def delete(ctx:click.Context, type, name):
    '''Deleting the various connections enabled'''
    name = name.lower()
    type = type.lower()
    if len(name) == 0:
        click.echo("Please use 'list' to display the various projects present")
        sys.exit(1)
    
    metadata = ctx.obj['metadata']
    connecdict = metadata['connections']
    try:
        for i in connecdict:
            if i==name:
                prodict = connecdict[i]
                if type in prodict:
                    if click.confirm(f'Confirm deletion of the Project {name} in {type}'):
                        del metadata['connections'][i][type]
                        configs.save_metadata(metadata)
                    else:
                        click.echo("Please start over again if required")
                        sys.exit(1)
                else:
                    click.echo("Given 'Project Name' doesnt Exit.")
                    sys.exit(1)
    except Exception as e:
        click.echo('System error has occured')


def checking_connections(type,details):
    try:
        if type=='mysql':
            conn = mysql.connector.connect(host=details['host'], user=details['user'], password=details['password'], database=details['database'])
            conn.close()
            return True
        elif type=='postgresql':
            db_url = f"postgresql+asyncpg://{details['user']}:{details['password']}@{details['host']}:{details['port']}/{details['database']}"
            return asyncio.run(check_connection(db_url))
    except Exception as e:
        return False

async def check_connection(details):
    try:
        conn = await asyncpg.connect(details['user'], password=details['password'], database=details['database'], host=details['host'])
        await conn.execute('SELECT 1')
        await conn.close()
        return True
    except Exception as e:
        return False