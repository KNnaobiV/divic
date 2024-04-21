import operator

from sqlalchemy.ext.declarative import declarative_base

from task_manager.database.db import load_session, load_table
from task_manager.utils.custom_logger import get_logger


__all__= [
    "filter_table", 
    "get_id_from_name",
    "get_item_by_id",
    "get_objects_by_filter", 
]


Base = declarative_base()
logger = get_logger("api")


def filter_table(session, table_name, column_name, **kwargs):
    """
    Filters a table for according to values given in kwargs dict

    :param session: session instance.
    :param table_name: string name of table to be filtered
    :param column_name: string name of table column on which filter 
        will be applied
    :param **kwargs: dictionary of filter arguments and values
    """
    table = load_table(table_name)
    try:
        query = table.select().where(getattr(table.columns, column_name) == kwargs["column_name"])
        return session.execute(query).fetchall()
    except Exception:
        logger.warning("Filter failed.")
    

def get_operator_filter_param(column, operation, value):
    """
    Returns an operation using python's operator module based on the 
    provided parameters.

    :param column: The column on which the operation is to be executed.
    :param operation: The operation/method in python's operator module 
        as a string.
    :param value: The value to be used in the operation.

    :return: An operation using python's operator module based on the 
        provided parameters.
    """
    try:
        operation = getattr(operator, operation)
        return operation(column, value)
    except AttributeError:
        logger.error(f"operator does not have operation {operation}") 


def get_operator_filter_list(filter_dict):
    """
    Generates a list of filter conditions using python's operator module.

    :param column: The column on which the operations are to be executed.
    :param kwargs: Dictionary of filter conditions. Keys are methods in 
        python's operator module as strings.

    :return: A list of filter conditions using python's operator module.
    """
    filter_list = list()
    for column, filter_conditions in filter_dict.items():
        filter_list.append(
            get_operator_filter_param(
                column, 
                filter_conditions[0], 
                filter_conditions[1]
            )
        )
    return filter_list


def get_objects_by_filter(session, model, **kwargs):
    """
    Returns model filtered by items in kwargs.

    :param session: session instance.
    :param model: model to be filtered.
    :param kwargs: dictionary of filter conditions. Keys are column names
        of the specified model which the should be filtered.

    :return objects: filtered query of the model.
    """
    objects = session.query(model).filter_by(**kwargs).all()
    return objects


def get_objects_by_operator_filter(session, model, column, **kwargs):
    """
    Gets model items filtered by the conditions in kwargs.
    .. note::

        It is suited for handling filtering of queries based on 
        operations specified in the python's operator module.

    :param session: session instance.
    :param model: model to be filtered.
    :param column: column on which the operation is to be executed.
    :param kwargs: dictionary of filter conditions. Specified keys
        are methods in python's operator module as `str`

    :return objects: filtered query of the model.
    """
    filter_list = get_operator_filter_list(column, **kwargs)
    objects = session.query(model).filter(*filter_list).all()
    return objects
    

def get_filtered_model_objects(session, model, **kwargs):
    """
    Returns model filtered by items in kwargs.

    :param session: session instance.
    :param model: model to be filtered.
    :param kwargs: dictionary of filter conditions. Keys are column names
        of the specified model which the should be filtered.

    :return objects: filtered query of the model.
    """
    objects = session.query(model).filter_by(**kwargs).all()
    return objects


def get_class_by_tablename(fullname):
    """
    Returns class reference mapped to table.

    :param fullname: string with full name of table.
    :return: Class reference or None
    """
    for c in Base.registry._class_registry.data.values():
        if hasattr(c, "__table__") and c.__table__.fullname == fullname:
            return c
