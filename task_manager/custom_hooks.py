import asyncio
import json
import os

import frappe
from frappe.frappe.utils import get_site_path

from task_manager.utils import get_logger
from task_manager.task_manager.management.commands import (
    management_commands_before_migration
)

from .utils import backup_db
from  .server import run_server
# site_path = get_site_path()

logger = get_logger(name="root", loglevel="INFO")

async def after_start():
    await send_welcome_email()
    await update_last_login()
    await log_startup()


async def before_migrate():
    await management_commands_before_migration()
    await backup_db()
    await run_server() # perform_maintenance_tasks()


async def after_migrate():
    await update_db_version()
    await notify_db_migration()
    await schedule_periodic_tasks()


async def send_welcome_email():
    pass

async def update_last_login():
    logger.info("New login ")

async def log_startup():
    logger.info("Application Rebooted.")



