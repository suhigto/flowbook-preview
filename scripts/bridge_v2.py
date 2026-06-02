#!/usr/bin/env python3
import sqlite3, subprocess, time, os, sys, logging, fcntl, hashlib

DB = os.path.expanduser('~/Clipper/shared_memory.db')
LOG = os.path.expanduser('~/Clipper/bridge.log')
PID = os.path.expanduser('~/Clipper/bridge.pid')
SEEN = os.path.expanduser('~/Clipper/bridge_seen.txt')

logging.basicConfig(filename=LOG, level=logging.INFO, format='%(asctime)s %(message)s')

# PID lock - one instance only
try:
    pidfile = open(PID, 'w')
    fcntl.lockf(pidfile, fcntl.LOCK_EX | fcntl.LOCK_NB)
    pidfile.write(str(os.getpid()))
    pidfile.flush()
except IOError:
    logging.info('Duplicate - exiting')
    sys.exit(0)

def load_seen():
    try:
        return open(SEEN).read().strip()
    except:
        return ''

def save_seen(h):
    try:
        open(SEEN, 'w').write(h)
    except:
        pass

def get_conn():
    conn = sqlite3.connect(DB, timeout=5)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA journal_mode=WAL')
    return conn

logging.info('Bridge v3 started - read-only mode')
last_hash = load_seen()

while True:
    try:
        c = get_conn()
        row = c.execute("SELECT value FROM memory WHERE key='command'").fetchone()
        c.close()
        val = row['value'].strip() if row and row['value'] else ''
        if val:
            h = hashlib.md5(val.encode()).hexdigest()
            if h != last_hash:
                last_hash = h
                save_seen(h)
                logging.info(f'Executing: {val[:100]}')
                subprocess.Popen(val, shell=True)
                logging.info('Dispatched')
        time.sleep(2)
    except Exception as e:
        logging.error(f'loop: {e}')
        time.sleep(5)
