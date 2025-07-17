# Developer Notes


## Releasing

Simply create a new tag and push it to [github][gh].  Make sure the tag follows
version [guidelines][vg] from [setuptools][st] which are based on [PEP440][pep440]

Sample versions:

- `1.0` or `1.2.3` -- normal release
- pre-releases
  - `1.0.a1` - alpha
  - `1.0.b1` - beta
  - `1.0.rc1` - release candidate
- `1.0.post1` - post release (or patch release)
- `1.0.dev1` - development release

  [gh]: https://github.com
  [vg]: https://setuptools.pypa.io/en/latest/userguide/distribution.html
  [st]: https://github.com/pypa/setuptools
  [plp440]: https://peps.python.org/pep-0440/
  
