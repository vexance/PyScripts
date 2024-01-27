import termcolor

def print_status(msg: str, **kwargs) -> None:
    print(termcolor.colored('[*]', 'blue', attrs=['bold']), msg)

def print_failure(msg: str, **kwargs) -> None:
    print(termcolor.colored('[-]', 'red', attrs=['bold']), msg)

def print_error(msg: str, **kwargs) -> None:
    print(termcolor.colored('[x]', 'magenta', attrs=['bold']), msg)

def print_warning(msg: str, **kwargs) -> None:
    print(termcolor.colored('[!]', 'yellow', attrs=['bold']), msg)

def print_unknown(msg: str, **kwargs) -> None:
    print(termcolor.colored('[?]', 'yellow', attrs=['bold']), msg)

def print_success(msg: str, **kwargs) -> None:
    print(termcolor.colored('[+]', 'green', attrs=['bold']), msg)
