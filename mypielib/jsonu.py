#
'''
Module with very simple JSON utilities
'''
import json

try:
  from icecream import ic # type:ignore
  ic.configureOutput(includeContext=True)
except ImportError: # Gracefull fallback if IceCream isn't installed
  ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a) # noqa


def load_json(afile:str, **kwargs) -> any:
  '''Load JSON from a given file name

  :param afile: path to file to load
  :param kwargs: Additional optional keywords to be pass to json.dump
  :returns: value loaded from json

  Examples:

  ```{doctest}

  >>> from mypielib.jsonu import load_json
  >>> import mypielib.doctesting as dt
  >>> fp = dt.testfile('--data-for-load_json---')
  { "one": 1, "two": "dos", "list": [1,2,3]}
  >>> load_json(fp.name)
  {'one': 1, 'two': 'dos', 'list': [1, 2, 3]}

  ```

  '''
  with open(afile,'r') as fp:
    dat = json.load(fp, **kwargs)
  return dat

def save_json(afile:str, data:any, **kwargs):
  '''Save data to afile in JSON format

  :param afile: path to file to save to
  :param data: data to save
  :param kwargs: Additional optional keywords to be pass to json.dump

  ```{doctest}
  
  >>> from tempfile import NamedTemporaryFile
  >>> from mypielib.readfile import readfile
  >>> temp = NamedTemporaryFile('w')

  >>> from mypielib.jsonu import save_json
  >>> save_json(temp.name, {'one': 1, 'two': 'dos', 'list': [1, 2, 3]})
  >>> readfile(temp.name)
  '{"one": 1, "two": "dos", "list": [1, 2, 3]}'

  ```

  '''
  with open(afile,'w') as fp:
    json.dump(data, fp, **kwargs)

  ...
if __name__ == '__main__':
  import doctest
  import os
  import sys
  sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
  failures, tests = doctest.testmod()
  print(f'Failures: {failures} of {tests} tests')
