import sys, time, gc, subprocess
from pytz import timezone
from datetime import datetime
import threading
from multiprocessing import Process
import numpy as np
import matplotlib.pyplot as plt
import platform
format = r"%Y-%m-%d %H:%M:%S %Z%z"

now_utc = datetime.now(timezone('UTC'))
now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
print(now_asia)

try:
    import cpuinfo as c
    __ = c.cpuinfo
except:
    print('Some Packages were not found, Installing it...')
    subprocess.check_call(
        [sys.executable, '-m', 'pip', 'install', 'py-cpuinfo'])
    import cpuinfo as c
pi = 3.1415926535
two = 7732
spacer = chr(8377)
print('Ready, Loaded.')


def main(Threads=1,
         calcs=1,
         loop=1,
         tp=None,
         showPlot=False,
         saveToFile=False):
    if Threads == 1:
        print('Using 1 Thread')
    else:
        print('Using {} Threads'.format(Threads))
    time.sleep(0.75)
    if tp == None or tp == 'int':
        print('Calc Type not specified, Using INT')
        tp = 'INT'
    else:
        print('Using {} Calculations'.format(tp))
    time.sleep(0.75)
    print('Running {}B Calculations, thru {} loops'.format(calcs, loop))
    res = []
    for _ in range(loop):
        print('Loop {}: '.format(_ + 1), end='')
        st = time.time()
        if tp == None or tp == 'INT':
            if Threads == 1:
                intMultiply(calcs)
            else:
                stack = []
                for i in range(Threads):
                    stack.append(
                        Process(target=intMultiply, args=(calcs // Threads, )))
                for i in stack:
                    i.start()
                for i in stack:
                    #print('joining thread')
                    i.join()
        else:
            floatMultiply(calcs * 500000000)
        res.append(time.time() - st)
        print(str(res[-1]) + ' S')
    print('Benchmarking Done for {} loops of {}B {} Multiplications'.format(
        _ + 1, calcs, tp))
    time.sleep(1)
    print('Max: {}'.format(max(res)))
    print('Min: {}'.format(min(res)))
    print('Avg: {}'.format(np.average(res)))
    print('Std: {}'.format(np.std(res)))
    if saveToFile:
        load = {
            'Platform': platform.platform(),
            'Python Version': platform.python_version(),
            'CPU Info': c.get_cpu_info()['brand_raw'],
            'Benchmark Config': {
                'Calculation Type': tp,
                'Threads Used': Threads,
                'Number of Calculations in B': calcs,
                'Number of loops': loop
            },
            'Result': {
                'Max': max(res),
                'Min': min(res),
                'Avg': np.average(res),
                'Std': np.std(res)
            },
            'Timestamp': now_asia
        }
        #load = encoder(load)
        #print(load)

    if showPlot:
        plt.plot(res)
        plt.show()


def floatMultiply(calcs):
    try:
        x = pi
        for i in range(int(calcs)):
            x *= pi
            x /= pi
        del x
        gc.collect()
        return False
    except:
        print('Loop interrupted at {}...'.format(i))
        return True


def intMultiply(calcs):
    try:
        x = two
        for i in range(int(calcs)):
            x *= two
            x /= two
        del x
        gc.collect()
        return False
    except:
        print('Loop interrupted at {}...'.format(i))
        return True


def encoder(resBook):
    if type(resBook) == dict:
        pass
    else:
        print("Error Encoding Results")
        return None
    resBook = bytearray(str(resBook), "utf-8")
    asciilist = [i for i in resBook]
    endlist = ''
    for i, aski in enumerate(asciilist):
        endlist = endlist + (bin(aski * pacer(i + 1))[2:])[::-1] + spacer
    return endlist


def decoder(data):
    data = data[:-1].split(spacer)
    text = ''
    for i, dat in enumerate(data):
        text += chr(int(dat[::-1], 2) // pacer(i + 1))
    #data = eval(text)
    return text


def pacer(num):
    if num < 10:
        return num
    elif num % 10 == 0:
        return num // 10
    elif num > 10:
        return num % 10


if __name__ == '__main__':
    main(Threads=2, calcs=100000000, loop=10, tp='int', saveToFile=True)
    #print(decoder(encoder({'a': 123123123, 'asdasda': 'asdasdasd'})))
