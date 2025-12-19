'''
My private python library
'''

from .version import VERSION
# only purpose of `_keep` is to fake the usage of a few symbols
# such that the star imports are not flagged as dead code.
# It does nothing at runtime.
def _keep(x): pass

_keep(VERSION)
