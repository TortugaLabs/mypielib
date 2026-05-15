#python3

from typing import Any


def get_nested_value(path_string: str, nested_dict: dict) -> Any:
  '''
  Retrieve a value from a deeply nested dictionary using a dot-separated path.

  :param path_string: A string with dot-separated keys, e.g., 'something.or.other'
  :param nested_dict: A deeply nested dictionary
  :returns: The value at the specified path
  :raises KeyError: If any key in the path doesn't exist
  :raises TypeError: If a path segment leads to a non-dict value

  Examples:

  ```{doctest}

  >>> from mypielib.get_nested import get_nested_value
  >>> get_nested_value('a.b.c', {'a': {'b': {'c': 42}}})
  42

  >>> get_nested_value('x', {'x': 'hello'})
  'hello'

  >>> get_nested_value('missing.key', {'a': 1})
  Traceback (most recent call last):
  ...
  KeyError: 'missing'

  ```
  '''
  keys = path_string.split('.')
  current = nested_dict
  for key in keys:
    current = current[key]
  return current


if __name__ == '__main__':
  import doctest
  import os
  import sys
  sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
  failures, tests = doctest.testmod()
  print(f'Failures: {failures} of {tests} tests')
