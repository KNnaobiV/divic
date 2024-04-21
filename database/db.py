import configparser
import os

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker


__all__= [
    "get_engine", 
    "load_session", 
    "load_table"
]
    

def get_engine(db_url):
    "Returns an instance of the database engine."
    return create_engine(db_url)


def load_session(db_url):
    """Returns an instance of the session."""
    engine = get_engine(db_url)
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