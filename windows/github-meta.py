'''
Play around with github meta data
'''
try:
  from icecream import ic
except ImportError:  # Graceful fallback if IceCream isn't installed.
  ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)  # noqa

import os
import re
import sys
import subprocess
from packaging.version import Version, InvalidVersion


def check_version(tag:str) -> [bool,bool|None]:
  '''
  Check if a version string is valid and determine if it is a pre-release.

  :param tag: The version string to be checked.

  :returns: A tuple containing:
      - A boolean indicating if the version string is valid.
      - A boolean indicating if the version string is a pre-release.
        If the version is invalid, this will be None.

  Example:

  ```{doctest}
  
  >>> check_version('1.0.0-alpha')
  (True, True)

  >>> check_version('1.0.0')
  (True, False)

  >>> check_version('invalid-version')
  (False, None)

  ```
  '''
  try:
    version = Version(tag)
    is_valid = True
    is_pre_release = version.is_prerelease
  except InvalidVersion:
    is_valid = False
    is_pre_release = None
  
  return is_valid, is_pre_release

def gitrun(cmd:list[str], wd:str =".") -> str|None:
  '''Run git command

  :param cmd: command line to execute
  :param wd: working directory
  :returns: stdout of command or the default value if non-zero return code
  
  Will run the given command capturing standard output
  '''
  result = subprocess.run(cmd,
                            cwd=wd,
                            stdout=subprocess.PIPE,
                            text=True,
                            )
  if result.returncode: return None
  return result.stdout.strip()
  
def sanitize(text:str) -> str:
  '''Sanitize output for GITHUB_OUTPUT

  :param text: text to sanitize
  :returns: sanitized string
  '''
  return text.replace('%','%25').replace('\n','%0A').replace('\r','%0D')

def main():
  output_lines = dict()

  if (github_output := os.getenv('GITHUB_OUTPUT',None)) is None:
    sys.stderr.write('No GITHUB_OUTPUT found\n')
  else:
    print('... GITHUB_OUTPUT', github_output) 

  if (github_repo := os.getenv('GITHUB_REPOSITORY', None)) is None:
    sys.stderr.write('No GITHUB_REPOSITORY found\n')
    sys.exit(1)
  print('... GITHUB_REPOSITORY', github_repo)

  pkgname = os.path.basename(github_repo)
  if not os.path.isdir(pkgname):
    sys.stderr.write(f'{pkgname}: directory not found\n')
    sys.exit(1)

  output_lines['PYPKG'] = pkgname

  if os.getenv('GITHUB_REF_TYPE','unknown') == 'tag':
    pkgver = os.getenv('GITHUB_REF_NAME',None)
    print('GITHUB_REF_NAME', pkgver)

    is_valid, prerelease = check_version(pkgver)

    if is_valid:
      output_lines['PRERELEASE'] = 'true' if prerelease else 'false'
      pkgid = pkgver
    else:
      output_lines['PRERELEASE'] = 'true'
      pkgid = 'pre'

    body = gitrun(['git','show','-s','--format=%B', pkgver,'--'])    
    output_lines['RELTEXT'] = '' if body is None else body
  else:
    pkgver = gitrun(['git','describe'])
    if pkgver is None:
      pkgver = gitrun(['git','describe','--always'])
      pkgver = '$unknown$' if pkgver is None else f'$git:{pkgver}$'
    pkgid = 'snapshot' 
    is_valid, _ = check_version(pkgver)
    output_lines['PRERELEASE'] = 'true'

  output_lines['PKGID'] = pkgid
  output_lines['PKGVER'] = pkgver

  text = 'VERSION = "{version}"\nSETUP_VERSION = {setup}\n'.format(
                version = pkgver,
                setup = f"'{pkgver}'" if is_valid else 'None'
                )

  print('+++ version.py')
  print('==============================')
  print(text)
  print('==============================')
  if os.path.isfile(f'{pkgname}/version.py'):
    wrversion = os.getenv('WRITE_VERSION', None)
    if wrversion is None:
      sys.stderr.write(f'Setenv WRITE_VERSION to "1" to write to {pkgname}/version.py\n')
    elif wrversion  == '1':
      sys.stderr.write(f'Updating {pkgname}/version.py\n')
      with open(f'{pkgname}/version.py','w') as fp:
        fp.write(text)
    else:
      sys.stderr.write(f'WRITE_VERSION is not set to "1" will not write to  {pkgname}/version.py\n')
  else:
    sys.stderr.write(f'{pkgname}/version.py: file does not exist!\n')
  
  if len(output_lines) > 0:
    if github_output:
      with open(github_output,'a') as fp:
        for k,v in output_lines.items():
          print(f'{k}={sanitize(v)}')
          fp.write(f'{k}={sanitize(v)}\n')
    else:
      sys.stderr.write('Displaying GITHUB_OUTPUT to the screen only...\n')
      for k,v in output_lines.items():
        print(f'{k}={sanitize(v)}')

def load_args(args:list[str]):
  '''Load args into the current environment

  :param args: list of key=value elements to load.

  `os.environ` is updated
  '''
  for i in args:
    if '=' in i:
      k,v = i.split('=',1) 
      os.environ[k] = v
    else:
      os.environ[i] = 'true'

load_args(sys.argv[1:])
main()
