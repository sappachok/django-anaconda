import os
import sys
import signal

try:
    pid = int(sys.argv[1])
    os.kill(pid, signal.SIGTERM)
    os.waitpid(pid, 0)
    print(True)
    exit()
except OSError:
    pass
    print(False)
    exit()