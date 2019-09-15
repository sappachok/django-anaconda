import fcntl
import os
import time
import select
import tempfile
import unittest
from ptyprocess.ptyprocess import which
from ptyprocess import PtyProcess, PtyProcessUnicode
                
p = PtyProcessUnicode.spawn(['python3','-i'])
p.read(20)
p.write('6+6\n')
p.read(20)