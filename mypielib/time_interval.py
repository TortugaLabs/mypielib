

def _tiv_segment(itxt:str, secs:int, interval:int, one:str, many:str) -> tuple[str,int]:
  i, secs = divmod(secs , interval)
  tx = one if i == 1 else many.format(i)
  if itxt:
    if i == 0:
      return itxt
    else:
      return itxt + ', ' + tx, secs
  else:
    return tx, secs


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
  >>> time_interval(86400*1000+3945)
  '1,000 days, one hour, 5 minutes, 45 seconds'
  >>> time_interval(3600+20)
  'one hour, 20 seconds'
  >>> time_interval(3600+20, True)
  'one hour'

  ```
  '''
  if secs >= 86400:
    txt, secs = _tiv_segment('', secs, 86400, 'one day', '{:,} days')
    if rough: return txt
  else:
    txt = ''
  if secs >= 3600:
    txt, secs = _tiv_segment(txt, secs, 3600, 'one hour', '{:,} hours')
    if rough: return txt
  if secs >= 60:
    txt, secs = _tiv_segment(txt, secs, 60, 'one minute', '{:,} minutes')
    if rough: return txt

  if secs == 0:
    if txt: return txt
    return 'zero seconds'
  if rough: return 'a few seconds'

  txt, secs = _tiv_segment(txt, secs, 1, 'second', '{:,} seconds')
  return txt

if __name__ == '__main__':
  import doctest
  import os
  import sys
  sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
  failures, tests = doctest.testmod()
  print(f'Failures: {failures} of {tests} tests')
