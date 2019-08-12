import subprocess

class ProcessManager(object):
    __PROCESS = None

    def __init__(self):
        pass

    def set_process(self, args):
        if self.__PROCESS is None:
            p = subprocess.Popen(args)
            self.__PROCESS = p

    def kill_process(self):
        if self.__PROCESS is None:
            # exeception handling
            print("none")
        else:
            self.__PROCESS.kill()