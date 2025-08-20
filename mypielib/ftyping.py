'''
Unix types utilities
'''
import os
import stat

def is_block(path:str) -> bool:
  '''Determine if path is a block device

  :param path: device path to check
  :returns: True or False depending on the test result
  '''
  try:
    mode = os.stat(path).st_mode
    return stat.S_ISBLK(mode)
  except (FileNotFoundError, PermissionError):
    return False

def is_char(path:str) -> bool:
  '''Determine if path is a character special device

  :param path: device path to check
  :returns: True or False depending on the test result
  '''
  try:
    mode = os.stat(path).st_mode
    return stat.S_ISCHR(mode)
  except (FileNotFoundError, PermissionError):
    return False

def is_fifo(path:str) -> bool:
  '''Determine if path is a FIFO

  :param path: device path to check
  :returns: True or False depending on the test result
  '''
  try:
    mode = os.stat(path).st_mode
    return stat.S_ISFIFO(mode)
  except (FileNotFoundError, PermissionError):
    return False

def is_link(path:str) -> bool:
  '''Determine if path is a symlink

  :param path: device path to check
  :returns: True or False depending on the test result
  '''
  try:
    mode = os.stat(path).st_mode
    return stat.S_ISLNK(mode)
  except (FileNotFoundError, PermissionError):
    return False

def is_sock(path:str) -> bool:
  '''Determine if path is a UNIX socket

  :param path: device path to check
  :returns: True or False depending on the test result
  '''
  try:
    mode = os.stat(path).st_mode
    return stat.S_ISSOCK(mode)
  except (FileNotFoundError, PermissionError):
    return False


# Don't really know how to test this...
