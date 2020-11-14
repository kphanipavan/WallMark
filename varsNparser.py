from datetime import datetime
import sys
import subprocess
from pytz import timezone
import platform
format = r"%Y-%m-%d %H:%M:%S %Z%z"
menuList = ['1. Run a Benchmark', '2. Load a result', '3. Quit']
now_utc = datetime.now(timezone('UTC'))
now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
now_asia = now_asia.strftime(format)

pi = 3.1415926535
two = 7732
spacer = chr(8377)
imageComposer = {
    '1': [255, 0, 0],
    '0': [0, 255, 0],
    chr(8377): [0, 0, 255],
    ' ': [0, 0, 0]
}
imageDecomposer = {
    (255, 0, 0): '1',
    (0, 255, 0): '0',
    (0, 0, 255): chr(8377),
    (0, 0, 0): ' '
}


def mac():
    hwinf = {}
    hwinf['OS'] = 'MacOS ' + platform.mac_ver()[0]
    data0 = subprocess.run(
        ['sysctl', 'machdep'],
        stdout=subprocess.PIPE).stdout.decode('utf-8').split('\n')
    for i in data0:
        if i.split(': ')[0] == 'machdep.cpu.brand_string':
            hwinf['CPU Name'] = i.split(': ')[1]
        elif i.split(': ')[0] == 'machdep.cpu.core_count':
            hwinf['Cores'] = int(i.split(':')[1])
        elif i.split(': ')[0] == 'machdep.cpu.thread_count':
            hwinf['Threads'] = int(i.split(':')[1])
    if hwinf['Cores'] == hwinf['Threads']:
        hwinf['SMT'] = False
    elif hwinf['Cores'] == hwinf['Threads'] / 2:
        hwinf['SMT'] = True
    else:
        return 'Error Gathering Data'
    #print(hwinf)
    return hwinf


def win():
    pass


def linux():
    x = subprocess.run(['lscpu'], stdout=subprocess.PIPE)
    if x.returncode != 0:
        return None
    x = x.stdout.decode('utf-8').split('\n')[:-1]
    x = [i.split(':') for i in x]
    x = [[i[0], i[1].strip()] for i in x]
    req = ['CPU(s)', 'Thread(s) per core', 'Core(s) per socket', 'Model name']
    f = []
    for i in x:
        if i[0] in req:
            f.append(i)
    f = dict(f)
    n = {}
    n['CPU Name'] = f['Model name']
    n['Cores'] = f['Core(s) per socket']
    n['Threads'] = f['CPU(s)']
    if int(f['Core(s) per socket']) * int(f['Thread(s) per core']) == int(
            f['CPU(s)']) and int(f['Core(s) per socket']) * 2 == int(
                f['CPU(s)']) and int(f['Thread(s) per core']) == 2:
        n['SMT'] = True
    return n


def cpuinfo():
    if sys.platform == 'darwin':
        return mac()
    elif sys.platform == 'win32':
        return win()
    elif sys.platform == 'linux':
        return linux()
    else:
        print('Unsupported platform detected.')