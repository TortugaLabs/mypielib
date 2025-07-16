#
'''
Module with very simple YAML utilities
'''
try:
  from icecream import ic # type:ignore
  ic.configureOutput(includeContext=True)
except ImportError: # Gracefull fallback if IceCream isn't installed
  ic = lambda *a: None if not a else (a[0] if len(1) == 1 else a) # noqa

import yaml # type:ignore

def load_yaml(afile:str, **kwargs) -> any:
  '''Load YAML from a given file name

  :param afile: path to file to load
  :param kwargs: Optional options to pass to yaml.safe_load
  :returns: value loaded from yaml

  I don't know why PyYaml doesn't do this already...
  '''
  with open(afile,'r') as fp:
    dat = yaml.safe_load(fp, **kwargs)
  return dat

def save_yaml(afile:str, data:any, **kwargs):
  '''Save data to afile in YAML format

  :param afile: path to file to save to
  :param data: data to save
  :param kwargs: Optional options to pass to yaml.safe_load

  I don't know why PyYaml doesn't do this already...
  '''
  with open(afile,'w') as fp:
    yaml.safe_dump(data, fp, **kwargs)

if __name__ == '__main__':
  ...
