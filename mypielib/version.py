'''
Report my module version information
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

def _get_git_description(default:str|None = None) -> str|None:
  '''use `git describe` to get version info

  :param default: returns this value in case of error
  :returns: string with version info or None on error

  This is in-line here because we do not want dependancies.
  '''
  try:
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
        stderr=subprocess.PIPE,   # Capture standard error (optional)
        text=True,                # Decode bytes to string
        check=True                # Raise a CalledProcessError for non-zero exit codes
    )

    # The output is available in result.stdout
    vs = result.stdout.strip()
    if mv := re.match(r'^(.+)-(\d+)-(g[0-9a-f]+)',vs):
      vs = f'{mv.group(1)}a{mv.group(2)}+{mv.group(3)}'
    if VCHECK:
      try:
        # Attempt to create a Version object; this will validate the version string
        Version(vs)
      except InvalidVersion:
        # If an InvalidVersion exception is raised, the version string is invalid
        return default
    return vs
  except subprocess.CalledProcessError as e:
    sys.stderr.write(f"Warning: An error occurred while running git describe: {e.stderr.strip()}\nUnknown module version.\n")
    return default
  except Exception as e:
    sys.stderr.write(f"Unexpected error: {e}\n")
    return default


VERSION = _get_git_description()
'''git based version'''


if __name__ == '__main__':
  print(VERSION)
