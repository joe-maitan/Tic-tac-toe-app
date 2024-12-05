# Allows convienient start up by installing everything needed to run the frontend and then running it once successful

import subprocess

def run_command_realtime(command):
    # try/catch for a graceful Ctrl C exit instead of error
    try:
        process = subprocess.Popen(command, shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for line in process.stdout:
            print(line, end="")

        process.wait()
        if process.returncode != 0:
            print("Error:", process.stderr.read())
    except KeyboardInterrupt:
        print("Disconnecting from backend")

# Runs the frontend install commands then starts up the program
run_command_realtime("./set_environment.sh")