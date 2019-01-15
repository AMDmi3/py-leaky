#!/usr/bin/env python3

import argparse
import tracemalloc

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
elif args.func == 'leak_malloc':
    callee = leaky.leak_malloc
elif args.func == 'doublefree_malloc':
    callee = leaky.doublefree_malloc
else:
    raise RuntimeError('unknown func {}'.format(args.func))

def tracemalloc_wrapper(callee):
    tracemalloc.start()

    snapshot1 = tracemalloc.take_snapshot()
    callee()
    snapshot2 = tracemalloc.take_snapshot()

    top_stats = snapshot2.compare_to(snapshot1, 'lineno')

    print("tracemalloc stats:")
    for stat in top_stats:
        print(stat)

if args.tracemalloc:
    tracemalloc_wrapper(callee)
else:
    callee()
