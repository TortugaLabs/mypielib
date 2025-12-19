'''
CLI utilties
'''
try:
  from icecream import ic
except ImportError:  # Graceful fallback if IceCream isn't installed.
  ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)  # noqa

import argparse
import os
import subprocess
import sys
from typing import TextIO

from mypielib.version import VERSION

def make_parser():
  ''' Command Line Interface argument parser '''
  name = sys.argv[0]
  if os.path.basename(name) == '__main__.py': name = os.path.basename(os.path.dirname(name))

  cli = argparse.ArgumentParser(prog=name, description='Command line utilities')
  cli.add_argument('-V','--version', action='version', version=f'%(prog)s {VERSION}')

  subs = cli.add_subparsers(dest='command', help='Available subcommands')

  sub0 = subs.add_parser('xxargs',help ='Like xargs but with file_args support')
  sub0.add_argument('-d','--delimiter',default = '\n', type=str,
                    help='Input items are terminated by the specified character')
  sub0.add_argument('-0','--null',action='store_const', dest='delimiter', const = '\0',
                    help='Input items are terminated by a null character')
  sub0.add_argument('-s','--space',action='store_const', dest='delimiter', const = None,
                    help='Input items are terminated by whitespace')
  sub0.add_argument('-a','--arg-file', type=argparse.FileType('r'), default=sys.stdin,
                    help='Read items from file instead of standard input.')
  sub0.add_argument('-n','--max-args', type=int, default=None,
                    help='Use at most max-args arguments per command line.')
  sub0.add_argument('-o','--open-tty', action='store_true', default=False,
                    help='Reopen stdin as /dev/tty in the child process before executing the command.')
  sub0.add_argument('-t','--verbose', action='store_true', default=False,
                    help='Print the command line on the standard error output before executing it.')
  sub0.add_argument('cmd',nargs='*', default=[],
                    help='Command to execute')

  return cli


def exec_cmd(cmd:list[str], input_fh = None, verbose:bool  = False):
  '''Execute the command

  :param cmd: command to execute
  :param input_fh: File handle to use for stdin
  :param verbose: print command before running
  '''
  if verbose:
    sys.stderr.write(' '.join(cmd))
    sys.stderr.write('\n')

  result = subprocess.run(cmd, stdin = input_fh)
  ic(result)
  if result.returncode: sys.exit(result.returncode)


def xxargs(args:argparse.Namespace):
  '''Run a command-like xargs

  :param str|None args.delimiter: Character used for delimiter.  If None, it will use whitespace.
  :param file-handle args.arg_file: Input file handle
  :param int|None args.max_args: Max args in command line
  :param bool args.open_tty: Re-open stdin as /dev/tty
  :param bool args.verbose: Print command-line on stderr
  :param list[str] args.cmd: Command to execute
  '''

  input_fh = open('/dev/tty' if args.open_tty else '/dev/null')
  prefix = args.cmd if len(args.cmd) else ['echo']

  if args.delimiter is None:
    last_ch = ' '
    validate_ch = lambda ch: ch.isspace()
    cmd_queue = [ ]
  else:
    last_ch = None
    validate_ch = lambda ch: ch == args.delimiter
    cmd_queue = [ '' ]

  while (ch := args.arg_file.read(1)) != '':
    ic(ch)
    if validate_ch(ch):
      if args.max_args is not None and len(cmd_queue) == args.max_args:
        exec_cmd(prefix + cmd_queue, input_fh, args.verbose)
        cmd_queue = [ '' ]
      if args.delimiter is not None:
        ic(last_ch)
        cmd_queue.append('')
      ic(ch, cmd_queue)
    else:
      if args.delimiter is None and validate_ch(last_ch): cmd_queue.append('')
      cmd_queue[-1] += ch
    last_ch = ch

  if len(cmd_queue):
    exec_cmd(prefix + cmd_queue, input_fh, args.verbose)
  sys.exit(0)

if __name__ == '__main__':
  cli = make_parser()
  args = cli.parse_args()
  ic(args)
  if args.command is None:
    cli.print_help()
    sys.exit(0)
  elif args.command == 'xxargs':
    xxargs(args)
  else:
    raise RuntimeError(f'Command {args.command} not implemented')

