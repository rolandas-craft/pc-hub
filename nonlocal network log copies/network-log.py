#!/usr/bin/env python3

from datetime import datetime

print(f"{datetime.now()}: Script started.")  # <- This goes to .log

with open("/Users/rolandas/scripts/log/log.txt", "a") as f:
    f.write(f"{datetime.now()}: Script was run.\n")