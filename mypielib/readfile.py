
def readfile(name:str) -> str:
  '''Read the contents of a file as whole

  :param str name: File name to read
  :returns str: contents of file

  Examples:

  ```{doctest}

  >>> from tempfile import NamedTemporaryFile
  >>> from mypielib.readfile import readfile
  >>> from mypielib.writefile import writefile
  >>> temp = NamedTemporaryFile('w')
  >>> writefile(temp.name,'this is a file')
  >>> readfile(temp.name)
  'this is a file'
  

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
