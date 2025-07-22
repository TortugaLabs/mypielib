#python
import os
import shlex
import sys

def file_args(inargs:list[str]) -> list[str]:
  """Read arguments from files

  :param list args: arguments to process
  :returns list: replacement args

  Arguments that begin with '@' are replaced with the contents
  of an argument file or a single '@' followed by a filename.
  Unless the file does not exists and then the argument is just
  added as is.

  Argument file syntax follows `shlex` semantics with comments
  enabled.

  Note that if using Python's `argparse`, you can simply use the
  `fromfile_prefix_chars` option.

  ```{donttest}
  
  >>> from mypielib.file_args import file_args
  >>> import mypielib.doctesting as dt
  >>> fp = dt.testfile('---data-for-file_args---')
  this "is a" file
  one
  >>> file_args(['@'+fp.name,'blah','bloh'])
  ['this', 'is a', 'file', 'one', 'blah', 'bloh']
  

  ```


  """
  outargs = []
  i = 0
  while i < len(inargs):
    arg = inargs[i]
    if arg.startswith('@'):
      filename = arg[1:] if arg != '@' else inargs[i+1] if i+1 < len(inargs) else None
      if (not filename is None) and os.path.isfile(filename):
        if len(outargs) == 0: outargs = inargs[:i]
        with open(filename,'r') as fp:
          outargs.extend(shlex.split(fp.read(), True, True))
        i += 2 if arg == '@' else 1
        continue
    if len(outargs) > 0: outargs.append(inargs[i])
    i += 1

  if len(outargs) == 0: return inargs
  return outargs


if __name__ == '__main__':
  import doctest
  import os,sys
  sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
  failures, tests = doctest.testmod()
  print(f'Failures: {failures} of {tests} tests')
