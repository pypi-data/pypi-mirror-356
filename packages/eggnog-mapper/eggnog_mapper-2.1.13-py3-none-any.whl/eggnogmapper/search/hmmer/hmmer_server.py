##
## JHCepas

import sys
import os
import time
import subprocess
from multiprocessing import Process
import signal

from ...common import HMMPGMD, TIMEOUT_LOAD_SERVER
from ...utils import colorify

from .hmmer_search_hmmpgmd import get_hits
from .hmmer_search import DB_TYPE_SEQ, DB_TYPE_HMM, QUERY_TYPE_SEQ, QUERY_TYPE_HMM
from .hmm_qtype_test_data import test_hmm

CHILD_PROC = None
MASTER = None
WORKERS = None


##
def check_servers(dbtype, qtype, dbpath, host, port, servers_list):
    # Get list of servers
    servers = []
    functional = 0
    if servers_list is not None:
        with open(servers_list, 'r') as servers_fn:
            for line in servers_fn:
                host, port = map(str.strip, line.split(":"))
                port = int(port)
                servers.append([host, port, -1, -1]) # set -1 to master and worker PIDs, since they are not needed here
                if server_functional(host, port, dbtype, qtype):
                    functional += 1
                else:
                    print(colorify("warning: eggnog-mapper server not found at %s:%s" % (host, port), 'orange'))
                    
    else:
        servers = [[host, port, -1, -1]] # set -1 to master and worker PIDs, since they are not needed here
        if server_functional(host, port, dbtype, qtype):
            functional += 1
        else:
            print(colorify("eggnog-mapper server not found at %s:%s" % (host, port), 'red'))
            exit(1)
            
    if functional == 0:
        print(colorify("No functional server was found", 'red'))
        exit(1)

    return dbpath, host, port, servers


##
def create_servers(dbtype, dbpath, host, port, end_port, num_servers, num_workers, cpus_per_worker, timeout_load_server, silent = False):
    if silent == False:
        print(f"create_servers: {dbtype}:{dbpath}:{host}:{port}-{end_port}")
    servers = []
    sdbpath = dbpath
    shost = host
    sport = port
    MAX_CREATE_SERVER_FAILS = 3 # max number of cummulative fails creating servers before aborting creating new ones
    fails = 0
    
    for num_server in range(num_servers):
        if sport >= end_port:
            printf(colorify(f"start port ({sport}) equal or greater than end port ({end_port})", 'red'))
            break

        if silent == False:
            print(f"Creating server number {num_server+1}/{num_servers}")
        try:
            sdbpath, shost, sport, master_pid, workers_pids = start_server(dbpath, host, sport, end_port, cpus_per_worker, num_workers, dbtype, timeout_load_server, silent = silent)
            servers.append((sdbpath, sport, master_pid, workers_pids))
            fails = 0
        except Exception as e:
            import traceback
            traceback.print_exc()
            fails += 1
            print(colorify(f"Could not create server number {num_server+1}/{num_servers}. Fails: {fails}", 'red'))
            if fails >= MAX_CREATE_SERVER_FAILS:
                break
            
        sport = sport + 2
        
    dbpath = sdbpath
    host = shost
    port = sport

    if silent == False:
        print(f"Created {len(servers)} out of {num_servers}")
    if len(servers) == 0:
        raise Exception("Could not create hmmpgmd servers")

    return dbpath, host, port, servers


##
def start_server(dbpath, host, port, end_port, cpus_per_worker, num_workers, dbtype, timeout_load_server, qtype = QUERY_TYPE_SEQ, silent = False):
    master_db = worker_db = workers = None
    MAX_PORTS_TO_TRY = 3
    ports_tried = 0
    ready = False
    for try_port in range(port, end_port, 2):
        if silent == False:
            print(colorify("Loading server at localhost, port %s-%s" %
                           (try_port, try_port + 1), 'lblue'))

        dbpath, master_db, workers = load_server(dbpath, try_port, try_port + 1,
                                                 cpus_per_worker, num_workers = num_workers, dbtype = dbtype,
                                                 silent = silent)
        port = try_port
        # ready = False
        if silent == False:
            print(f"Waiting for server to become ready at {host}:{port} ...")
        for attempt in range(timeout_load_server):
            time.sleep(attempt+1)
            if not master_db.is_alive() or not any([worker_db.is_alive() for worker_db in workers]):
                master_db.terminate()
                master_db.join()
                for worker_db in workers:
                    worker_db.terminate()
                    worker_db.join()                        
                break
            elif server_functional(host, port, dbtype, qtype):
                if silent == False:
                    print(f"Server ready at {host}:{port}")
                ready = True
                break
            else:
                if silent == False:
                    sys.stdout.write(".")
                    sys.stdout.flush()

        ports_tried += 1
        if ready:
            dbpath = host
            break
        else:
            if ports_tried >= MAX_PORTS_TO_TRY:
                raise Exception("Could not start server after trying {ports_tried} ports.")
            
    if ready == False:
        raise Exception("Could not start server.")        

    return dbpath, host, port, master_db, workers


##
def server_up(host, port):
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((host, port))
    sock.close()
    if result == 0:
        return True
    else:
        return False

