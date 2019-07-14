import fishPI
import fishPI.models
import fishPI.models.database
import sqlite3
import os

from sqlite3 import Error
from fishPI import logging
from fishPI import services
from fishPI import config


def load():
    create_schema()
        
def close_conn(conn):
    try:
        conn.close()
    except Error as e:
        print(e)
            
def create_conn():
    conn = sqlite3.connect(fishPI.config.database)
    return conn

def database_exists():
    return os.path.exists(fishPI.config.database)

def create_table(create_table_sql):
    conn = create_conn()
    c = conn.cursor()
    c.execute(create_table_sql)
    conn.commit()
    close_conn(conn)

def create_schema():
    if(database_exists()):
        return True

    logging.logInfo(" * Creating Database")

    sql_create_meta_table = """ CREATE TABLE IF NOT EXISTS meta (
                                    id INTEGER PRIMARY KEY,
                                    key TEXT NOT NULL,
                                    value TEXT,
                                    added DATETIME DEFAULT CURRENT_TIMESTAMP
                                ); """
    conn = create_conn()
    create_table(sql_create_meta_table)
    close_conn(conn)

def key_count(key):
    conn = create_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM meta WHERE key=?", (key,))
    result=cur.fetchone()
    close_conn(conn)
    return result[0]

def set_initial(key,value):
    set_meta(key, value, True, True)

def set_meta(key, value, unique = True, if_not_exists = False):

    key = str(key)
    value = str(value)



    if(key_count(key) > 0 and if_not_exists):
        return True

    if(unique and key_count(key) > 0):
        meta = (value, key)
        sql = ''' UPDATE meta set value = ? where key = ? '''
        conn = create_conn()
        cur = conn.cursor()
        cur.execute(sql, meta)
        conn.commit()
        close_conn(conn)
        return get_meta(key,unique)

    else:
        meta = (key, value)
        sql = ''' INSERT INTO meta(key,value)
                VALUES(?,?) '''
        conn = create_conn()
        cur = conn.cursor()
        cur.execute(sql, meta)
        conn.commit()
        close_conn(conn)
        return get_meta(key,unique)

def get_meta(key, unique = True):
        conn = create_conn()
        cur = conn.cursor()
        cur.execute("SELECT id, key, value, added FROM meta WHERE key=?", (key,))

        if(unique):
            result=cur.fetchone()
            close_conn(conn)
            return fishPI.models.database.meta(result[1],result[2],result[3])
        else:
            result=cur.fetchone()
            result=cur.fetchall()
            close_conn(conn)
            return result
         
         