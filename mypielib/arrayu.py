'''
PHP array like functions and other structure like
stuff.
'''
from typing import Callable, Any
import sys

LOWER = 0
'''Lower case characters'''
UPPER = 1
'''Upper case characters'''


def change_key_case(array:dict, case:int=LOWER):
  '''Changes the case of all keys in an dict

  :param array: dictionary to change key case
  :param case: LOWER (0) or UPPER (1)
  :returns: modified dict

  Returns an dict with all keys lowercased or uppercased. Numbered
  keys are left as is.

  This is equivalent to PHP's [array_change_key_case](https://www.php.net/manual/en/function.array-change-key-case.php)


  Examples:

  ```{doctest}

  >>> import mypielib.arrayu as phparray
  >>> x = {'one': 1, 'two': 2, 'three': 3, 792: 'none' }
  >>> phparray.change_key_case(x, phparray.UPPER)
  {'ONE': 1, 'TWO': 2, 'THREE': 3, 792: 'none'}
  >>> phparray.change_key_case(x)
  {'one': 1, 'two': 2, 'three': 3, 792: 'none'}

  ```
  '''
  if case == LOWER:
    f = str.lower
  elif case == UPPER:
    f = str.upper
  else:
    raise ValueError(f'case {case} should be LOWER ({LOWER}) or UPPER ({UPPER})')
  return dict((f(k) if isinstance(k,str) else k, v) for k, v in array.items())

def flip(array:dict) -> dict:
  '''Exchanges all keys with their associated values in dict

  :param array: dictionary to flip
  :returns: flipped dictionary

  flip() returns an dictioanry in flip order, i.e. keys from
  dictionary become values and values from dictionary become
  keys.

  Note that the values of dictionary need to be valid keys, i.e.
  they need to be either int or string. An TypeError exception
  is thrown if a value has the wrong type.

  If a value has several occurrences, the latest key will be used as
  its value, and all others will be lost.

  This is similar to PHP's [array_flip](https://www.php.net/manual/en/function.array-flip.php)

  Examples:

  ```{doctest}

  >>> import mypielib.arrayu as phparray
  >>> x = { 1: 2, 3: 4 }
  >>> phparray.flip(x)
  {2: 1, 4: 3}

  ```
  '''
  return dict((v, k) for k, v in array.items())


def merge_recursive(*arrays:list[dict]) -> dict:
  '''Merge one or more dicts recursively

  :param arrays: List of arrays to recursively merge.

  merges the elements of one or more dicts together so that the
  values of one are appended to the end of the previous one. It
  returns the resulting dict.

  If the input dict have the same string keys, then the values for
  these keys are merged together into an dict, and this is done
  recursively, so that if one of the values is a dict itself, the
  function will merge it with a corresponding entry in another dict
  too. If, however, the dicts have the same numeric key, the later
  value will not overwrite the original value, but will be appended.

  This is similar to PHP's [array_merge_recursive](https://www.php.net/manual/en/function.array-merge-recursive.php)


  Examples:

  ```{doctest}

  >>> import mypielib.arrayu as phparray
  >>> a1 = dict(color = dict(favorite='red'), five = 5)
  >>> a2 = dict(diez = 10, color = dict(favorite='green', hated='blue'))
  >>> phparray.merge_recursive(a1, a2)
  {'color': {'favorite': 'green', 'hated': 'blue'}, 'five': 5, 'diez': 10}


  ```
  '''
  array1 = dict()
  for array in arrays:
    for key, value in array.items():
      if key in array1:
        if isinstance(value, dict):
          array[key] = merge_recursive(array1[key], value)
        if isinstance(value, (list, tuple)):
          array[key] += array1[key]
    array1.update(array)
  return array1

