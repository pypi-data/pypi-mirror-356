

import inspect
import sys
from pathlib import Path

class DebugTracer:
    def __init__(self, filter_path=None, enabled:bool=True):
        self.filter_path = Path(filter_path).resolve() if filter_path else None
        self.enabled = enabled

    def trace_calls(self, frame, event, arg):
        code = frame.f_code
        function_name = code.co_name
        filename = Path(code.co_filename).resolve()
        line_num = frame.f_lineno

        # colors
        bold_yellow = '\x1b[33;1m'
        bold_red = '\x1b[31;1m'
        bold_cyan = '\x1b[36;1m'
        bold_magneta = '\x1b[35;1m'
        reset = '\x1b[0m'

        # Only trace files in filter_path (if set)
        if self.filter_path and not str(filename).startswith(str(self.filter_path)):
            return
        
        if event == 'call':
            # Get argument values
            args_info = inspect.getargvalues(frame)
            args_str = ', '.join(f'{k}={args_info.locals[k]!r}' for k in args_info.args)

            print(f'{bold_yellow}[CALL] {function_name}({args_str}) at {filename}:{line_num}{reset}', flush=True)
            if 'builtin' in str(code):
                print(f'{bold_magneta}[NOTE] {function_name} may be a built-in or C-extension (limited debug info){reset}')
        
        elif event == 'return':
            print(f'{bold_cyan}[RETURN] {function_name} -> {arg!r}{reset}', flush=True)
        
        elif event == 'exception':
            exc_type, exc_value = arg
            print(f'{bold_red}[EXCEPTION] {function_name} raised {exc_type.__name__}: {exc_value}{reset}', flush=True)


    def start(self):
        bold_green = '\x1b[32;1m'
        reset = '\x1b[0m'
        if self.enabled:
            sys.settrace(self.trace_calls)
            print(f'{bold_green}[DebugTracer] Started{reset}')
    
    def stop(self):
        bold_green = '\x1b[32;1m'
        reset = '\x1b[0m'
        if self.enabled:
            sys.settrace(None)
            print(f'{bold_green}[DebugTracer] Stopped{reset}')