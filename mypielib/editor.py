'''
Run a OS specific editor
'''
import os
import subprocess
import tempfile
from mypielib.readfile import readfile

EDITOR_DEFAULTS = {
  'posix': 'vi',
  'nt': 'notepad',
  'java': None,   # No good defaults here...
}

def get_editor() -> str:
  '''Get user preferred editor

  :returns: Editor command to use

  Follows normal UNIX conventions:

  - VISUAL environment variable
  - EDITOR environment variable
  - just default to `vi`

  '''

  if 'VISUAL' in os.environ: return os.environ['VISUAL']
  if 'EDITOR' in os.environ: return os.environ['EDITOR']

  return EDITOR_DEFAULTS.get(os.name, None)

def edit(filename:str, check=True) -> int:
  ''' edit file

  :param filename: file to edit.
  :param check: If True, it will check the return code and raise an error

  '''
  rc = subprocess.run([get_editor(), filename],check=check)
  return rc.returncode

def edit_str(text:str, check=True) -> str:
  '''Edit a string using preferred editor

  :param text: text to edit.
  :param check: If True, it will check the return code and raise an error
  '''

  with tempfile.NamedTemporaryFile(delete_on_close=False) as fp:
    fp.write(bytes(text,encoding = 'ascii'))
    fp.close()
    subprocess.run([get_editor(),fp.name], check=check)
    return readfile(fp.name)

  raise RuntimeError('Unknown error')
