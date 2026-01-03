#!/home/alex/t/mypielib/dev/pys.sh python
# PYTHON_ARGCOMPLETE_OK
'''
Configure argparse from a data structure

Supports [argcomplete](https://github.com/kislyuk/argcomplete)
when available.

Examples:

```{doctest}

>>> import mypielib.argparse_cfg as argparse_cfg
>>> from mypielib.version import VERSION
>>> parser = argparse_cfg.make_parser([
...    (['-V','--version'], dict(help='Show version',
...                             action='version',
...                             version=f'%(prog)s {VERSION}')),
...    (['--timeout'], dict(help='Time out value', type=int,
...                                 completer=argparse_cfg.hint_factory('SECONDS'))),
...    ([argparse_cfg.CFG.GROUP, 'modes', 'parser mode'], [
...         (argparse_cfg.CFG.REQ_MXGROUP, [
...            ('--send', dict(help='Send mode', dest='mode', action='store_const', const='send')),
...            ('--recv', dict(help='Recv mode', dest='mode', action='store_const', const='recv')),
...         ]),
...       ]),
...    ([argparse_cfg.CFG.SUBPARSER,dict(help='sub functions',dest='function', callable='func')],[
...        (['list','ls','ll'], dict(help='list command', callable=lambda x: print(str(x)),
...          args = [
...              (['-l','--long'], dict(help='Long mode', action='store_true')),
...            ])),
...      ]
...    ),
...    ],prog='myprogram',exit_on_error = False)
>>> parser.print_help()   # doctest: +NORMALIZE_WHITESPACE
usage: myprogram [-h] [-V] [--timeout TIMEOUT] (--send | --recv) {list,ls,ll} ...
<BLANKLINE>
positional arguments:
  {list,ls,ll}       sub functions
    list (ls, ll)    list command
<BLANKLINE>
options:
  -h, --help         show this help message and exit
  -V, --version      Show version
  --timeout TIMEOUT  Time out value
<BLANKLINE>
modes:
  parser mode
<BLANKLINE>
  --send             Send mode
  --recv             Recv mode
>>> parser.parse_args('--send'.split(' '))
Namespace(timeout=None, mode='send', function=None)
>>> parser.parse_args('--recv'.split(' '))
Namespace(timeout=None, mode='recv', function=None)
>>> parser.parse_args('--recv --send'.split(' '))
Traceback (most recent call last):
argparse.ArgumentError: argument --send: not allowed with argument --recv
>>> parser.parse_args('--ver'.split(' '))
Traceback (most recent call last):
SystemExit: 0

```

'''

import argparse
import sys
from typing import Any
try:
  from icecream import ic
except ImportError:  # Graceful fallback if IceCream isn't installed.
  ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)  # noqa
try:
  import argcomplete
except ImportError: # Gracefull fallback if argcomplete isnt' installed.
  class argcomplete:
    def autocomplete(parser):
      pass


class CFG:
  '''Class containing string constants'''
  GROUP = '180$76'
  '''Create an argument group'''
  OPT_MXGROUP = '180$79'
  '''Marker constant indicating an optional mutually exclusive group'''
  REQ_MXGROUP = '180$78'
  '''Marker constant indicating a required mutually exclusive group'''
  SUBPARSER = '180$77'
  '''Marker constant indicating a subparser'''
  CALLABLE = 'callable'
  '''When defining a sub-parser group,
  the name of the attribute in the namespace that will receive callable functions.

  When defining a sub-parser, the function that will be called.
  '''
  FUNCTION = 'function'
  '''The default attribute name for CALLABLE'''
  ARGS = 'args'
  '''key for arguments to a sub-parsers'''
  COMPLETER = 'completer'
  '''Attribute for defining a completer function'''
  DONT_COMPLETE = 'do_not_complete'
  '''A kwarg to disable argcomplete'''

def hint_factory(msg:str):
  '''Helper function to create a readline tab completion function

  :param msg: this is the hint to show when pressing Tab
  :returns: completion function.

  '''
  def hint_callable(prefix, parsed_args, **kwargs):
    if prefix == '': return [ msg, '=']
    return []
  return hint_callable

