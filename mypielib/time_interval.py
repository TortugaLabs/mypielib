

def time_interval(secs:int, rough:bool = False) -> str:
  '''
  Converts a value in seconds into a string describing the time interval

  :param secs: value in seconds
  :param rough: Defaults to `False`.  If `True` only a rough value is returned
  :returns: string

  ```{doctest}

  >>> from mypielib.time_interval import time_interval
  >>> time_interval(10)
  '10 seconds'
  >>> time_interval(10,True)
  'a few seconds'
  >>> time_interval(0)
  'zero seconds'
  >>> time_interval(0,True)
  'zero seconds'
  >>> time_interval(60)
  'one minute'
  >>> time_interval(120)
  '2 minutes'
  >>> time_interval(244)
  '4 minutes, 4 seconds'
  >>> time_interval(244,True)
  '4 minutes'
  >>> time_interval(3600)
  'one hour'
  >>> time_interval(86400*5+3945)
  '5 days, one hour, 5 minutes, 45 seconds'

  ```
  '''
  q = ''
  if secs >= 86400:
    i = int(secs / 86400)
    if i == 1:
      txt = 'one day'
    else:
      txt = f'{i:,} days'
    if rough: return txt
    secs = secs % 86400
    q = ', '
  else:
    txt = ''

  if secs >= 3600:
    i = int(secs/3600)
    if i == 1:
      txt += q + 'one hour'
    else:
      txt += q + f'{i} hours'
    if rough: return txt
    secs = secs % 3600
    if q == '': q = ', '

  if secs >= 60:
    i = int(secs/60)
    if i == 1:
      txt += q + 'one minute'
    else:
      txt += q + f'{i} minutes'
    if rough: return txt
    secs = secs % 60
    if q == '': q = ', '

  if rough: return 'zero seconds' if secs == 0  else 'a few seconds'

  if secs == 1:
    txt += q + 'one second'
  elif secs > 0:
    txt += q + f'{secs} seconds'
  elif secs == 0 and txt == '':
    return 'zero seconds'

  return txt

if __name__ == '__main__':
  import doctest
  import os,sys
  sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
  failures, tests = doctest.testmod()
  print(f'Failures: {failures} of {tests} tests')
