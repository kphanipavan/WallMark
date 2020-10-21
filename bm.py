import os, sys, time, gc
import _thread as t
import numpy as np
import matplotlib.pyplot as plt
pi = 3.1415926535
two = 2
spacer = chr(8377)


def main(Threads=1, calcs=1, loop=1, tp=None, showPlot=False):
    if Threads == 1:
        print('Using 1 Thread')
    else:
        print('Using {} Threads'.format(Threads))
    time.sleep(0.75)
    if tp == None:
        print('Calc Type not specified, Using INT')
        tp = 'INT'
    else:
        print('Using {} Calculations'.format(type))
    time.sleep(0.75)
    print('Running {}B Calculations, thru {} loops'.format(calcs, loop))
    res = []
    for _ in range(loop):
        print('Loop {}: '.format(_ + 1), end='')
        st = time.time()
        if tp == None or tp == 'INT':
            brk = intMultiply(calcs)
        else:
            brk = floatMultiply(calcs * 500000000)
        res.append(time.time() - st)
        if brk:
            if len(res) == 1:
                print('Didn\'t complete even 1 loop')
                return None
            else:
                res = res[:-1]
                _ -= 1
                break
        print(str(res[-1]) + ' S')
    print('Benchmarking Done for {} loops of {}B {} Multiplications'.format(
        _ + 1, calcs, tp))
    time.sleep(1)
    print('Max: {}'.format(max(res)))
    print('Min: {}'.format(min(res)))
    print('Avg: {}'.format(np.average(res)))
    print('Std: {}'.format(np.std(res)))
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
        print('Loop interrupted...')
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
        print('Loop interrupted...')
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
    for i in asciilist:
        endlist = endlist + (bin(i * 2)[2:]) + spacer
    return endlist


def decoder(data):
    pass


if __name__ == '__main__':
    #main(calcs=0.1, loop=10, tp='float')
    print(encoder({'a': 123123123, 'asdasda': 'asdasdasd'}))
