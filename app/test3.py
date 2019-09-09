import contextlib
import subprocess
import pty
import os

# Unix, Windows and old Macintosh end-of-line
newlines = ['\n', '\r\n', '\r']
def unbuffered(proc, stream='stdout'):
    stream = getattr(proc, stream)
    commands = ['1+1\n','2+2\n']
    for cmd in commands:
        proc.stdin.write(cmd)
        proc.stdin.flush()
        with contextlib.closing(stream):
            while True:
                out = []
                last = stream.read(1)
                # Don't loop forever
                if last == '' and proc.poll() is not None:
                    break
                while last not in newlines:
                    # Don't loop forever
                    if last == '' and proc.poll() is not None:
                        break
                    out.append(last)
                    last = stream.read(1)
                out = ''.join(out)
                yield out
                break

def example():
    master, slave = pty.openpty()

    proc = subprocess.Popen(['python3', '-i'],
        stdin=subprocess.PIPE,
        stdout=slave,
        stderr=subprocess.PIPE,
        # Make all end-of-lines '\n'
        universal_newlines=True,
    )
       
    for line in unbuffered(proc,slave):
        print(line)

example()