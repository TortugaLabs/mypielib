import re

WHITESPACE = r'\w+'
'''Regular expression for whitespace separator'''
COMMAS = r'\w*,\w*'
'''Regular expression for comma separated lists'''

def force_list(val: str|list, sep = WHITESPACE) -> list:
  '''Given a variable containing a string or a list, make sure it is a list

  :param val: value to validate
  :param sep: RE to split the string.  Use `WHITESPACE` as list separator
     or `COMMAS` if using commas.

  This is a simple function to make sure that entries that expect
  lists, can also accepts strings which are in turn converted into
  lists.
  '''
  if isinstance(val, str):
    return re.split(r'\W+', val)
  elif isinstance(val, list):
    return val
  raise TypeError(f'Expected str or list but got {type(val).__name__}')
