'''
Report my module version information
'''
import os
import sys
import subprocess

try:
  from .gitver import gitver
except ImportError:
  from gitver import gitver

VERSION = gitver(setup_ver = bool(os.getenv('IN_SETUPTOOLS',None)))
'''git based version'''

try:
  from icecream import ic
except ImportError:  # Graceful fallback if IceCream isn't installed.
  ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)  # noqa

if __name__ == '__main__':
  try:
    from icecream import ic
  except ImportError:  # Graceful fallback if IceCream isn't installed.
    ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)  # noqa
  ic(VERSION)
