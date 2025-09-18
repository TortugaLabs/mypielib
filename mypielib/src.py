#python3
from inspect import getframeinfo, stack

def src(climb=1):
  '''Return file,line of caller

  :param climb: Defaults to 1, how far up the stack to climb
  :returns (str,int): file and line of caller

  Example:
  ```{doctest}

  >>> from mypielib.src import src
  >>> filename, lineno = src()
  >>> type(filename)
  <class 'str'>
  >>> lineno
  1

  ```
  '''
  caller = getframeinfo(stack()[climb][0])
  return (caller.filename,caller.lineno)

if __name__ == '__main__':
  import doctest
  import os,sys
  sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
  failures, tests = doctest.testmod()
  print(f'Failures: {failures} of {tests} tests')
