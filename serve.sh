#!/bin/bash
# Serve the site locally. Any static server works — the engine loads clips as blobs,
# so it does not depend on the host supporting HTTP byte-range requests.
cd "$(dirname "$0")/site" && exec python3 -m http.server "${1:-8787}"
