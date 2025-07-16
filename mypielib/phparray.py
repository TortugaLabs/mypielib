'''
PHP array like functions
'''
LOWER = 0
UPPER = 1

def change_key_case(array:dict, case:int=LOWER):
  '''Changes the case of all keys in an dict

  :param array: dictionary to change key case
  :param case: LOWER (0) or UPPER (1)
  :returns: modified dict

  Returns an dict with all keys lowercased or uppercased. Numbered
  keys are left as is.

  Examples:

  ```{doctest}

  >>> import mypielib.phparray as phparray
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

  Examples:

  ```{doctest}

  >>> import mypielib.phparray as phparray
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

  Examples:

  ```{doctest}

  >>> import mypielib.phparray as phparray
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


if __name__ == '__main__':
  import doctest
  import os,sys
  sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
  failures, tests = doctest.testmod()
  print(f'Failures: {failures} of {tests} tests')
