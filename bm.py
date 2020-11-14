import sys, time, gc, subprocess
from multiprocessing import Process
import numpy as np
import matplotlib.pyplot as plt
import cv2
import platform, math
from varsNparser import *

print('Ready, Loaded.')
cpuInfo = cpuinfo()


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
    print('Running {}M Calculations, thru {} loops'.format(calcs, loop))
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
    print('Benchmarking Done for {} loops of {}M {} Multiplications'.format(
        _ + 1, calcs, tp))
    time.sleep(1)
    print('Max: {}'.format(max(res)))
    print('Min: {}'.format(min(res)))
    print('Avg: {}'.format(np.average(res)))
    print('Std: {}'.format(np.std(res)))
    if saveToFile:
        load = {
            'Platform': platform.platform(),
            'OS': cpuInfo['OS'],
            'Python Version': platform.python_version(),
            'CPU Info': cpuInfo['CPU Name'],
            'Core Count': cpuInfo['Cores'],
            'Thread Count': cpuInfo['Threads'],
            'SMT': cpuInfo['SMT'],
            'Benchmark Config': {
                'Calculation Type': tp,
                'Threads Used': Threads,
                'Number of Calculations in M': calcs,
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
        plt.plot([np.average(res)] * loop)
        plt.plot([np.average(res) + np.std(res)] * loop)
        plt.plot([np.average(res) - np.std(res)] * loop)
        plt.xlabel('Loop')
        plt.ylabel('Time (lower is Better)')
        plt.legend(
            ['Result', 'Average', 'Stddev Upper Limit', 'Stddev Lower Limit'])
        plt.plot(res, 'x')
        print('Close the Graph Window to continue.')
        plt.show()


def multiply(tp, calcs):
    if tp == 'INT':
        mul = two
    else:
        mul = pi
    x = mul
    for _ in range(int(calcs) * 1000000):
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
    if list(keys) != [
            'Platform', 'OS', 'Python Version', 'CPU Info', 'Core Count',
            'Thread Count', 'SMT', 'Benchmark Config', 'Result', 'Timestamp'
    ]:
        print(
            'Error with data, Data is not as Expected, Try rerunning Benchmarks.'
        )
    else:
        print('\n' * 4)
        print('Platform: ', dataDict['Platform'])
        print('OS: ', dataDict['OS'])
        print('Python Version: ', dataDict['Python Version'])
        print('CPU Info: ', dataDict['CPU Info'])
        print('CPU Core Count: ', dataDict['Core Count'])
        print('CPU Thread Count: ', dataDict['Thread Count'])
        print('Hyperthreading: ', (True if dataDict['SMT'] else False))
        print('Benchmark Config: ')
        print('\tCalculation Type: ',
              dataDict['Benchmark Config']['Calculation Type'])
        print('\tThreads Used: ', dataDict['Benchmark Config']['Threads Used'])
        print('\tNumber os Calculations in M: ',
              dataDict['Benchmark Config']['Number of Calculations in M'])
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
    print('Saving to Result_{}_{}_{}_{}.png'.format(tim.tm_yday, tim.tm_hour,
                                                    tim.tm_min, tim.tm_sec))
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


def bmMenu():
    try:
        print('Enter your selection:')
        print('1. Guided Parameter entry')
        print('2. Advanced Parameter entry')
        while True:
            try:
                sel = int(input('Selection: '))
                if sel == 0:
                    return None
                if sel in [1, 2]:
                    break
                else:
                    print('Enter the corresponding number.')
            except:
                print("Enter the corresponding number, not text.")
                continue
        if sel == 1:
            payload = []
            while True:
                try:
                    tr = int(
                        input('Enter the number of Threads to use({} max): '.
                              format(cpuInfo['Threads'])))
                    if tr == 0:
                        return None
                    if tr > cpuInfo['Threads']:
                        print(
                            'Your CPU has a maximum of {} Threads, Enter a number less than that...'
                            .format(cpuInfo['Threads']))
                    else:
                        break
                except:
                    print('Enter a number less than or equal to {}, not text'.
                          format(cpuInfo['Threads']))
            payload.append(tr)
            del tr
            while True:
                try:
                    cl = int(
                        input(
                            'Enter the number of Calculations in Millions: '))
                    if cl == 0:
                        return None
                    break
                except:
                    print('Enter a number, not text.')
            payload.append(cl)
            del cl
            while True:
                try:
                    lp = int(input("Enter the number of loops: "))
                    if lp == 0:
                        return None
                    break
                except:
                    print('Enter a number, not text.')
            payload.append(lp)
            while True:
                try:
                    print('Enter the type of Calculation to be done.')
                    print('1. Integer')
                    print('2. Floating point number')
                    tp = int(input('Enter your selection: '))
                    if tp == 0:
                        return None
                    if tp == 1:
                        payload.append('int')
                        break
                    elif tp == 2:
                        payload.append('float')
                        break
                    else:
                        print('Enter 1 or 2.')
                except:
                    print('Enter a number, not text.')
            while True:
                try:
                    print('You want to see the plot of benchmark times?')
                    print('1. Yes\n2. No')
                    tp = int(input('Enter your selection: '))
                    if tp == 0:
                        return None
                    if tp == 1:
                        payload.append(True)
                        break
                    elif tp == 2:
                        payload.append(False)
                        break
                    else:
                        print('Enter 1 or 2.')
                except:
                    print('Enter a number, not text.')
            while True:
                try:
                    print(
                        'You want save the result to a WallMark encoded file?')
                    print('1. Yes\n2. No')
                    tp = int(input('Enter your selection: '))
                    if tp == 0:
                        return None
                    if tp == 1:
                        payload.append(True)
                        break
                    elif tp == 2:
                        payload.append(False)
                        break
                    else:
                        print('Enter 1 or 2.')
                except:
                    print('Enter a number, not text.')
            main(payload[0], payload[1], payload[2], payload[3], payload[4],
                 payload[5])
        elif sel == 2:
            while True:
                print('Enter Parameters:')
                print(
                    'Threads ({} max), Calcs, Loops, Calc Type(int or float), Show Plot(True or False), Save Result to file(True or False)'
                    .format(cpuInfo['Threads']))
                x = input(': ')
                x = x.split(',')
                x = [i.strip() for i in x]
                print(x)
                if '0' in x:
                    print('Leaving to Main Menu.')
                    break
                try:
                    x[0] = int(x[0])
                    if x[0] > cpuInfo['Threads']:
                        print('Too many Threads mentioned.')
                        continue
                    if x[0] <= 0:
                        print('Enter a valid number of threads.')
                        continue
                except:
                    print('Enter Threads in integer number.')
                    continue
                try:
                    x[1] = int(x[1])
                    if x[1] <= 0:
                        print(
                            'Enter a valid number of Calculations in Millions')
                        continue
                except:
                    print('Enter a Number, greater than 0.')
                    continue
                try:
                    x[2] = int(x[2])
                    if x[2] <= 0:
                        print('Enter a valid number of loops.')
                        continue
                except:
                    print("Enter a valid number of loops.")
                    continue
                if x[3].lower() == 'int':
                    x[3] = 'INT'
                elif x[3].lower() == 'float':
                    x[3] = 'FLOAT'
                else:
                    print('Enter a valid calc mode.')
                    continue
                try:
                    if x[4].lower() == 'true' or x[4].lower() == 't':
                        x[4] = True
                    elif x[4].lower() == 'false' or x[4].lower() == 'f':
                        x[4] = False
                    else:
                        print('Enter a proper true or false for Show Plot')
                        continue
                except:
                    print(
                        'Enter a proper string, True or False, for Show Plot')
                    continue
                try:
                    if x[5].lower() == 'true' or x[5].lower() == 't':
                        x[5] = True
                        break
                    elif x[5].lower() == 'false' or x[5].lower() == 'f':
                        x[5] = False
                        break
                    else:
                        print('Enter a proper true or false for Save to File')
                        continue
                except:
                    print(
                        'Enter a proper string, True or False, for Save to File'
                    )
                    continue
            print(x)
            main(x[0], x[1], x[2], x[3], x[4], x[5])
        else:
            print('Program Corrupt!!!')
            exit()
    except:
        print('Process Stopped.')
        return None


def cli():
    while True:
        print('\nEnter your selection:')
        for _ in menuList:
            print(_)
        while True:
            try:
                sel = int(input('Selection: '))
                if sel in [1, 2, 3, 0]:
                    break
                else:
                    print('Enter the corresponding number.')
            except:
                print("Enter the corresponding number, not text.")
                continue
        if sel == 1:
            bmMenu()
        elif sel == 2:
            loc = input('Enter the absolute location of the Result file: ')
            imageDecoder(loc)
        elif sel == 3:
            exit()
        elif sel == 0:
            print('You are already on the Main Menu :|')


if __name__ == '__main__':
    print('Welcome to WallMark™️ V0.0.1 PreRelease 1\n')
    print('*** Enter 0 as input to return to the Main Menu ***')
    cli()
