import subprocess
import sys
import threading
import time

# we'll be using a separate thread and a timed event to request the user input

def print_buffer(timer, wait, buffer_in, buffer_out, buffer_target, buffer_err):
	global num_block

	for cmd in buffer_in:
		buffer_target.write("{}\n".format(cmd))

	buffer_target.flush()
	#time.sleep(0.1)

def run(commands):
	global num_block

	if not commands:
		return False
		
	input_buffer = commands  # a buffer to get the user input from
	output_buffer = sys.stdout  # a buffer to write rasa's output to
	error_buffer = sys.stderr
	proc = subprocess.Popen(["python3","-i","-q","-u"],  # start the process
							stdin=subprocess.PIPE,  # pipe its STDIN so we can write to it
							stdout=subprocess.PIPE,  # pipe its STDIN so we can process it
							stderr=subprocess.PIPE,
                            shell=True,
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

	proc.stdin.close()

	output = []
	for line in proc.stdout:
		output.append(line)
	
	error = []
	for line in proc.stderr:
		error.append(line)
	
	proc.terminate()
	proc.wait(timeout=0.2)

	return (output, error)