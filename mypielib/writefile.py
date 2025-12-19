
def writefile(name:str, data:str|bytes, offset:int=0, mode:str = 'w', truncate:bool = False):
  '''Write the contents of a file as whole

  :param name: File name to write
  :param data: data to write
  :param offset: start writing at the given offset
  :param truncate: will truncate the file

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
  with open(name,f'{mode}{"b" if isinstance(data,bytes) else ""}') as fp:
    if offset: fp.seek(offset)
    fp.write(data)
    if truncate: fp.truncate()

if __name__ == '__main__':
  import doctest
  import os
  import sys
  sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
  failures, tests = doctest.testmod()
  print(f'Failures: {failures} of {tests} tests')
