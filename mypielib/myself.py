#python3
from inspect import getframeinfo, stack

def myself(climb=1):
  '''Return information of the caller

  :param climb: Defaults to 1, how far up the stack to climb
  :returns object: with attributes

  Among the attributes returned:

  - filename
  - lineno
  - function
  - code_context : list of lines being executed.

  ```{doctest}

  >>> from mypielib.myself import myself
  >>> trace = myself()
  >>> trace.lineno
  1
  >>> type(trace.filename)
  <class 'str'>


  ```

  '''
  caller = getframeinfo(stack()[climb][0])
  return caller

  ...

if __name__ == '__main__':
  import doctest
  import os,sys
  sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
  failures, tests = doctest.testmod()
  print(f'Failures: {failures} of {tests} tests')
