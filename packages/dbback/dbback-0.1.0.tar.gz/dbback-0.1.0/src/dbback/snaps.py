import click
import sys
from datetime import datetime
import mysql.connector
import os
import random
import pathlib
from rich.console import Console
from rich.table import Table
from . import configs

@click.command()
@click.option("--name",prompt="Project Name")
@click.option("--type",prompt='DBMS type')
@click.option("--table",prompt="Table Name")
@click.pass_context
def add(ctx:click.Context, name:str, type:str, table:str):
    '''Take the snapshot of a tracked table'''
    try:
        name = name.lower()
        type= type.lower()
        table = table.lower()
        metadata = ctx.obj['metadata']
        if not configs.check_exist(metadata,name,type,table):
            click.echo('Project or Table not being tracked properly')
            sys.exit(1)
        
        if type == 'mysql':
            now = datetime.now()
            current_date = now.strftime("%Y-%m-%d")
            current_time = now.strftime("%H-%M-%S")
            number = random.randint(10**9, 10**10 - 1)
            snapname = click.prompt('Name of Snapshot',type=str,default=f"snapshot_{name}_{type}_{table}")
            snapname = snapname.lower()
            new_file_name = snapname + "__" + str(number) + "__" + current_date + "__" + current_time+'.sql'
            snap_dir = r'C:\dbback\snapshots'
            snap_project_dir = os.path.join(snap_dir,name)
            snap_sqldb_dir = os.path.join(snap_project_dir,type)
            snap_table_dir = os.path.join(snap_sqldb_dir,table)

            if not os.path.exists(snap_project_dir):
                os.makedirs(snap_project_dir)
                os.makedirs(snap_sqldb_dir)
                os.makedirs(snap_table_dir)
            elif not os.path.exists(snap_sqldb_dir):
                os.makedirs(snap_sqldb_dir)
                os.makedirs(snap_table_dir)
            elif not os.path.exists(snap_table_dir):
                os.makedirs(snap_table_dir)
                
            file_path = os.path.join(snap_table_dir, new_file_name)
            f = open(file_path,'x')
            result = taking_snapshot(metadata['connections'][name][type],type,table,file_path)
            if not result:
                os.remove(file_path)
                raise Exception("Not working")
            metadata['connections'][name][type]['tables'][table].append(new_file_name)
            configs.save_metadata(metadata)
            click.echo('Snapshot taken successfully')

    except Exception as e:
        click.echo(f"Try again later, System Error {e}")
        sys.exit(1)

def taking_snapshot(details,type,table,output_file):
    try:
        if type=='mysql':
            conn = mysql.connector.connect(
                host=details['host'],
                user=details['user'],
                password=details['password'],
                database=details['database']
            )
            cursor = conn.cursor()
            cursor.execute(f'Select * from {table}')
            rows = cursor.fetchall()
            col_names = [desc[0] for desc in cursor.description]
            with open(output_file, "w") as f:
                    for row in rows:
                        values = ', '.join([f"'{str(val).replace("'", "''")}'" if val is not None else "NULL" for val in row])
                        f.write(f"INSERT INTO {table} ({', '.join(col_names)}) VALUES ({values});\n")
        return True
    except Exception as e:
        print(e)
        return False




@click.command()    
@click.option("--name",prompt="Project Name")
@click.option("--type",prompt='DBMS type')
@click.option("--table",prompt="Table Name")
@click.option("--row_cnt",prompt="Count of Snapshots",type=int,default="5")
@click.pass_context
def list(ctx:click.Context,name,type,table,row_cnt):
    '''List of Snapshots from a table'''
    metadata = ctx.obj['metadata']
    name = name.lower()
    type= type.lower()
    table = table.lower()
    console = Console()
    if not configs.check_exist(metadata,name,type,table):
        click.echo(f"{table} from {name} in {type} is not tracked")
        sys.exit(1)
    
    connec = metadata['connections']
    project = connec[name]
    specific_db = project[type]
    table_list = specific_db['tables']
    snap_list = table_list[table]
    table = Table(title=f"Snapshots from {table} in {name} under {type}")
    table.add_column('Snapshot ID')
    table.add_column('Snapshot Name')
    table.add_column('Date(YYYY-MM-DD)',)
    table.add_column('Time(HH-MM-SS)')
    print(snap_list)
    snap_cnt = len(snap_list)
    for i in range(min(row_cnt,snap_cnt)):
        snap_name = snap_list[snap_cnt-i-1]
        snap_name = snap_name[:-4]
        snap_details = snap_name.split('__')
        table.add_row(snap_details[1],snap_details[0],snap_details[2],snap_details[3])
    console.log(table)
    return

@click.command()    
@click.option("--name",prompt="Project Name")
@click.option("--type",prompt='DBMS type')
@click.option("--table",prompt="Table Name")
@click.option("--row_cnt",prompt="Snapshot ID ",default='1')
@click.pass_context
def restore(ctx:click.Context,name,type,table,row_cnt):
    metadata = ctx.obj['metadata']
    name = name.lower() 
    type= type.lower()  
    table = table.lower()
    if not configs.check_exist(metadata,name,type,table):
        click.echo(f"{table} from {name} in {type} is not tracked")
        sys.exit(1)
    
    project_list = metadata.get('connections',{})
    specific_project = project_list.get(name,{})
    db_project = specific_project.get(type,{})
    tables_list = db_project.get('tables',{})
    snap_details = tables_list.get(table,{})
    for i in snap_details:
        split_val = i.split('__')
        if split_val[1] == row_cnt:
            file_path = get_file_path(i,name,type,table)
            if len(file_path) != 0:
                if change_table(file_path,name,type,table,db_project):
                    click.echo('Successfully restored!')
                else:
                    click.echo('System Error, Check Details and Try again!')
            else:
                click.echo('Error in the system, Try Later')
            
def get_file_path(file_name,name,type,table):
    snap_dir = r'C:\dbback\snapshots'
    name_dir = os.path.join(snap_dir,name)
    type_dir = os.path.join(name_dir,type)
    table_dir = os.path.join(type_dir,table)
    file_path = os.path.join(table_dir,file_name)
    if os.path.exists(file_path):
        return file_path
    return ''

    

def change_table(file_name, name, type, table, details):
    try:
        if type=='mysql':
            conn = mysql.connector.connect(host=details['host'], user=details['user'], password=details['password'], database=details['database'])
            cursor = conn.cursor()
            cursor.execute(f"Truncate table {table}")
            conn.commit()
            with open(file_name,"r") as f:
                statement = ''
                for line in f:
                    checked = line.strip()
                    if not checked or checked.startswith('--'):
                        continue
                    statement += line
                    if checked.endswith(';'):
                        cursor.execute(statement)
                        conn.commit()
                        statement = ''
            return True
    except Exception as e:
        print(e)
        return False
        