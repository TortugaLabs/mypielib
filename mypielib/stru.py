'''
String utilities.
'''

def strtr(strng:str, replace:dict[str]) -> str:
  '''Replaces substrings defined in the `replace` dictionary with
  its replacement value.

  :param str string: String to convert
  :param dict replace: Mapping of string substitutions
  :returns str: string with the replaced contents

  Based on
  [phps-strtr-for-python](https://stackoverflow.com/questions/10931150/phps-strtr-for-python).

  Equivalent to php [strtr](https://www.php.net/manual/en/function.strtr.php)
  function.

  Example:
  ```{doctest}

  >>> from mypielib.stru import strtr
  >>> strtr('one two three',{'one': '1', 'two': '2', 'three': '3'})
  '1 2 3'

  ```

  '''
  buf, i = [], 0
  while i < len(strng):
    for s, r in replace.items():
      if strng[i:len(s)+i] == s:
        buf.append(r)
        i += len(s)
        break
    else:
      buf.append(strng[i])
      i += 1
  return ''.join(buf)

def ws_norm(inp:str) -> str:
  '''Normalize whitespace

  :param inp: input string
  :returns: string with whitespaces made consistent.

  Example:

  ```{doctest}

  >>> from mypielib.stru import ws_norm
  >>> ws_norm('Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...')
  'Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...'
  >>> ws_norm('  Neque    porro    quisquam          est    qui ')
  'Neque porro quisquam est qui'
  >>> ws_norm('           ')
  ''

  ```

  '''
  return ' '.join(inp.split())


if __name__ == '__main__':
  import doctest
  import os
  import sys
  sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
  failures, tests = doctest.testmod()
  print(f'Failures: {failures} of {tests} tests')

