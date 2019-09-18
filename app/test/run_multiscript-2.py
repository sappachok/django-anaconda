from __future__ import print_function
import os
import subprocess
import sys

proc = subprocess.Popen(['python3','-i','-u'],
						stdout = subprocess.PIPE,
						stderr = subprocess.PIPE,
						universal_newlines = True,
						)
						
def run(cmd, proc):
    os.environ['PYTHONUNBUFFERED'] = "1"

    stdout = []
    stderr = []
    mix = []
    while proc.poll() is None:
        line = proc.stdout.readline()
        if line != "":
            stdout.append(line)
            mix.append(line)
            print(line, end='')
 
        line = proc.stderr.readline()
        if line != "":
            stderr.append(line)
            mix.append(line)
            print(line, end='')
 
    return proc.returncode, stdout, stderr, mix
 
f = open("iris.py", "r")	
commands = f.read().splitlines()
for c in commands:
	code, out, err, mix = run(c, proc)
#print("out: '{}'".format(out))
#print("err: '{}'".format(err))
#print("err: '{}'".format(mix))
#print("exit: {}".format(code))