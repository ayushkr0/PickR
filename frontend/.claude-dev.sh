#!/bin/sh
# Ensure node is findable by Turbopack's child process spawner
BINDIR="/Users/ayush/Developer/ProductRec/frontend/.bin"
mkdir -p "$BINDIR"
ln -sf /opt/homebrew/bin/node "$BINDIR/node"
export PATH="$BINDIR:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"
cd /Users/ayush/Developer/ProductRec/frontend
exec "$BINDIR/node" node_modules/.bin/next dev --webpack "$@"
