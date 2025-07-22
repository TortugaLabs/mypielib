'''
Tools for running doctests

Let's you prepare input files and/or strings by examining docstrings.
It will use the passed "marker" string to identify the right
docscring.  Therefore the "marker" needs to be somewhat unique.

Example:

```python
    |>>> import mypielib.doctesting as dt
    |>>> import testmodule
    |>>> fp = dt.testfile("__testmodule_foo_data___")
    |This is the content for foo function
    |it can contain multiple lines
    |<BLANKSPACE>
    |>>> foo(fp.name)
    |True
    |
    |>>> dat = dt.teststr("__testmodule_bar_data___")
    |This is test data
    |>>> bar(dat)
    |0x45996
```

'''
try:
  from icecream import ic # type:ignore
  ic.configureOutput(includeContext=True)
except ImportError: # Gracefull fallback if IceCream isn't installed
  ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a) # noqa

from inspect import stack, ismodule
from typing import TextIO, Any
from tempfile import NamedTemporaryFile

import sys


def _find_docstr(marker:str, obj:Any,no_loop:set|None = None) -> str|None:
  '''Try to retrieve the doc string...'''
  if no_loop is None: no_loop = set()

  if ismodule(obj):
    # Special handling for modules...
    if not hasattr(obj,'__file__'): return None
    for k in dir(obj):
      v = getattr(obj, k)
      if hasattr(v,'__doc__') and isinstance(v.__doc__, str) and (marker in v.__doc__):
        return v.__doc__

      if ismodule(v) and not (v.__name__ in no_loop):
        no_loop.add(v.__name__)
        txt = _find_docstr(marker,v, no_loop)
        if not txt is None: return txt
    return None

  for k,v in obj.items():
    # ic(k,type(v))
    if hasattr(v,'__doc__') and isinstance(v.__doc__, str) and (marker in v.__doc__):
      return v.__doc__

    if ismodule(v) and not (v.__name__ in no_loop):
      no_loop.add(v.__name__)
      txt = _find_docstr(marker,v, no_loop)
      if not txt is None: return txt

  return None


def _extract_str(marker:str, text:str|None) -> str|None:
  '''Extract the test data from the docstring
  '''
  if text is None: return text
  # ic(marker,text)

  # Determine the exact location of marker
  mrkrpos = text.find(marker)
  bol = text.rfind('\n',0,mrkrpos)+1
  start = text.find('\n', mrkrpos + len(marker) + 2)+1
  # ic(mrkrpos, bol, start)
  if start == 0: return None

  # Calculate indentation...
  # ic(text[bol:start])
  i = bol
  while i < start and text[i].isspace(): i += 1
  prefix = text[bol:i]
  # ic(prefix)
  if prefix != '' and not prefix.isspace(): return None

  # Remove continuation lines...
  lenprefix3 = len(prefix)+3
  prefixcont = prefix + '...'
  # ic(lenprefix3, prefixcont)
  while text[start:start+lenprefix3] == prefixcont:
    start = text.find('\n',start+lenprefix3)+1
    if start == 0: return None

  # OK found the actual begining of test data
  # determine the end of test data
  end = start
  prefixnext = prefix + '>>>'

  # ic(end,prefixnext)
  while end < len(text):
    if text[end:end+lenprefix3] == prefixnext:
      # Found the ">>>" line
      break
    n = text.find('\n', end)+1
    if n == 0:
      # Reached the end of the string
      end = len(text)
      break
    if text[end:n].isspace():
      # This was a blank line
      break
    end = n

  # ic(end)

  # Remove indetation
  text = ('\n'.join([item[len(prefix):] if item.startswith(prefix) else item for item in text[start:end].split('\n')])).rstrip()

  # matched = text if  (zz:=text.find('\n')) == -1 else (text[:zz] + "...")
  # ic(marker, matched)
  return text


def teststr(marker:str) -> str|None:
  '''Returns a test string from docstrings

  :param marker: used to identify the test data from data files
  :returns: str or None

  ```{doctest}

  >>> import mypielib.doctesting as dt
  >>> fp = dt.testfile('==cdkd==lksjdflsdf===lskdjf==')
  This is sample
  one string dos
  >>> print(fp.read().rstrip())
  This is sample
  one string dos

  >>> txt = dt.teststr('abskkk385485jdklsdjf')
  This is sample
  What a day
  >>> print(txt.rstrip())
  This is sample
  What a day


  ```
  '''
  frame = stack()[1].frame
  text = _extract_str(marker, _find_docstr(marker, dict(frame.f_locals)))
  if text is None:
    return None
  print(text)
  return text

def testfile(marker:str) -> TextIO|None:
  '''Returns a temporary test file from docstrings

  :param marker: used to identify the test data from data files
  :returns: TextIO object or None

  ```{doctest}

  >>> from mypielib.readfile import readfile
  >>> import mypielib.doctesting as dt
  >>> fp = dt.testfile('abcd-kdkc-llllskd')
  This is sample
  one string
  >>> print(readfile(fp.name).rstrip())
  This is sample
  one string

  ```

  '''
  doctext = _extract_str(marker, _find_docstr(marker, dict(stack()[1].frame.f_locals)))
  if doctext is None: return None
  print(doctext)
  temp = NamedTemporaryFile('w+', delete_on_close=False)
  temp.write(doctext)
  temp.write('\n')
  temp.flush()
  temp.seek(0)
  return temp

if __name__ == '__main__':
  import doctest
  import os,sys
  sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
  failures, tests = doctest.testmod()
  print(f'Failures: {failures} of {tests} tests')
