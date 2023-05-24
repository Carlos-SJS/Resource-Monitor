import psutil
import threading
from time import sleep

max_history = 100

cpu_stats = []
memory_stats = []
disk_stats = []

load1, load5, load15 = psutil.getloadavg()

def _get_cpu():
    cpu_stats.append(psutil.cpu_percent())
    #cpu_usage = (load1/psutil.cpu_count()) * 100
    #cpu_stats.append(cpu_usage)

    if(len(cpu_stats) > max_history):
        cpu_stats.pop(0)

def get_cpu():
    return cpu_stats

def _get_memory():
    total = psutil.virtual_memory().total
    used = psutil.virtual_memory().used

    ussage = used/total*100
    memory_stats.append(ussage)

    if(len(memory_stats) > max_history):
        memory_stats.pop(0)

def get_memory():
    return memory_stats


p_name = psutil.disk_partitions()[0].device
stats = psutil.disk_usage(p_name)

def _get_disk():
    global stats
    global p_name
    p_name = psutil.disk_partitions()[0].device
    stats = psutil.disk_usage(p_name)

def get_disk():
    return [stats.free, stats.used], stats.percent

def get_processes(sort_by):
    procs = [p.info for p in psutil.process_iter(['name', 'cpu_percent', 'memory_percent', 'pid'])]

    if sort_by == 'cpu':
        procs.sort(key=lambda x: x['cpu_percent'], reverse=True)
    elif sort_by == 'mem':
        procs.sort(key=lambda x: x['memory_percent'], reverse=True)

    return procs

def keep_updated():
    while True:
        _get_cpu()
        _get_memory()
        _get_disk()
        sleep(.2)

t = threading.Thread(target=keep_updated)
t.start()