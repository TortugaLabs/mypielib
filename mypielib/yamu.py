#
'''
Module with very simple YAML utilities
'''
try:
  from icecream import ic # type:ignore
  ic.configureOutput(includeContext=True)
except ImportError: # Gracefull fallback if IceCream isn't installed
  ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a) # noqa

import yaml # type:ignore

def load_yaml(afile:str, **kwargs) -> any:
  '''Load YAML from a given file name

  :param afile: path to file to load
  :param kwargs: Optional options to pass to yaml.safe_load
  :returns: value loaded from yaml

  I don't know why PyYaml doesn't do this already...


  ```{doctest}

  >>> from mypielib.yamu import load_yaml
  >>> import mypielib.doctesting as dt
  >>> fp = dt.testfile('--test-file-load-yaml---')
  one: 1
  two: dos
  list: [ 1, 2, 3]
  >>> load_yaml(fp.name)
  {'one': 1, 'two': 'dos', 'list': [1, 2, 3]}

  
  ```

  '''
  with open(afile,'r') as fp:
    dat = yaml.safe_load(fp, **kwargs)
  return dat

def save_yaml(afile:str, data:any, **kwargs):
  '''Save data to afile in YAML format

  :param afile: path to file to save to
  :param data: data to save
  :param kwargs: Optional options to pass to yaml.safe_load

  I don't know why PyYaml doesn't do this already...

  ```{doctest}
  
  >>> from tempfile import NamedTemporaryFile
  >>> from mypielib.readfile import readfile
  >>> temp = NamedTemporaryFile('w')

  >>> from mypielib.yamu import save_yaml
  >>> save_yaml(temp.name, {'one': 1, 'two': 'dos', 'list': [1, 2, 3]})
  >>> readfile(temp.name).replace(chr(10),'%0A')
  'list:%0A- 1%0A- 2%0A- 3%0Aone: 1%0Atwo: dos%0A'
  

  ```

  '''
  with open(afile,'w') as fp:
    yaml.safe_dump(data, fp, **kwargs)

if __name__ == '__main__':
  import doctest
  import os
  import sys
  sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
  failures, tests = doctest.testmod()
  print(f'Failures: {failures} of {tests} tests')
