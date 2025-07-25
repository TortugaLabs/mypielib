'''
Report my module version information

It defines two values:

- `VERSION` : module version (using git describe or release tag)
- `SETUP_VERSION` : version string suitable for `setuptools`
   If the version string doesn't match `setuptools` rules, then
   it is set to `None`.
'''
import os
import re
import sys
import subprocess
try:
  from icecream import ic
except ImportError:  # Graceful fallback if IceCream isn't installed.
  ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)  # noqa

try:
  from packaging.version import Version, InvalidVersion
  VCHECK = not 'NO_VCHECK' in os.environ
except ImportError:
  VCHECK = False

def _get_git_description() -> str:
  '''use `git describe` to get version info

  :returns: string with version info or None on error

  This is in-line here because we do not want dependancies.
  '''
  # Get the directory where this script is located
  if 'tag' == os.getenv('GITHUB_REF_TYPE','unknown'):
    env = os.getenv('GITHUB_REF_NAME',None)
    if env: return env

  script_dir = os.path.dirname(os.path.abspath(__file__))

  # Run the command with subprocess.run in the script's directory
  result = subprocess.run(
        ['git', 'describe'],
        cwd=script_dir,           # Set the current working directory
        stdout=subprocess.PIPE,   # Capture standard output
        text=True,                # Decode bytes to string
  )
  if result.returncode == 0: return result.stdout.strip()

  result = subprocess.run(
        ['git', 'describe','--always'],
        cwd=script_dir,           # Set the current working directory
        stdout=subprocess.PIPE,   # Capture standard output
        text=True,                # Decode bytes to string
  )
  if result.returncode == 0: return f'$git:{result.stdout.strip()}$'

  return '$unknown$'

VERSION = _get_git_description()
'''git based version'''
if VCHECK:
  SETUP_VERSION = VERSION
  try:
    # Attempt to create a Version object; this will validate the version string
    Version(SETUP_VERSION)
  except InvalidVersion:
    # If an InvalidVersion exception is raised, the version string is invalid
    SETUP_VERSION = None
else:
  SETUP_VERSION = None

if __name__ == '__main__':
  print('VERSION',VERSION)
  print('SETUP_VERSION', SETUP_VERSION)
