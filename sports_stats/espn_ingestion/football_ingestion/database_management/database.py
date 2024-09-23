import logging
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.errors import *

import config

conf = config.conf


def create_db(db_name):
    con = psycopg2.connect(dbname='postgres', user=conf.username, host=conf.host, password=conf.password)

    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cur = con.cursor()

    # Use the psycopg2.sql module instead of string concatenation
    # in order to avoid sql injection attacks.
    try:
        cur.execute(sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier(db_name))
        )
    except DuplicateDatabase:
        logging.warning(f'Database {db_name} already exists, not recreating.')

create_db('football')
