import subprocess
import sys, os
import threading
import time
import io

# we'll be using a separate thread and a timed event to request the user input
def print_buffer(timer, wait, buffer_in, buffer_out, buffer_target, buffer_err, input):
	for cmd in buffer_in:
		if cmd.strip() != '\n':
			print(cmd, file=buffer_target)
		#buffer_target.write(cmd)
		#buffer_target.flush()
		#input.append(buffer_out)
		#print('quit()', file=buffer_target, flush=True)
	buffer_target.flush()

def run(commands):
    if not commands:
        return False
    input = []
    input_buffer = commands  # a buffer to get the user input from
    output_buffer = sys.stdout  # a buffer to write rasa's output to
    error_buffer = sys.stderr
	
    os.environ['PYTHONUNBUFFERED'] = "1"
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
                                          input_buffer, output_buffer, proc.stdin, proc.stderr, input))
    input_thread.daemon = True  # no need to keep the input thread blocking...
    input_thread.start()  # start the timer thread
    input_thread.join()
    # now we'll read the `rasa` STDOUT line by line, forward it to output_buffer and reset
    # the timer each time a new line is encountered
	
    
    output = []
    for line in proc.stdout:        
        output.append(line)
    
    print(output)
    
    '''
    error = []
    for line in proc.stderr:
        error.append(line)
	
    print(error)
    '''
    proc.stdin.close()
    proc.terminate()
    proc.wait()       

    
if __name__ == "__main__":
	print("start...")
	f = open("iris.py", "r")
	
	commands = f.read().splitlines()
	commands.append("1+1\n")
	#commands.append("1+200\n")
	#commands.append('exit(42)')
	#commands.append('quit()')
	commands.append('exit(42)')
	commands.append("1+300\n")
	commands.append('import util_interactive')
	commands.append('util_interactive.printfigs("fig", None, ".png")')
	#commands.append('quit()')
	run(commands)
    
'''
quit()
'''

