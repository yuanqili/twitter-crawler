import json
import os
import sys


def print_json(json_file):
    print(json.dumps(json_file, sort_keys=True, indent=4, separators=(',', ':')))


def sqlite_url_gen(path, filename):
    return 'sqlite:///' + os.path.join(os.path.abspath(path), filename)

palette = {
    'black': '\033[30m',
    'red': '\033[91m',
    'green': '\033[32m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'pink': '\033[95m',
    'magenta': '\033[95m',
    'cyan': '\033[96m',
    'white': '\033[97m',
    'gray': '\033[37m',
    'default': '\033[0m',
}

highlighter = {
    'black': '\033[40m',
    'red': '\033[101m',
    'green': '\033[102m',
    'yellow': '\033[103m',
    'blue': '\033[104m',
    'pink': '\033[105m', 'magenta': '\033[105m',
    'cyan': '\033[106m',
    'white': '\033[107m',
    'gray': '\033[47m',
}

formatter = {
    'default': '\033[0m',
    'bold': '\033[1m',
    'faint': '\033[2m',
    'italic': '\033[3m',        # Doesn't work on Ubuntu/Mac terminal.
    'underline': '\033[4m',
    'blinking': '\033[5m',
    'fast_blinking': '\033[6m', # Doesn't work on Ubuntu/Mac terminal.
    'reverse': '\033[7m',       # Note: This reverses the back-/foreground color.
    'hide': '\033[8m',
    'strikethrough': '\033[9m', # Doesn't work on Ubuntu/Mac terminal.
}


def color_print(s, color=None, highlight=None, end='\n', file=sys.stdout,
                **kwargs):
    if color in palette and color != 'default':
        s = palette[color] + s
    # Highlight / Background color.
    if highlight and highlight in highlighter:
        s = highlighter[highlight] + s
    # Custom string format.
    for name, value in kwargs.items():
        if name in formatter and value:
            s = formatter[name] + s
    print(s + palette['default'], end=end, file=file)
