import subprocess
import sys
import threading

# we'll be using a separate thread and a timed event to request the user input
def timed_script(timer, wait, buffer_in, buffer_out, buffer_target, buffer_err):
    for cmd in buffer_in:
        print(cmd, file=buffer_target, flush=True)

if __name__ == "__main__":  # a guard from unintended usage
    commands = ['1+1\n','2+2\n','print("hello")\n','a=1\n','b=2\n','a+b\n','import json','d=[1,2,3,4,5]','e=json.dumps(d)\n','e\n','print(g)','print(d)','x=100\n','x++\n','quit()\n']
    input_buffer = commands  # a buffer to get the user input from
    output_buffer = sys.stdout  # a buffer to write rasa's output to
    error_buffer = sys.stderr
    proc = subprocess.Popen(["python3","-i","-q","-u"],  # start the process
                            stdin=subprocess.PIPE,  # pipe its STDIN so we can write to it
                            stdout=subprocess.PIPE,  # pipe its STDIN so we can process it
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    # lets build a timer which will fire off if we don't reset it
    timer = threading.Event()  # a simple Event timer
    input_thread = threading.Thread(target=timed_script,
                                    args=(timer,  # pass the timer
                                          0.2,  # prompt after one second
                                          input_buffer, output_buffer, proc.stdin, proc.stderr))
    input_thread.daemon = True  # no need to keep the input thread blocking...
    input_thread.start()  # start the timer thread
    input_thread.join()
    # now we'll read the `rasa` STDOUT line by line, forward it to output_buffer and reset
    # the timer each time a new line is encountered
    output = []
    for line in proc.stdout:
        output.append(line)
    
    error = []
    for line in proc.stderr:
        error.append(line)
    
    print(output)
    print(error)
    proc.stdin.close()
    proc.terminate()
    proc.wait(timeout=0.2)