import keyboard
from typing import Callable

current_key: str = ""
current_allowed_key: str = ""
current_word_typed: str = ""
current_line_typed: str = ""
stdin: str = ""

last_key: str = ""
last_allowed_key: str = ""
last_word_typed: str = ""
last_line_typed: str = ""

def on_key_event(key: keyboard.KeyboardEvent) -> None:
    if key.name is None:
        return
    global current_key, current_word_typed, current_line_typed, stdin, current_allowed_key
    global last_key, last_allowed_key, last_word_typed, last_line_typed
    allowed: str = 'qwertyuiopasdfghjklzxcvbnm'
    allowed += allowed.upper()
    allowed += '0123456789'
    allowed += '-_=()!@#$%^&*;'
    allowed: set[str] = set(allowed)
    allowed.add('space')
    if key.event_type == "up":
        last_key = current_key
        current_key = ""
        if key.name in allowed:
            last_allowed_key = current_allowed_key
        current_allowed_key = ""
    else:
        current_key = key.name  # type: ignore
        if key.name in allowed:
            last_word_typed = current_word_typed
            if key.name != "space":
                stdin += key.name
                if key.name not in {';', ',', '.'}:
                    current_word_typed += key.name
                else:
                    current_word_typed = ""
            else:
                stdin += ' '
                current_word_typed = ""
            current_allowed_key = key.name
        elif key.name == "enter":
            current_line_typed = ""
            current_word_typed = ""

keyboard.hook(on_key_event)

STARTED_INPUT: Callable | None = None
INPUT = ""
ALLOW_BACK = False

def start_input(backspace_enabled: bool = False):
    global STARTED_INPUT
    global INPUT
    global ALLOW_BACK
    if STARTED_INPUT:
        return
    allowed = 'qwertyuiopasdfghjklzxcvbnm'
    allowed += allowed.upper()
    allowed += '.>,</?+_-=[]}{\\|\'";:0987654321!@#$%^&*()'
    allowed = set(allowed)
    INPUT = ""
    ALLOW_BACK = backspace_enabled

    def helper(event: keyboard.KeyboardEvent):
        global INPUT, ALLOW_BACK
        nonlocal allowed
        if not event.event_type == "down": return
        if event.name not in allowed:
            if (not (event.name == 'backspace' and ALLOW_BACK)) and event.name != 'space':
                return
        if event.name == "backspace" and ALLOW_BACK:
            INPUT = INPUT[:-1]
        elif event.name == 'space':
            INPUT += ' '
        else:
            INPUT += event.name

    keyboard.hook(helper)
    STARTED_INPUT = helper

def end_input() -> str:
    global STARTED_INPUT
    if not STARTED_INPUT: return ''
    keyboard.unhook(STARTED_INPUT)
    return INPUT

def current_input():
    global INPUT
    return INPUT
