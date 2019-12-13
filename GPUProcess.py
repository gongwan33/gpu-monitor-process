from subprocess import Popen, PIPE
from distutils import spawn
import os
import time
import sys
import platform
import time

target_name = 'python'

def getGPUProcess():
    if platform.system() == "Windows":
        nvidia_smi = spawn.find_executable('nvidia-smi')
        if nvidia_smi is None:
            nvidia_smi = "%s\\Program Files\\NVIDIA Corporation\\NVSMI\\nvidia-smi.exe" % os.environ['systemdrive']
    else:
        nvidia_smi = "nvidia-smi"

    try:
        p = Popen([nvidia_smi], stdout=PIPE)
        stdout, stderror = p.communicate()
    except:
        return []
    output = stdout.decode('UTF-8')

    # Interpret the output of the nvidia command
    GPUs = {}
    lines = output.split(os.linesep)
    process_start_line = -1
    for idx, line in enumerate(lines):
        if line is not None and len(line) > 0:
            if line.find('GPU') != -1 and line.find('Process name') != -1 and line.find('PID') != -1:
                process_start_line = idx + 2
                break

    if process_start_line != -1:
        for line in lines[process_start_line : -2]:
            parts = line.split()
            mem_use = parts[5].replace('MiB', '')
            GPUs[parts[4]] = int(mem_use)

    return GPUs

max_gpu_mem = 0
sep_flag = True

while True:
    gpus = getGPUProcess()
    found_flag = False
    for gpup in gpus:
        if gpup == target_name:
            found_flag = True
            if gpus[gpup] > max_gpu_mem:
                print(gpus[gpup])
                max_gpu_mem = gpus[gpup]

    if found_flag == True:
        sep_flag = False
    else:
        max_gpu_mem = 0
        if sep_flag == False:
            print("------------------------------------------")
            sep_flag = True

    time.sleep(0.5)
