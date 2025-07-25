
def readfile(name:str) -> str:
  '''Read the contents of a file as whole

  :param str name: File name to read
  :returns str: contents of file

  Examples:

  ```{doctest}

  >>> import mypielib.doctesting as dt
  >>> from mypielib.readfile import readfile
  >>> fp = dt.testfile('__data_for_readfile__test__')
  This is the contents of
  a sample test file
  >>> print(readfile(fp.name).rstrip())
  This is the contents of
  a sample test file

  ```
  '''
  with open(name,'r') as fp:
    text = fp.read()
  return text

if __name__ == '__main__':
  import doctest
  import os,sys
  sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
  failures, tests = doctest.testmod()
  print(f'Failures: {failures} of {tests} tests')