def traverse(data:Any, callback:Callable[[Any],None]):
  '''
  Recursively walk a nested structure of dicts and lists,
  applying the `callback` function to each leaf node.

  :param data: The input data structure, which may be a dict, list, or any other type.
  :param callback: function to call

  Examples:

  ```{doctest}

  >>> import mypielib.arrayu as arrayu
  >>> def runme(x): print(x)
  >>> arrayu.traverse(['one','two',{'uno': 1, 'dos': 2},[3,4]],runme)
  one
  two
  1
  2
  3
  4

  ```
  '''
  if isinstance(data, dict):
    for key, value in data.items():
      traverse(value, callback)
  elif isinstance(data, list):
    for item in data:
      traverse(item, callback)
  else:
    callback(data)

def transform(data:list|dict, callback:Callable[[Any],Any]):
  '''
  Recursively walk a nested structure of dicts and lists,
  applying a transformation to each leaf node using the `callback` function.

  :param data: The input data structure, which may be a dict, list, or any other type.
  :param callback: function to call

  Examples:

  ```{doctest}

  >>> import mypielib.arrayu as arrayu
  >>> def runme(x): return x.upper() if isinstance(x,str) else x
  >>> inp = ['one','two',{'uno': 'wot', 'dos': 'not'},[3,4,'yes','maybe']]
  >>> arrayu.transform(inp,runme)
  >>> inp
  ['ONE', 'TWO', {'uno': 'WOT', 'dos': 'NOT'}, [3, 4, 'YES', 'MAYBE']]
  >>> def greeter(x,y): return f'{y} greets {x}' if isinstance(x,str) and isinstance(y,str) else x
  >>> arrayu.transform(inp, lambda val: greeter(val, 'Alice'))
  >>> inp
  ['Alice greets ONE', 'Alice greets TWO', {'uno': 'Alice greets WOT', 'dos': 'Alice greets NOT'}, [3, 4, 'Alice greets YES', 'Alice greets MAYBE']]

  ```
  '''
  if isinstance(data, dict):
    for key in list(data.keys()):  # Avoid RuntimeError during mutation
      if isinstance(data[key],dict) or isinstance(data[key],list):
        transform(data[key], callback)
      else:
        newitem = callback(data[key])
        if newitem != data[key]: data[key] = newitem
  elif isinstance(data, list):
    for i in range(len(data)):
      if isinstance(data[i],dict) or isinstance(data[i],list):
        transform(data[i], callback)
      else:
        newitem = callback(data[i])
        if newitem != data[i]: data[i] = newitem
  else:
    raise TypeError('Only dict or list allowed')

def add_uniq(lst:list, value:Any) -> bool:
  '''Append a value to a list only if doesn't exist already

  :param lst: List to modify
  :param value: value to append
  :returns: True if lst was modified, else False

  Examples:

  ```{doctest}

  >>> import mypielib.arrayu as arrayu
  >>> l = [ 1,2,3,4 ]
  >>> arrayu.add_uniq(l, 3)
  False
  >>> l
  [1, 2, 3, 4]
  >>> arrayu.add_uniq(l,5)
  True
  >>> l
  [1, 2, 3, 4, 5]
  
  ```
  '''
  if value in lst: return False
  lst.append(value)
  return True

class LtPython3_7Error(Exception):
  pass

def sort_structure(obj:Any) -> Any:
    """
    Recursively sort dictionaries but preserve list order.

    :param obj: structure to sort
    :returns: sorted structure

    Examples:

    ```{doctest}

  >>> import mypielib.arrayu as arrayu
    >>> arrayu.sort_structure({
    ...    'user': {'name': 'Alice', 'age': 30},
    ...    'roles': ['editor', 'admin']
    ... }) # doctest: +NORMALIZE_WHITESPACE
    {'roles': ['editor', 'admin'],
     'user': {'age': 30, 'name': 'Alice'}}

    ```
    """
    if sys.version_info < (3,7):
      raise LtPython3_7Error('Calling sort_structure requires version Python 3.7 or newer!\n')
    if isinstance(obj, dict):
      return {k: sort_structure(obj[k]) for k in sorted(obj)}
    elif isinstance(obj, list):
      return [sort_structure(item) for item in obj]
    else:
      return obj



if __name__ == '__main__':
  import doctest
  import os

  sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
  failures, tests = doctest.testmod()
  print(f'Failures: {failures} of {tests} tests')
