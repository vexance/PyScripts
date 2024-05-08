import iptools, ipaddress, argparse
from util.printfuncs import *


if __name__ == '__main__':
    parser = argparse.ArgumentParser('iplister.py', 'python3 iplister.py <infile> [-c|--compile]')
    parser.add_argument('infile', type=str, help='input File containing IP addresses / CIDRs / ranges')
    parser.add_argument('-c', '--compile', action='store_true', required=False, default=False, help='Compile addresses into CIDR ranges instead of expanding them')
    args = parser.parse_args()

    org, expanded, compiled = [], [], []
    with open(args.infile, 'r') as file:
        org = [line.strip() for line in file.readlines()]

    print_status(f'Expanding addresses from {len(org)} entries')
    for entry in org:
        if '-' in entry: # e.g., 1.2.3.4-1.2.3.6
            split = entry.split('-')
            start, end = split[0], split[1]
            ip_range = iptools.IpRange(start, end)

        else: # e.g., CIDR range or just one address
            ip_range = iptools.IpRange(entry)

        expanded.extend([str(ip) for ip in ip_range])


    expanded = list(set(expanded)) # deduplicate

    print_status(f'Expanded to {len(expanded)} total addresses')
    if args.compile:
        print_status(f'Compiling addresses into minimal CIDR list')
        ips = [ipaddress.IPv4Address(ip) for ip in expanded]
        compiled = [ip.with_prefixlen for ip in ipaddress.collapse_addresses(ips)]

        print('\n'.join(compiled))

    else: print('\n'.join(expanded))
    

