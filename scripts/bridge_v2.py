#!/usr/bin/env python3
import sqlite3, subprocess, time, os, sys, logging, fcntl

DB = os.path.expanduser('~/Clipper/shared_memory.db')
LOG = os.path.expanduser('~/Clipper/bridge.log')
PID = os.path.expanduser('~/Clipper/bridge.pid')

logging.basicConfig(filename=LOG, level=logging.INFO, format='%(asctime)s %(message)s')

# PID lock - one instance only
try:
    pidfile = open(PID, 'w')
    fcntl.lockf(pidfile, fcntl.LOCK_EX | fcntl.LOCK_NB)
    pidfile.write(str(os.getpid()))
    pidfile.flush()
except IOError:
    logging.info('Duplicate instance - exiting')
    sys.exit(0)

def get_conn():
    conn = sqlite3.connect(DB, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA journal_mode=WAL')
    conn.execute('PRAGMA busy_timeout=10000')
    conn.execute('PRAGMA synchronous=NORMAL')
    return conn

def ensure_tables():
    try:
        c = get_conn()
        c.execute('''CREATE TABLE IF NOT EXISTS status (
            component TEXT PRIMARY KEY,
            status TEXT, message TEXT, updated_at TEXT
        )''')
        c.commit()
        c.close()
    except Exception as e:
        logging.error(f'ensure_tables: {e}')

def log_status(st, msg=''):
    try:
        c = get_conn()
        c.execute(
            'INSERT OR REPLACE INTO status (component,status,message,updated_at) VALUES (?,?,?,datetime("now"))',
            ('mcp_bridge', st, msg)
        )
        c.commit()
        c.close()
    except Exception as e:
        logging.error(f'log_status: {e}')

ensure_tables()
logging.info('Bridge v2 started')
log_status('up', 'v2 running')
last = ''

while True:
    try:
        c = get_conn()
        row = c.execute("SELECT value FROM memory WHERE key='command'").fetchone()
        c.close()
        val = row['value'].strip() if row and row['value'] else ''
        if val and val != last:
            last = val
            logging.info(f'CMD: {val[:100]}')
            c2 = get_conn()
            c2.execute("UPDATE memory SET value='' WHERE key='command'")
            c2.commit()
            c2.close()
            subprocess.Popen(val, shell=True)
            logging.info('Dispatched OK')
            log_status('up', f'ran at {time.strftime("%H:%M:%S")}')
        time.sleep(2)
    except Exception as e:
        logging.error(f'loop: {e}')
        time.sleep(5)
