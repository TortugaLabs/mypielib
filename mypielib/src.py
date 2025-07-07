#python3
from inspect import getframeinfo, stack

def src():
  '''Return file,line of caller

  :returns (str,int): file and line of caller

  >>> src()
  ('<doctest __main__.src[0]>', 1)
  '''
  caller = getframeinfo(stack()[1][0])
  return (caller.filename,caller.lineno)

if __name__ == '__main__':
  import doctest
  doctest.testmod()
