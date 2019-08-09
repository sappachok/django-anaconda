from subprocess import Popen, PIPE, STDOUT

def Command(cmd):
    command = cmd
    try:
        process = Popen(command, stdout=PIPE, stderr=STDOUT)
        output = process.stdout.read()
        exitstatus = process.poll()
        if (exitstatus == 0):
            return {"status": "Success", "output": str(output)}
        else:
            return {"status": "Failed", "output": str(output)}
    except Exception as e:
        return {"status": "failed", "output": str(e)}

test = []
test.append(Command(["python", "my.py"]))
print(test)