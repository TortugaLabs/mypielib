#python3
from inspect import getframeinfo, stack

def src():
  '''Return file,line of caller

  :returns (str,int): file and line of caller

  Example:
  ```{doctest}

  >>> from mypielib.src import src
  >>> src()
  ('<doctest default[1]>', 1)

  ```
  '''
  caller = getframeinfo(stack()[1][0])
  return (caller.filename,caller.lineno)

if __name__ == '__main__':
  ...
  # ~ import doctest
  # ~ import sys
  # ~ mypielib = sys.modules[__name__]
  # ~ doctest.testmod()