def server_functional(host, port, dbtype = DB_TYPE_HMM, qtype = QUERY_TYPE_SEQ):
    if server_up(host, port):
        try:
            if qtype == QUERY_TYPE_SEQ:
                get_hits("test", "TESTSEQ", host, port, dbtype, qtype=qtype)
            elif qtype == QUERY_TYPE_HMM:
                get_hits("test", test_hmm, host, port, dbtype, qtype=qtype)

            else:
                raise Exception(f"Unrecognized qtype: {qtype}")
            
        except Exception as e:
            # import traceback
            # traceback.print_exc()
            # print(e)
            return False
        else:
            return True
    # else:
    #     print(colorify("Server is still down", 'red'))
    return False

def safe_exit(a, b):
    if CHILD_PROC:
        CHILD_PROC.kill()
    sys.exit(0)


# These __start_master_subprocess and __start_worker_subprocess
# were formerly functions embedded within load_server and load_worker,
# but using "spawn" as multiprocessing context, instead of default ("fork" for Unix, "spawn" for windows, ...),
# hinders its use do to pickeability
def __start_master_subprocess(client_port, worker_port, dbtype, dbpath, silent, output):
    if not output:
        OUT = open(os.devnull, 'w')
    else:
        OUT = output
        
    cmd = HMMPGMD + f' --master --cport {client_port} --wport {worker_port} --{dbtype} '
    cmd_split = cmd.split()
    cmd_split.append(f'{dbpath}')
    if silent == False:
        print(colorify(f"Loading master: {' '.join(cmd_split)}", 'orange'))
    CHILD_PROC = subprocess.Popen(cmd_split, shell=False, stderr=OUT, stdout=OUT)
    while 1:
        time.sleep(60)
    return

def __start_worker_subprocess(worker_port, cpus_per_worker, silent, output):
    if not output:
        OUT = open(os.devnull, 'w')
    else:
        OUT = output
        
    cmd = HMMPGMD + f' --worker localhost --wport {worker_port} --cpu {cpus_per_worker}'
    if silent == False:
        print(colorify(f"Loading worker: {cmd}", 'orange'))
    CHILD_PROC = subprocess.Popen(cmd.split(), shell=False, stderr=OUT, stdout=OUT)
    while 1:
        time.sleep(60)
    return


def load_worker(worker_port, cpu, output=None, silent = False):
    global CHILD_PID, WORKERS
    if not output:
        OUT = open(os.devnull, 'w')
    else:
        OUT = output
        
    signal.signal(signal.SIGINT, safe_exit)
    signal.signal(signal.SIGTERM, safe_exit)
    
    worker = Process(target=__start_worker_subprocess, args=(worker_port, cpu, silent, output))
    worker.start()
    WORKERS = [worker]
    
    return worker


def load_server(dbpath, client_port, worker_port, cpus_per_worker, num_workers=1, output=None, dbtype=DB_TYPE_HMM, is_worker = True, silent = False):
    global MASTER, WORKERS
    if not output:
        OUT = open(os.devnull, 'w')
    else:
        OUT = output
        
    signal.signal(signal.SIGINT, safe_exit)
    signal.signal(signal.SIGTERM, safe_exit)

    if silent == False:
        print(f"Creating hmmpgmd server at port {client_port} ...")
    # MASTER = Process(target=start_master)
    MASTER = Process(target=__start_master_subprocess, args=(client_port, worker_port, dbtype, dbpath, silent, output))
    MASTER.start()

    if is_worker == True and num_workers > 0:
        if silent == False:
            print(f"Creating hmmpgmd workers ({num_workers}) at port {worker_port} ...")
        WORKERS = []
        for i in range(num_workers):
            worker = Process(target=__start_worker_subprocess, args=(worker_port, cpus_per_worker, silent, output))
            worker.start()
            WORKERS.append(worker)
            
    return dbpath, MASTER, WORKERS


def shutdown_server_by_pid(MASTER, WORKERS):

    import psutil
    
    # This is killing THIS python script also, and is UNIX dependent
    # os.killpg(os.getpgid(WORKER.pid), signal.SIGTERM)

    for worker in WORKERS:
        try:
            parent = psutil.Process(worker.pid)
            for child in parent.children(recursive=True):  # or parent.children() for recursive=False
                child.kill()
            parent.kill()
        except Exception as e:
            print("warning: could not kill hmmpgmd worker --> " + e.msg)

        except (OSError, AttributeError):
            print("warning: could not kill hmmpgmd worker")
            pass
    
    try:
        parent = psutil.Process(MASTER.pid)
        for child in parent.children(recursive=True):  # or parent.children() for recursive=False
            child.kill()
        parent.kill()
                
    except Exception as e:
        print("warning: could not kill hmmpgmd master --> " + e.msg)
    except (OSError, AttributeError):
        print("warning: could not kill hmmpgmd master")
        pass
    
    return


def shutdown_server():
    global MASTER, WORKERS
    shutdown_server_by_pid(MASTER, WORKERS)
    return 
    
    
def alive(p):
    """ Check For the existence of a unix pid. """
    return p.is_alive()
    
## END
