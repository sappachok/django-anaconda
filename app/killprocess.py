import os
import sys
import signal

try:
    pid = int(sys.argv[1])
    os.kill(pid, signal.SIGTERM)
except Exception as e:
    print(e)