import subprocess

def run_command_realtime(command):
    process = subprocess.Popen(command, shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in process.stdout:
        print(line, end="")

    process.wait()
    if process.returncode != 0:
        print("Error:", process.stderr.read())

# Run the commands
run_command_realtime("./set_environment.sh")