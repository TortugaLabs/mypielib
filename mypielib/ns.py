'''
Basic Namespace class


'''
class BasicNamespace:
  '''This is a barebones basic namespace class

  Examples:

  ```{doctest}

  >>> from mypielib.ns import BasicNamespace
  >>> x = BasicNamespace(a=1,b=2)
  >>> x
  BasicNamespace(a=1, b=2)
  >>> x.a
  1
  >>> x.b
  2
  >>> x.a = 5
  >>> x
  BasicNamespace(a=5, b=2)
  >>> x.a
  5

  ```

  This is a very barebones namespace class.  You probably should use
  [types.SimpleNamespace](https://docs.python.org/3/library/types.html#types.SimpleNamespace)
  or
  [collections.namedtuple](https://docs.python.org/3/library/collections.html#collections.namedtuple)
  instead.
  '''
  def __init__(self, **kwargs):
    self.__dict__.update(kwargs)

  def __repr__(self):
    keys = sorted(self.__dict__)
    items = ("{}={!r}".format(k, self.__dict__[k]) for k in keys)
    return "BasicNamespace({})".format(", ".join(items))

  def __eq__(self, other):
    if isinstance(self, BasicNamespace) and isinstance(other, BasicNamespace):
      return self.__dict__ == other.__dict__
    return NotImplemented

if __name__ == '__main__':
  import doctest
  import os
  import sys
  sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
  failures, tests = doctest.testmod()
  print(f'Failures: {failures} of {tests} tests')