def _add_arg(sub:argparse.ArgumentParser|argparse._MutuallyExclusiveGroup,
            opts:list|str, kwargs:dict):
  '''Helper function used to load argument options

  :param sub: sub parser
  :param opts: varargs list
  :param kwargs: keyword args dictionary

  Handles completer options.
  '''
  if not isinstance(opts,list): opts = [opts]
  if CFG.COMPLETER in kwargs:
    completer = kwargs[CFG.COMPLETER]
    del kwargs[CFG.COMPLETER]
    sub.add_argument(*opts, **kwargs).completer = completer
  else:
    sub.add_argument(*opts, **kwargs)

def _argparser_factory(kwargs:dict[Any]) -> argparse.ArgumentParser:
  '''Create an argument parser

  Plays with the passed keywords switching defaults around.
  '''
  for kw,val in [
          ('fromfile_prefix_chars', '@'),
        ]:
    if kw not in kwargs: kwargs[kw] = val
  if sys.version_info >= (3,14,0):
    for kw,val in [
            ('suggest_on_error', True),
          ]:
      if kw not in kwargs: kwargs[kw] = val

  skip_complete = False
  if CFG.DONT_COMPLETE in kwargs:
    skip_complete = kwargs[CFG.DONT_COMPLETE]
    del kwargs[CFG.DONT_COMPLETE]
  parser = argparse.ArgumentParser(**kwargs)
  if not skip_complete: argcomplete.autocomplete(parser)
  return parser

def _add_subparsers(parser:argparse.ArgumentParser, subopts:dict[Any], kwargs:list[Any]):
  '''Create sub parser definitions...
  '''
  callable_name = CFG.FUNCTION
  if CFG.CALLABLE in subopts:
    callable_name = subopts[CFG.CALLABLE]
    del subopts[CFG.CALLABLE]
  subs = parser.add_subparsers(**subopts)
  for sp, spopts in kwargs:
    if isinstance(sp,str): sp = [sp]
    args = spopts[CFG.ARGS]
    del spopts[CFG.ARGS]
    if CFG.CALLABLE in spopts:
      callme = spopts[CFG.CALLABLE]
      del spopts[CFG.CALLABLE]
    else:
      callme = None

    subparser = subs.add_parser(sp[0],aliases=sp[1:], **spopts)
    make_parser(args, subparser)
    if callme is not None:
      subparser.set_defaults(**{callable_name: callme})

def make_parser(argopts:list[Any],
                parser:argparse.ArgumentParser|None = None,
                **kwargs) -> argparse.ArgumentParser:
  '''Configure argparser

  :param argopts: configuration
  :param parser: Use this parser instead of creating a new one.
  :param kwargs:  Additional kwargs passwd to ArgumentParser constructor

  '''
  if parser is None:
    parser = _argparser_factory(kwargs)

  for opts,kwargs in argopts:
    if opts == CFG.OPT_MXGROUP or opts[0] == CFG.OPT_MXGROUP:
      group = parser.add_mutually_exclusive_group()
      make_parser(kwargs, group)
    elif opts == CFG.REQ_MXGROUP or opts[0] == CFG.REQ_MXGROUP:
      group = parser.add_mutually_exclusive_group(required=True)
      make_parser(kwargs, group)
    elif opts == CFG.GROUP or opts[0] == CFG.GROUP:
      if isinstance(opts,str): opts = [CFG.GROUP]
      group = parser.add_argument_group(*opts[1:])
      make_parser(kwargs, group)
    elif opts[0] == CFG.SUBPARSER:
      _add_subparsers(parser, opts[1], kwargs)
    else:
      _add_arg(parser, opts, kwargs)

  return parser



if __name__ == '__main__':
  import doctest
  import os
  import sys
  sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
  failures, tests = doctest.testmod()
  print(f'Failures: {failures} of {tests} tests')




