import subprocess
import sys
import time

if __name__ == "__main__":  # a guard from unintended usage
    input_buffer = sys.stdin  # a buffer to get the user input from
    output_buffer = sys.stdout  # a buffer to write rasa's output to
    proc = subprocess.Popen(["python3","-i","-q","-u"],  # start the process
                            stdin=subprocess.PIPE,  # pipe its STDIN so we can write to it
                            stdout=output_buffer, # pipe directly to the output_buffer
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    while True:  # run a main loop
        time.sleep(0.5)  # give some time for `rasa` to forward its STDOUT
        print("", file=output_buffer, flush=True)  # print the input prompt
        print(input_buffer.readline(), file=proc.stdin, flush=True)  # forward the user input