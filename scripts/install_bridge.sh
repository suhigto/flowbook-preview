#!/bin/bash
set -e
echo "=== Stopping old bridge ==="
launchctl unload ~/Library/LaunchAgents/com.hypersuite.bridge.plist 2>/dev/null || true
pkill -9 -f hermes_bridge 2>/dev/null || true
sleep 2

echo "=== Clearing locks ==="
rm -f ~/Clipper/shared_memory.db-shm ~/Clipper/shared_memory.db-wal ~/Clipper/bridge.pid
> ~/Clipper/bridge.log

echo "=== Enabling WAL mode on DB ==="
python3 -c "
import sqlite3, os
db = os.path.expanduser('~/Clipper/shared_memory.db')
c = sqlite3.connect(db)
c.execute('PRAGMA journal_mode=WAL')
c.execute(\"UPDATE memory SET value='' WHERE key='command'\")
c.commit()
c.close()
print('WAL enabled + command cleared')
"

echo "=== Downloading bridge v2 ==="
curl -s https://raw.githubusercontent.com/suhigto/flowbook-preview/main/scripts/bridge_v2.py -o ~/Clipper/hermes_bridge.py
echo "Downloaded OK"

echo "=== Writing LaunchAgent ==="
PYTHON=$(which python3)
cat > ~/Library/LaunchAgents/com.hypersuite.bridge.plist << PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.hypersuite.bridge</string>
  <key>ProgramArguments</key>
  <array>
    <string>$PYTHON</string>
    <string>$HOME/Clipper/hermes_bridge.py</string>
  </array>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <dict>
    <key>SuccessfulExit</key>
    <false/>
  </dict>
  <key>StandardOutPath</key>
  <string>$HOME/Clipper/bridge_out.log</string>
  <key>StandardErrorPath</key>
  <string>$HOME/Clipper/bridge_err.log</string>
</dict>
</plist>
PLIST

echo "=== Loading bridge ==="
launchctl load ~/Library/LaunchAgents/com.hypersuite.bridge.plist
sleep 5

echo "=== Bridge log ==="
tail -5 ~/Clipper/bridge.log
echo "=== INSTALL COMPLETE ==="
