import sys, time, gc, subprocess
from pytz import timezone
from datetime import datetime
from multiprocessing import Process
import numpy as np
import matplotlib.pyplot as plt
import cv2
import platform, math
format = r"%Y-%m-%d %H:%M:%S %Z%z"
menuList = ['1. Run a Benchmark', '2. Load a result', '3. Quit']
now_utc = datetime.now(timezone('UTC'))
now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
now_asia = now_asia.strftime(format)
print(now_asia)
lastResult = None
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
print('Ready, Loaded.')


def main(Threads=1, calcs=1, loop=1, tp=None, showPlot=False, saveToFile=True):
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
        try:
            st = time.time()
            if tp == None or tp == 'INT':
                if Threads == 1:
                    multiply('INT', calcs)
                else:
                    stack = []
                    for i in range(Threads):
                        stack.append(
                            Process(target=multiply,
                                    args=(
                                        'INT',
                                        calcs // Threads,
                                    )))
                    for i in stack:
                        i.start()
                    for i in stack:
                        i.join()
            else:
                if Threads == 1:
                    multiply('FLOAT', calcs)
                else:
                    stack = []
                    for i in range(Threads):
                        stack.append(
                            Process(target=multiply,
                                    args=(
                                        'FLOAT',
                                        calcs // Threads,
                                    )))
                    for i in stack:
                        i.start()
                    for i in stack:
                        i.join()
            res.append(time.time() - st)
            print(str(res[-1]) + ' S')
        except:
            print('Loop interrupted..')
            return None
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
        imageCreater(encoder(load))

    if showPlot:
        plt.plot(res)
        plt.show()


def multiply(tp, calcs):
    if tp == 'INT':
        mul = two
    else:
        mul = pi
    x = mul
    for _ in range(int(calcs)):
        x *= mul
        x /= mul
    del x
    gc.collect()
    return None


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


def resultPrinter(dataDict):
    keys = list(dataDict.keys())
    print(keys)
    if list(keys) != [
            'Platform', 'Python Version', 'CPU Info', 'Benchmark Config',
            'Result', 'Timestamp'
    ]:
        print(
            'Error with data, Data is not as Expected, Try rerunning Benchmarks.'
        )
    else:
        print('\n' * 4)
        print('Platform: ', dataDict['Platform'])
        print('Python Version: ', dataDict['Python Version'])
        print('CPU Info: ', dataDict['CPU Info'])
        print('Benchmark Config: ')
        print('\tCalculation Type: ',
              dataDict['Benchmark Config']['Calculation Type'])
        print('\tThreads Used: ', dataDict['Benchmark Config']['Threads Used'])
        print('\tNumber os Calculations in B: ',
              dataDict['Benchmark Config']['Number of Calculations in B'])
        print('\tNumber of loops:',
              dataDict['Benchmark Config']['Number of loops'])
        print('Result: ')
        print('\tMaximum: ', dataDict['Result']['Max'])
        print('\tMinimum: ', dataDict['Result']['Min'])
        print('\tAverage: ', dataDict['Result']['Avg'])
        print('\tStandard deviation: ', dataDict['Result']['Std'])
        print('Timestamp: ', dataDict['Timestamp'])
        print('\n')


def decoder(data):
    data = data[:-1].split(spacer)
    text = ''
    for i, dat in enumerate(data):
        text += chr(int(dat[::-1], 2) // pacer(i + 1))
    #data = eval(text)
    return text


def imageCreater(data):
    l = len(data)
    side = math.ceil(math.sqrt(l))
    data = data + ' ' * (side**2 - l)
    mat = []
    k = 0
    for _ in range(side):
        row = []
        for __ in range(side):
            row.append(imageComposer[data[k]])
            k += 1
        mat.append(row)
    print(np.array(mat).shape)
    tim = time.localtime()
    cv2.imwrite(
        'Result_{}_{}_{}_{}.png'.format(tim.tm_yday, tim.tm_hour, tim.tm_min,
                                        tim.tm_sec), np.array(mat))


def imageDecoder(img):
    data = cv2.imread(img)
    text = ''
    for i in data:
        for j in i:
            text += imageDecomposer[tuple(j)]
    text = text.replace(' ', '')
    result = decoder(text)
    resultPrinter(eval(result))


def pacer(num):
    if num < 10:
        return num
    elif num % 10 == 0:
        return num // 10
    elif num > 10:
        return num % 10


def cli():
    while True:
        print('Enter your selection:')
        for _ in menuList:
            print(_)
        while True:
            try:
                sel = int(input('Selection: '))
                if sel in [1, 2, 3]:
                    break
                else:
                    print('Enter the corresponding number.')
            except:
                print("Enter the corresponding number, not text.")
                continue
        if sel == 1:
            main()
        elif sel == 2:
            loc = input('Enter the absolute location of the Result file: ')
            imageDecoder(loc)
        elif sel == 3:
            exit()


if __name__ == '__main__':
    print('Welcome to WallMark™️')
    cli()
    #main(Threads=2, calcs=10000000, loop=1, tp='int', saveToFile=True)
    #imageDecoder('result.png')
    #main(Threads=2, calcs=100000000, loop=10, tp='int', saveToFile=True)
    #main(Threads=3, calcs=100000000, loop=10, tp='int', saveToFile=True)
    #main(Threads=4, calcs=100000000, loop=10, tp='int', saveToFile=True)
    #print(decoder(encoder({'a': 123123123, 'asdasda': 'asdasdasd'})))
