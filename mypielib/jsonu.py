#
'''
Module with very simple JSON utilities
'''
import json

try:
  from icecream import ic # type:ignore
  ic.configureOutput(includeContext=True)
except ImportError: # Gracefull fallback if IceCream isn't installed
  ic = lambda *a: None if not a else (a[0] if len(1) == 1 else a) # noqa


def load_json(afile:str, **kwargs) -> any:
  '''Load JSON from a given file name

  :param afile: path to file to load
  :param kwargs: Additional optional keywords to be pass to json.dump
  :returns: value loaded from json

  '''
  with open(afile,'r') as fp:
    dat = json.safe_load(fp, **kwargs)
  return dat

def save_json(afile:str, data:any, **kwargs):
  '''Save data to afile in JSON format

  :param afile: path to file to save to
  :param data: data to save
  :param kwargs: Additional optional keywords to be pass to json.dump

  '''
  with open(afile,'w') as fp:
    json.dump(data, fp, **kwargs)

if __name__ == '__main__':
  ...
