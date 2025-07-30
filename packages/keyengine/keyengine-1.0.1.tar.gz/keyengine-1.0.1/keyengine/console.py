from threading import RLock, Thread, Event
from . import keydetection as kd
import keyboard
import time
import os
import sys
import colorama
from typing import Any
from .menus import flush_stdin

class Console:
    def __init__(self):
        colorama.init()
        self.outputs = []
        self.stdin = ''
        self.t = Thread(target = self._refreshloop)
        self.t.start()
        self.lock = RLock()
        self.s = Event()

    def print(self, *values: str, sep: str = ' ', end: str = '\n'):
        self.lock.acquire()

        self.outputs.append(('out', sep.join(values) + end))

        self.lock.release()

    def input(self, prompt: str) -> str:
        self.stdin = prompt
        kd.start_input(True)
        while keyboard.read_event().name != 'enter':
            with self.lock:
                self.stdin = prompt + kd.INPUT
            time.sleep(0.05)
        val = kd.end_input()
        self.lock.acquire()
        self.stdin = ''
        self.print(str(prompt) + str(val))
        flush_stdin()
        self.lock.release()
        return val

    def error(self, err: str):
        self.lock.acquire()
        self.outputs.append(('error', err))
        self.lock.release()

    def log(self, content: str, values: dict[str, Any] | None = None):
        self.lock.acquire()
        self.outputs.append(('log', f"[LOG] {content}"))
        if values:
            for k, v in values.items():
                self.outputs.append(('log', f"  |  `{k}` = `{v}`"))
        self.lock.release()

    def _refreshloop(self):
        while True:
            time.sleep(0.05)
            if self.s.is_set(): return
            self._update()

    def _update(self):
        if self.s.is_set(): return
        self.lock.acquire()
        os.system('cls')
        if not hasattr(self, 'outputs'):
            self.s.set()
            self.lock.release()
            return
        if len(self.outputs) > 100:
            self.outputs = self.outputs[69:] # Stop the outputs from being longer than 100.
        for (t, v) in self.outputs:
            if t == 'out':
                sys.stdout.write(f'{v}')
            elif t == 'error':
                sys.stderr.write(f'{colorama.Fore.RED}{v}{colorama.Fore.RESET}\n')
            elif t == 'log':
                sys.stderr.write(f'{v}\n')
            else:
                sys.stdout.write(f'{v}\n')

        sys.stdout.write(f"{colorama.Style.BRIGHT}{self.stdin}{colorama.Style.RESET_ALL}")
        sys.stdout.flush()
        self.lock.release()

    def stop(self):
        if hasattr(self, 'outputs'):
            del self.outputs
        self.s.set()

    def __del__(self):
        self.stop()
