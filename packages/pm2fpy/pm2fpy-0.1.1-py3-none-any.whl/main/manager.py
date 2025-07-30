import subprocess
import os
import signal
import shlex
import psutil
from tabulate import tabulate


class ProcessInfo:
    def __init__(self, name, proc, interpreter):
        self.name = name
        self.proc = proc
        self.interpreter = interpreter
        self.restarts = 0
        self.mode = 'fork'

    def is_running(self):
        return self.proc.poll() is None

    def restart(self):
        if self.is_running():
            self.stop()
        self.proc = subprocess.Popen(
            [self.interpreter, self.proc.args[1]],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid
        )
        self.restarts += 1

    def stop(self):
        if self.is_running():
            os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)
            self.proc.wait()

    def cpu_memory(self):
        try:
            p = psutil.Process(self.proc.pid)
            cpu = p.cpu_percent(interval=0.1)
            mem = p.memory_info().rss / (1024 * 1024)
            return cpu, mem
        except Exception:
            return 0.0, 0.0


class SimpleDaemonManager:
    def __init__(self):
        self.processes = {}  # name: ProcessInfo

    def start(self, name, script, interpreter='python3'):
        if name in self.processes and self.processes[name].is_running():
            return False  # already running

        proc = subprocess.Popen(
            [interpreter, script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid
        )
        self.processes[name] = ProcessInfo(name, proc, interpreter)
        return True

    def stop(self, name):
        pi = self.processes.get(name)
        if not pi or not pi.is_running():
            return False
        pi.stop()
        return True

    def list(self):
        result = []
        for i, (name, pi) in enumerate(self.processes.items()):
            status = 'online' if pi.is_running() else 'stopped'
            cpu, mem = pi.cpu_memory()
            result.append({
                'id': i,
                'name': name,
                'mode': pi.mode,
                'restarts': pi.restarts,
                'status': status,
                'cpu': f"{cpu:.1f}%",
                'memory': f"{mem:.1f}mb"
            })
        return result


def parse_start_args(args):
    name = None
    interpreter = 'python3'
    script = None

    i = 0
    while i < len(args):
        arg = args[i]
        if arg == '--name' and i + 1 < len(args):
            name = args[i + 1]
            i += 1
        elif arg == '--interpreter' and i + 1 < len(args):
            interpreter = args[i + 1]
            i += 1
        else:
            if not script:
                script = arg
        i += 1

    if not script:
        return None
    if not name:
        name = os.path.splitext(os.path.basename(script))[0]

    return name, script, interpreter


def print_table(processes):
    if not processes:
        print("No processes running.")
        return

    headers = ['id', 'name', 'mode', '↺', 'status', 'cpu', 'memory']
    rows = []
    for p in processes:
        rows.append([
            p['id'],
            p['name'],
            p['mode'],
            p['restarts'],
            p['status'],
            p['cpu'],
            p['memory']
        ])
    table = tabulate(rows, headers, tablefmt="fancy_grid", stralign='center')
    print(table)
