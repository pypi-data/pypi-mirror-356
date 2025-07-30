import os
import sys
import time

from cleary import version, author, description

def clear_ansi():
    """Try to clear console using ANSI escape codes."""
    print("\033[2J\033[H", end='', flush=True)


def clear_windows_ctypes():
    """Try to clear Windows console using ctypes (for cmd)."""
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)
        csbi = ctypes.create_string_buffer(22)
        res = kernel32.GetConsoleScreenBufferInfo(handle, csbi)
        if res:
            import struct
            (bufx, bufy, curx, cury, wattr,
             left, top, right, bottom, maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
            cells = (right - left + 1) * (bottom - top + 1)
            written = ctypes.c_int(0)
            kernel32.FillConsoleOutputCharacterA(handle, ctypes.c_char(b' '), cells, 0, ctypes.byref(written))
            kernel32.FillConsoleOutputAttribute(handle, wattr, cells, 0, ctypes.byref(written))
            kernel32.SetConsoleCursorPosition(handle, 0)
            return True
    except Exception:
        pass
    return False


def clear_input_buffer():
    """Clear input buffer (stdin) for Windows and Unix."""
    try:
        if os.name == 'nt':
            import msvcrt
            while msvcrt.kbhit():
                msvcrt.getch()
        else:
            import termios
            import sys
            termios.tcflush(sys.stdin, termios.TCIFLUSH)
    except Exception:
        pass


def detect_terminal():
    """Detect current terminal type."""
    term = os.environ.get('TERM', '')
    shell = os.environ.get('SHELL', '')
    if sys.platform.startswith('win'):
        if 'pwsh' in os.environ.get('PROMPT', '').lower() or 'powershell' in shell.lower():
            return 'PowerShell'
        elif 'cmd' in shell.lower() or not shell:
            return 'CMD'
        elif 'wt' in os.environ.get('WT_SESSION', ''):
            return 'Windows Terminal'
        else:
            return 'Windows (unknown)'
    if 'zsh' in shell:
        return 'zsh'
    if 'bash' in shell:
        return 'bash'
    if term:
        return term
    return 'unknown'


def print_help():
    from colorama import init, Fore, Style
    init(autoreset=True)
    print(Fore.CYAN + Style.BRIGHT + 'cleary Help')
    print(Fore.YELLOW + 'Usage:')
    print('  cleary [--delay N] [--] [command]')
    print('\nOptions:')
    print('  --delay N           Delay clear by N seconds')
    print('  --                  Run command after clearing (e.g. cleary -- pip list)')
    print('  info                Show program info')
    print('\nNote: input buffer is always cleared by default.')


def do_clear():
    clear_input_buffer()
    clear_ansi()
    if sys.platform.startswith('win'):
        if not clear_windows_ctypes():
            os.system('cls')
    else:
        os.system('clear')


def main():
    args = sys.argv[1:]
    from colorama import init, Fore, Style
    init(autoreset=True)

    if args and args[0] in ('--help', 'help', '-h'):
        print_help()
        return

    if args and args[0] in ('info', '--info'):
        print(Fore.CYAN + Style.BRIGHT + 'Cleary Info')
        print(Fore.GREEN + f'  Version: {version}')
        print(Fore.YELLOW + f'  Author: {author}')
        print(Fore.RED + f'  Description: {description}')
        return

    delay = 0
    run_cmd = None
    i = 0
    while i < len(args):
        if args[i] == '--delay' and i+1 < len(args):
            try:
                delay = float(args[i+1])
            except Exception:
                delay = 0
            i += 1
        elif args[i] == '--':
            run_cmd = args[i+1:]
            break
        i += 1

    if delay > 0:
        print(Fore.MAGENTA + f'Waiting {delay} seconds before clearing...')
        time.sleep(delay)

    do_clear()

    if run_cmd:
        os.system(' '.join(run_cmd))

if __name__ == '__main__':
    main() 