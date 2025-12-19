

def boolval(value:str) -> bool:
  '''Convert a string to boolean

  :param value: bool-like string value
  :returns: True or False depending on value.

  Examples:
  ```{doctest}

  >>> from mypielib.boolval import boolval
  >>> boolval('true')
  True
  >>> boolval('y')
  True
  >>> boolval('n')
  False
  >>> boolval('false')
  False
  >>> boolval('0')
  False

  ```

  '''
  if isinstance(value, bool): return value  # Already a bool

  yes_s = {'true', '1', 'yes', 'y', 'on', 'enable', 'enabled'}
  no_s = {'false', '0', 'no', 'n', 'off', 'disable', 'disabled'}

  if isinstance(value, str):
    val = value.strip().lower()
    if val in yes_s:
      return True
    elif val in no_s:
      return False
    elif val.isnumeric():
      return int(val) != 0
    raise ValueError(f'Invalid boolean string: {value}')

  raise TypeError(f'Invalid passed type: {type(value).__name__}')

if __name__ == '__main__':
  import doctest
  import os
  import sys
  sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
  failures, tests = doctest.testmod()
  print(f'Failures: {failures} of {tests} tests')
