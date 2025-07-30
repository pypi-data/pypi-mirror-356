from . import keydetection as kd
import colorama
import time
import os
import sys
import keyboard
import math

if sys.version_info >= (3, 13):
    from warnings import deprecated
else:
    try:
        from deprecated import deprecated
    except ImportError:
        raise ImportError("ImportError: Please import the `deprecated` library unless you have Python 3.13 or newer. If you have Python 3.13 or newer and are seeing this, please open an issue on Github.")

clear = lambda: os.system('cls || clear')

@deprecated('This function was depreacted in v1.0.0. Please use the new menu() function instead, as this one has many errors/issues.')
def plain_menu(choices: list[str]):
    global clear
    c = 0
    if c == -1: c = 6
    if c == 7: c = 0
    for option in choices:
        if choices[c] == option:
            print(f"{colorama.Style.BRIGHT}{option} <{colorama.Style.RESET_ALL}")
        else:
            print(option)
    while kd.current_key != 'enter':
        time.sleep(0.08)
        if kd.current_key != '':
            clear()
            if kd.current_key == 'up':
                c -= 1
            if kd.current_key == 'down':
                c += 1
            if c == -1: c = 6
            if c == 7: c = 0
            for option in choices:
                if choices[c] == option:
                    print(f"{colorama.Style.BRIGHT}{option} <{colorama.Style.RESET_ALL}")
                else:
                    print(option)

    flush_stdin()

    return c

def flush_stdin():
    """
    Flush any unread input from sys.stdin so that the leftover ENTER
    doesn’t immediately satisfy the next input() call.
    """
    try:
        # Unix‐style flush
        import termios
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
    except (ImportError, OSError):
        # Windows‐style flush
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()

def _menu(choices: list[str], index: bool = True, max_lines: int = math.inf):
    global clear

    if max_lines != math.inf:
        raise NotImplementedError("Please set max_lines to math.inf. Scrolling is not yet supported.")

    def with_index(thing):
        nonlocal index
        if not index: return thing
        return str(choices.index(thing)) + '. ' + thing

    c = 0
    if c == -1: c = len(choices) - 1
    if c == len(choices): c = 0
    for option in choices:
        display = with_index(option)
        if choices[c] == option:
            sys.stdout.write(f"{colorama.Style.BRIGHT}{display}{colorama.Style.RESET_ALL} <\n")
        else:
            sys.stdout.write(display + "\n")
        sys.stdout.flush()

    kd.start_input(True)
    while not keyboard.is_pressed('enter'):
        time.sleep(0.04)
        search = kd.INPUT
        event = keyboard.read_event()
        if event.name != '':
            clear()
            if keyboard.is_pressed('up'):
                c -= 1
                if c == -1: c = len(choices) - 1
                if c == len(choices): c = 0
                i = 0
                while not (choices[c].startswith(search) or
           with_index(choices[c]).startswith(search)):
                    i += 1
                    c += -1
                    if c == -1: c = len(choices) - 1
                    if c == len(choices): c = 0
                    if i >= len(choices):
                        search = search[:-1]
                        i = 0
            if keyboard.is_pressed('down'):
                c += 1
                if c == -1: c = len(choices) - 1
                if c == len(choices): c = 0
                i = 0
                while not (choices[c].startswith(search) or
           with_index(choices[c]).startswith(search)):
                    i += 1
                    c += 1
                    if c == -1: c = len(choices) - 1
                    if c == len(choices): c = 0
                    if i >= len(choices):
                        search = search[:-1]
                        i = 0

            if c == -1: c = len(choices) - 1
            if c == len(choices): c = 0
            iterations = 0
            for i, option in enumerate(choices):
                if not (choices[c] == option or option.startswith(search) or with_index(option).startswith(search)):
                    continue
                if i >= c: iterations += 1
                if iterations > max_lines:
                    continue
                display = with_index(option)
                if choices[c] == option:
                    sys.stdout.write(f"{colorama.Style.BRIGHT}{display}{colorama.Style.RESET_ALL} <\n")
                else:
                    sys.stdout.write(display + "\n")
            sys.stdout.write(f'------\n{kd.INPUT}')
            sys.stdout.flush()
    flush_stdin()

    return c

