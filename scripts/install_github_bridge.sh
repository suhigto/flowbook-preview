#!/bin/bash
echo "=== Installing GitHub Bridge ==="

launchctl unload ~/Library/LaunchAgents/com.hypersuite.bridge.plist 2>/dev/null || true
pkill -9 -f hermes_bridge.py 2>/dev/null || true
pkill -9 -f github_bridge.py 2>/dev/null || true
sleep 2

mkdir -p ~/Clipper
rm -f ~/Clipper/shared_memory.db-shm ~/Clipper/shared_memory.db-wal ~/Clipper/bridge.pid 2>/dev/null || true
> ~/Clipper/bridge.log

echo "Downloading GitHub bridge..."
curl -s "https://raw.githubusercontent.com/suhigto/flowbook-preview/main/scripts/github_bridge.py" -o ~/Clipper/github_bridge.py
echo "Downloaded OK"

echo "Writing LaunchAgent..."
python3 << 'PYEOF'
import os, subprocess
home = os.path.expanduser('~')
python_path = subprocess.check_output(['which', 'python3']).decode().strip()
bridge_path = os.path.join(home, 'Clipper', 'github_bridge.py')
plist_path = os.path.join(home, 'Library', 'LaunchAgents', 'com.hypersuite.bridge.plist')
out_log = os.path.join(home, 'Clipper', 'bridge_out.log')
err_log = os.path.join(home, 'Clipper', 'bridge_err.log')
plist = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n'
    '<plist version="1.0">\n<dict>\n'
    '  <key>Label</key>\n  <string>com.hypersuite.bridge</string>\n'
    '  <key>ProgramArguments</key>\n  <array>\n'
    '    <string>' + python_path + '</string>\n'
    '    <string>' + bridge_path + '</string>\n'
    '  </array>\n'
    '  <key>RunAtLoad</key>\n  <true/>\n'
    '  <key>KeepAlive</key>\n  <dict>\n'
    '    <key>SuccessfulExit</key>\n    <false/>\n'
    '  </dict>\n'
    '  <key>StandardOutPath</key>\n  <string>' + out_log + '</string>\n'
    '  <key>StandardErrorPath</key>\n  <string>' + err_log + '</string>\n'
    '</dict>\n</plist>\n'
)
open(plist_path, 'w').write(plist)
print('LaunchAgent written to ' + plist_path)
PYEOF

echo "Loading bridge..."
launchctl load ~/Library/LaunchAgents/com.hypersuite.bridge.plist
sleep 6

echo "=== Bridge Log ==="
tail -3 ~/Clipper/bridge.log
echo "=== INSTALL COMPLETE - GitHub Bridge is live ==="
