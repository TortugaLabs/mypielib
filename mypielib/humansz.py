"""

Retrieved from: https://github.com/kamrankausar/Python-Small-Utility-Programms/blob/master/humansize.py

Created on Thu Dec 28 22:40:20 2017

@author: genius
"""

# Define the Dictonary
_SUFFIXES = {1000: ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
            1024: ['KiB', 'MiB', 'Gib', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']}

# Define the function

def humansz(size:int, a_1024:bool = True) -> str:
  ''' Convert a file size to human-readable form.

  :param size: file size in bytes
  :param a_1024:  if True (default), use multiple of 1024
            if false, use multiple of 1000
  :return: string

  Examples:

  ```{doctest}

  >>> from mypielib.humansz import humansz
  >>> humansz(10000000000,False)
  '10.0 GB'
  >>> humansz(10000000000)
  '9.3 Gib'

  ```

  '''
  if size < 0: raise ValueError('Number must be negative')


  multiple = 1024 if a_1024 else 1000
  for suffix in _SUFFIXES[multiple]:
   size /= multiple
   if size < multiple: return f'{size:.1f} {suffix}'

  raise ValueError('Number too Large')

if __name__ == '__main__':
  import doctest
  import os,sys
  sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
  failures, tests = doctest.testmod()
  print(f'Failures: {failures} of {tests} tests')
