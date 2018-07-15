from time import time, localtime, strftime


def log(*args, **kwargs):
    time_format = '%Y|%m|%d|%a|%H:%M:%S'
    time_now = localtime(int(time()))
    dt = strftime(time_format, time_now)
    print(dt)
    print(*args, **kwargs)
    print('*' * 15)

    with open('log.txt', 'a+') as f:
        print(dt, file=f)
        print(*args, **kwargs, file=f)
        print('*' * 15, file=f)
