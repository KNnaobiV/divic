import datetime
import json
import os
import subprocess

from frappe import get_site_config

from task_manager.utils import get_logger
APP_PATH = os.path.dirname(os.path.dirname(__file__))



logger = get_logger(name="root", loglevel='INFO')



def get_dir_path(dirname, path_name):
    dirname = os.path.dirname(dirname)
    dir = dirname.split("/")[-1]
    if dir.lower() != path_name.lower():
        return get_dir_path(dirname, path_name)
    return dirname


def get_site_config_file(site_name):
    frappe_dir = get_dir_path(APP_PATH, "frappe-bench")
    sites = os.path.join(frappe_dir, "sites")
    for path, dirs, _ in os.walk(sites):
        if site_name in dirs:
            return os.path.join(path, site_name, "site_config.json")
        

def get_app_config():
    json_config_file = get_site_config_file("tasks.localhost")
    with open(json_config_file) as json_file:
        return json.load(json_file)
    

def backup_db(outfile):
    config = get_site_config() # get_app_config()
    db_name = config["db_name"]
    db_user = config["db_user"]
    db_password = config["db_password"] 

    command = ['pg_dump', '-U', db_user, '-d', db_name, '-f', outfile]

    env = os.environ.copy()
    env['PGPASSWORD'] = db_password

    try:
        subprocess.run(command, env=env, check=True)
        logger.info(f"Backup of {db_name} to {outfile} was successful.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Backup failed with error: {e}")


