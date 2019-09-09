from subprocess import Popen, PIPE, STDOUT
import fcntl, os
import pty
import time

master, slave = pty.openpty()
proc = Popen(['python3', '-i'],
                        stdin=PIPE,
                        stdout=PIPE,
                        stderr=PIPE,
                        bufsize=1,
                        #universal_newlines=True
                        )

# proc.wait()
# tokenizer = subprocess.Popen(script, shell=True stdin=subprocess.PIPE, stdout=slave)
#fcntl.fcntl(proc.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)
'''
fd = proc.stdout.fileno()
fl = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
'''
 
stdin_handle = proc.stdin
stdout_handle = os.fdopen(master)

def run_script(cmd, stdin, stdout):
    stdin.write(cmd)
    stdin.flush()
    print(stdout.readline())
    # p.wait()
    # print(a)
    # if not stdout.readline():
    #    print(stdout.readline())   

def run_script2(cmd, stdin, stdout):
    stdin.write(cmd)
    stdin.flush()
    print(stdout.readline())        

commands = ['2+2\n', 'len("foobar")\n', 'print("Hello")\n', 'a=1\n', 'a']

for cmd in commands:
    run_script(cmd.encode(), stdin_handle, proc.stdout)
    # run_script2(cmd.encode(), proc.stdin, proc.stdout)
    time.sleep(0.1)

# stdin_handle.write(b'import json\n')
# stdin_handle.flush()
# print(proc.stdout.readline())


'''
print(proc.stdout.readline())
'''
proc.stdin.close()
proc.terminate()
proc.wait(timeout=0.2)