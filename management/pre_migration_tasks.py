from frappe.frappe.utils import get_db_count
from sqlalchemy import inspect

from task_manager.database.db import get_engine, load_session, load_table
inspector = inspect(get_engine(db_url=))
schemas = inspector.get_schema_names()

for schema in schemas:
    print("schema: %s" % schema)
    for table_name in inspector.get_table_names(schema=schema):
        for column in inspector.get_columns(table_name, schema=schema):
            print("Column: %s" % column)