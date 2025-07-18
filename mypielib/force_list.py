import re

WHITESPACE = r'\W+'
'''Regular expression for whitespace separator'''
COMMAS = r'\W*,\W*'
'''Regular expression for comma separated lists'''

def force_list(val: str|list, sep = WHITESPACE) -> list:
  '''Given a variable containing a string or a list, make sure it is a list

  :param val: value to validate
  :param sep: RE to split the string.  Use `WHITESPACE` as list separator
     or `COMMAS` if using commas.

  This is a simple function to make sure that entries that expect
  lists, can also accepts strings which are in turn converted into
  lists.

  Examples:

  ```{doctest}

  >>> import mypielib.force_list as fl
  
  >>> fl.force_list('this must be a list')
  ['this', 'must', 'be', 'a', 'list']
  >>> fl.force_list(['one','two'])
  ['one', 'two']
  >>> fl.force_list('this must, be a list', fl.COMMAS)
  ['this must', 'be a list']
  >>> fl.force_list('this must be a list', fl.COMMAS)
  ['this must be a list']
  >>> fl.force_list('this , must be, a list', fl.COMMAS)
  ['this', 'must be', 'a list']
  

  ```

  '''
  if isinstance(val, str):
    return re.split(sep, val)
  elif isinstance(val, list):
    return val
  raise TypeError(f'Expected str or list but got {type(val).__name__}')

if __name__ == '__main__':
  import doctest
  import os,sys
  sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
  failures, tests = doctest.testmod()
  print(f'Failures: {failures} of {tests} tests')
