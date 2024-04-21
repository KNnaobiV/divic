import configparser
import os

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker


__all__= [
    "get_db_url",
    "get_engine", 
    "load_session", 
    "load_table"
]

def get_db_url():
    cfg =  configparser.ConfigParser()
    cfg.read(os.path.join(os.path.dirname(__file__), "config.cfg"))
    username = cfg.get("DB", "user", fallback=None)
    password = cfg.get("DB", "pwd", fallback=None)
    dbname = cfg.get("DB", "dbname", fallback=None)
    db_url = f"postgresql://{username}:{password}@localhost/{dbname}"
    return db_url
    

def get_engine():
    "Returns an instance of the database engine."
    db_url = get_db_url()
    return create_engine(db_url)


def load_session():
    """Returns an instance of the session."""
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def load_table(table_name):
    """
    Loads a db table
    
    :param table_name: string representation of the table
    :return table: table instance
    """
    metadata = MetaData()
    engine = get_engine()
    table = Table(table_name, metadata, autoload=True, autoload_with=engine)
    return table