def _menu2(choices: list[str], index: bool = True, max_lines: int = math.inf):
    global clear, kd, flush_stdin

    def with_index(thing):
        return f"{choices.index(thing)}. {thing}" if index else thing

    c = 0  # current selected index
    scroll = 0  # scroll offset

    kd.start_input(True)

    while True:
        clear()
        total_choices = len(choices)
        filtered_choices = filter(lambda x: (with_index(x).startswith(kd.INPUT)), choices)
        filtered_choices = list(filtered_choices)

        # Ensure scroll is within valid bounds
        if max_lines != math.inf:
            if c < scroll:
                scroll = c
            elif c >= scroll + max_lines:
                scroll = c - max_lines + 1
            visible_choices = filtered_choices[scroll:scroll + max_lines]
        else:
            visible_choices = filtered_choices

        i = 0
        ii = -1
        n = set(visible_choices.copy())
        n.add(choices[c])
        n = list(n)
        n = list(sorted(n, key = (lambda x: choices.index(x))))
        for option in visible_choices:
            ii += 1
            actual_index = scroll + i
            display = with_index(option)
            if not (choices[c] == option or option.startswith(kd.INPUT) or display.startswith(kd.INPUT)):
                    continue
            if ii + scroll == c:
                sys.stdout.write(f"{colorama.Style.BRIGHT}{display}{colorama.Style.RESET_ALL} <\n")
            else:
                sys.stdout.write(display + "\n")
            i += 1

        sys.stdout.write(f'------\n{kd.INPUT}')
        sys.stdout.flush()

        if keyboard.is_pressed('enter'):
            break

        time.sleep(0.04)
        event = keyboard.read_event()
        if event.name != '':
            search = kd.INPUT

            if keyboard.is_pressed('up'):
                c -= 1
                if c < 0:
                    c = total_choices - 1

                # Search support while navigating
                i = 0
                while not (choices[c].startswith(search) or with_index(choices[c]).startswith(search)):
                    c -= 1
                    if c < 0:
                        c = total_choices - 1
                    i += 1
                    if i >= total_choices:
                        search = search[:-1]
                        break

            elif keyboard.is_pressed('down'):
                c += 1
                if c >= total_choices:
                    c = 0

                i = 0
                while not (choices[c].startswith(search) or with_index(choices[c]).startswith(search)):
                    c += 1
                    if c >= total_choices:
                        c = 0
                    i += 1
                    if i >= total_choices:
                        search = search[:-1]
                        break

    flush_stdin()
    return c

def menu(choices: list[str], index: bool = True, max_lines: int = math.inf):
    """
    Afișează un meniu navigabil cu săgeți și filtrare live după prefixul tastat.
    Returnează indexul în lista originală al opțiunii selectate.
    """
    global clear, kd, flush_stdin

    # Pregătim lista de tuple (index_original, valoare)
    indexed = list(enumerate(choices))

    # Începem capturarea input-ului
    kd.start_input(True)
    c = 0       # selecția curentă în lista filtrată
    scroll = 0  # offset-ul pentru scroll
    search = "" # prefixul de căutare

    while True:
        clear()
        search = kd.INPUT

        # Filtrăm după prefixul introdus (pe text sau pe text cu index)
        def matches(item):
            orig_i, val = item
            disp = f"{orig_i}. {val}" if index else val
            return disp.startswith(search) or val.startswith(search)

        filtered = [item for item in indexed if matches(item)]
        total = len(filtered)

        # Dacă nu e niciun rezultat, arătăm toate opțiunile
        if total == 0:
            filtered = indexed.copy()
            total = len(filtered)
            # reajustăm c dacă era în afara noii liste
            c = min(c, total - 1)

        # Menținem c în limite
        c %= total

        # Ajustăm scroll astfel încât selecția să fie vizibilă
        if max_lines != math.inf:
            if c < scroll:
                scroll = c
            elif c >= scroll + max_lines:
                scroll = c - max_lines + 1
            visible = filtered[scroll:scroll + int(max_lines)]
        else:
            visible = filtered

        # Afişăm opțiunile vizibile
        for disp_i, (orig_i, val) in enumerate(visible, start=scroll):
            disp = f"{orig_i}. {val}" if index else val
            if disp_i == c:
                sys.stdout.write(f"{colorama.Style.BRIGHT}{disp}{colorama.Style.RESET_ALL} <\n")
            else:
                sys.stdout.write(disp + "\n")

        # Linia de input
        sys.stdout.write("------\n" + search)
        sys.stdout.flush()

        # Verificăm Enter
        if keyboard.is_pressed('enter'):
            break

        # Citim evenimentele de navigare
        time.sleep(0.04)
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == 'up':
                c = (c - 1) % total
            elif event.name == 'down':
                c = (c + 1) % total

    # Curățăm stdin și returnăm indexul original
    flush_stdin()
    return filtered[c][0]