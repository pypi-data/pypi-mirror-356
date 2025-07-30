import click
import os
import json
from pathlib import Path

config_dir = r"C:\dbback"
snap_dir = os.path.join(config_dir, "snapshots")
metapath = os.path.join(config_dir, "metadata.json")

def load_metadata():
    try:
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        create_snap()
        if not os.path.exists(metapath) or os.path.getsize(metapath) == 0:
            with open(metapath, "w") as f:
                json.dump({}, f)
            return {}
        else:
            with open(metapath, "r") as f:
                return json.load(f)
    except Exception as e:
        click.echo(f"Error has occured {e}")
        return {}

def save_metadata(jsonval):
    with open(metapath, "w") as f:
        json.dump(jsonval, f, indent=4)


def create_snap():
    if not os.path.exists(snap_dir):
        os.makedirs(snap_dir)
    return

def check_exist(metadata,name,type,table):
        connec = metadata.get('connections',{})
        connec_type = connec.get(name,{})
        specific_conenc = connec_type.get(type,{})
        tables = specific_conenc.get('tables',{})
        if table not in tables:
            return False
        return True