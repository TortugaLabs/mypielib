'''
Get version using git description
'''
try:
  from icecream import ic
except ImportError:  # Graceful fallback if IceCream isn't installed.
  ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)  # noqa

from inspect import getframeinfo, stack 
import os
import re
import sys
import subprocess

try:
  from packaging.version import Version, InvalidVersion
except ImportError:
  ...

def is_valid_version(version_string:str) -> bool:
  '''Test if the version is valid

  :param version_string: string to test
  :returns: True if valid, False if invalid
  '''
  try:
    # Attempt to create a Version object; this will validate the version string
    Version(version_string)
    return True
  except InvalidVersion:
    # If an InvalidVersion exception is raised, the version string is invalid
    return False

def gitver(script_dir:str|None = None, setup_ver:bool = False, default = None ) -> str|None:
  '''use `git describe` to get version info

  :param script_dir: working directory for git repo
  :param setup_ver: sanitize version so it can be used in `setuptools`.
  :param default: returns this value in case of error
  :returns: string with version info or None on error
  '''
  try:
    # Get the directory where this script is located
    env_type = os.getenv('GITHUB_REF_TYPE','unknown')
    if env_type == 'tag':
      env = os.getenv('GITHUB_REF_NAME',None)
      if not env is None: return env

    if script_dir is None:
      caller = getframeinfo(stack()[1][0])
      script_dir = os.path.dirname(os.path.abspath(caller.filename))
      ic(caller.filename)
    

    # Run the command with subprocess.run in the script's directory
    result = subprocess.run(
        ['git', 'describe'],
        cwd=script_dir,           # Set the current working directory
        stdout=subprocess.PIPE,   # Capture standard output
        stderr=subprocess.PIPE,   # Capture standard error (optional)
        text=True,                # Decode bytes to string
        check=True                # Raise a CalledProcessError for non-zero exit codes
    )

    # The output is available in result.stdout
    vs = result.stdout.strip()
    if setup_ver:
      if mv := re.match(r'^(.+)-(\d+)-(g[0-9a-f]+)',vs):
        vs = f'{mv.group(1)}a{mv.group(2)}+{mv.group(3)}'
      if not is_valid_version(vs): vs = default
    return vs
  except subprocess.CalledProcessError as e:
    sys.stderr.write(f"Warning: An error occurred while running git describe: {e.stderr.strip()}\nUnknown module version.\n")
    return default
  except Exception as e:
    sys.stderr.write(f"Unexpected error: {e}\n")
    return default


if __name__ == '__main__':
  ic(gitver())
