import re

WHITESPACE = r'\s+'
'''Regular expression for whitespace separator'''
COMMAS = r'\s*,\s*'
'''Regular expression for comma separated lists'''
C_WS = r'\s*[,\s]\s*'
'''Regular expression for comma/whitespace'''

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

  >>> fl.force_list('this must be a list', fl.WHITESPACE)
  ['this', 'must', 'be', 'a', 'list']
  >>> fl.force_list(['one','two'],fl.WHITESPACE)
  ['one', 'two']
  >>> fl.force_list('this must, be a list', fl.COMMAS)
  ['this must', 'be a list']
  >>> fl.force_list('this must be a list', fl.COMMAS)
  ['this must be a list']
  >>> fl.force_list('this , must be, a list', fl.COMMAS)
  ['this', 'must be', 'a list']
  >>> fl.force_list('one two thre,,four,five six', fl.C_WS)
  ['one', 'two', 'thre', '', 'four', 'five', 'six']
  >>> fl.force_list('one two thre,,four,five six', fl.COMMAS)
  ['one two thre', '', 'four', 'five six']
  >>> fl.force_list('one two thre,,four,five six', fl.WHITESPACE)
  ['one', 'two', 'thre,,four,five', 'six']

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


