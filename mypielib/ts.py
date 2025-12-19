#
# Time stamping
#
import sys
import time

TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S %z"
'''Time format to use'''

#
# Format timestamp
#
def timestamp(ts:float|None = None) -> str:
  '''Format a time stamp string

  :param float|None ts: Time stamp to create, omit if using current time
  :returns str: Formatted time stamp

  Example:

  ```{doctest}
  >>> import os
  >>> os.environ['TZ'] = 'UTC'
  >>> from mypielib.ts import timestamp
  >>> timestamp(0)
  '1970-01-01 00:00:00 +0000'
  >>> timestamp(1752660896)
  '2025-07-16 10:14:56 +0000'

  ```

  '''


  if ts is None: ts = time.time()
  return time.strftime(TIMESTAMP_FORMAT, time.localtime(ts))

#
# Prepends output with a timestamp
#
def ts_print(msg:str, io=None):
  '''Prepends output with a time stamp

  :param str msg: Message to display
  :param file-handle io: If specified, output file handle, otherwise uses stderr
  '''
  if io is None:  io = sys.stderr

  prefix = "[" + time.strftime(TIMESTAMP_FORMAT) + "]:"
  io.write(prefix + msg + "\n")

if __name__ == '__main__':
  import doctest
  import os
  import sys
  sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
  failures, tests = doctest.testmod()
  print(f'Failures: {failures} of {tests} tests')
