#!/usr/bin/env python3

import argparse
import tracemalloc
import sys

import leaky


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-t', '--tracemalloc', action='store_true', help='enable tracemalloc')
parser.add_argument('func', help='test function to call')
args = parser.parse_args()

if args.func == 'no_leak':
    callee = leaky.no_leak
elif args.func == 'leak_int':
    callee = leaky.leak_int
elif args.func == 'doublefree_int':
    callee = leaky.doublefree_int
elif args.func == 'leak_none':
    callee = leaky.leak_none
elif args.func == 'doublefree_none':
    callee = leaky.doublefree_none
elif args.func == 'leak_malloc':
    callee = leaky.leak_malloc
elif args.func == 'doublefree_malloc':
    callee = leaky.doublefree_malloc
elif args.func == 'leak_pymem':
    callee = leaky.leak_pymem
elif args.func == 'doublefree_pymem':
    callee = leaky.doublefree_pymem
else:
    raise RuntimeError('unknown func {}'.format(args.func))

def tracemalloc_wrapper(callee):
    tracemalloc.start()

    snapshot1 = tracemalloc.take_snapshot()
    callee()
    snapshot2 = tracemalloc.take_snapshot()

    filters = (tracemalloc.Filter(False, tracemalloc.__file__),)
    snapshot1 = snapshot1.filter_traces(filters)
    snapshot2 = snapshot2.filter_traces(filters)

    leaks = False
    for stat in snapshot2.compare_to(snapshot1, 'lineno'):
        if stat.size_diff != 0:
            print(stat)
            leaks = True

    if leaks:
        sys.exit(1)

if args.tracemalloc:
    tracemalloc_wrapper(callee)
else:
    callee()
