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

For some reason workflows triggered by tag pushes do not seem to update
the github pages documentation with new version numbers.  For that to
update properly a new commit needs to be pushed to the `main` branch.
Probably updating the `Change log` document and pushing to the `main`
branch would be enough.

  [gh]: https://github.com
  [vg]: https://setuptools.pypa.io/en/latest/userguide/distribution.html
  [st]: https://github.com/pypa/setuptools
  [pep440]: https://peps.python.org/pep-0440/

