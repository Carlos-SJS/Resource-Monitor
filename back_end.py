import psutil
import threading
from time import sleep

max_history = 100

cpu_stats = []
memory_stats = []
disk_stats = []
procs = []

load1, load5, load15 = psutil.getloadavg()

run_thread = True
sort_by = 'cpu'

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

black_list = ["Registry", "System Idle Process", "", "MsMpEng.exe", "System", "audiodg.exe", "services.exe", "csrss.exe", "smss.exe", "wininit.exe", "Isass.exe", "Lsalso.exe", "fontdrvhost.exe", "WmiPrvSE.exe", "dwm.exe", "prevhost.exe", "dasHost.exe", "MemCompression", "spoolsv.exe", "MoUsoCoreWorker.exe"]
def _get_processes():
    global procs
    ps = [p.info for p in psutil.process_iter(['name', 'cpu_percent', 'memory_percent', 'pid'])]
    
    pos = {}
    procs = []
    for p in ps:
        if p['name'] in black_list:
            continue
        p['cpu_percent'] = round((p['cpu_percent']/5), 2)
        p['memory_percent'] = round(p['memory_percent'])
        if p['name'] not in pos:
            pos[p['name']] = len(procs)
            procs.append(p)
        else:
            ix = pos[p['name']]
            procs[ix]['cpu_percent'] += p['cpu_percent']
            procs[ix]['memory_percent'] += p['memory_percent']   
    
    for p in procs:
        p['cpu_percent'] = round(p['cpu_percent'], 2)
        p['memory_percent'] = round(p['memory_percent'], 2)
    

    if sort_by == 'cpu':
        procs.sort(key=lambda x: x['cpu_percent'], reverse=True)
    elif sort_by == 'mem':
        procs.sort(key=lambda x: x['memory_percent'], reverse=True)

def get_processes():
    return procs

def keep_updated():
    ct = 4
    while run_thread:
        _get_cpu()
        _get_memory()
        _get_disk()

        ct += 1
        
        if ct == 5:
            _get_processes()
            ct = 0
        
        sleep(.2)

t = threading.Thread(target=keep_updated)
t.start()