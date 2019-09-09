import subprocess
import sys
import threading

# we'll be using a separate thread and a timed event to request the user input
def print_buffer(timer, wait, buffer_in, buffer_out, buffer_target, buffer_err):
    for cmd in buffer_in:
        print(cmd, file=buffer_target, flush=True)

def run(commands):
    if not commands:
        return False
        
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
    input_thread = threading.Thread(target=print_buffer,
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
    
    proc.stdin.close()
    proc.terminate()
    proc.wait(timeout=0.2)
    
    return (output, error)
    #print(error)