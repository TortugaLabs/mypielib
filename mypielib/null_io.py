#python
import os

_saved_fds = []
'''Used internally to save fds by null_io'''

def null_io(close:bool = False, keep_stderr:bool = False):
  '''Redirects I/O to `/dev/null`

  :param bool close: Defaults to False, if True, the current I/O channels are closed
  :param bool keep_stderr: Default to False, if True, do not close stderr

  It will manipulate the operating sytems file descriptors and redirect them
  to `/dev/null`.  By default, it will save the existing file descriptors so
  that they can be restored later with `denull_io`.

  If `True` was passed as the `close` parameter, then previous file descriptors
  will be closed and `denull_io` will not work anymore.

  '''
  if close:
    if len(_saved_fds) == 0:
      null_fd = os.open(os.devnull,os.O_RDWR)
      os.dup2(null_fd, 0)
      os.dup2(null_fd, 1)
      if not keep_stderr: os.dup2(null_fd, 2)
      os.close(null_fd)
    else:
      _saved_fds[0].close()
      _saved_fds[1].close()
      if _saved_fds[2] is not None: _saved_fds[2].close()
      _saved_fds[3].close()
    return

  if len(_saved_fds) == 0:
    null_fd = os.open(os.devnull,os.O_RDWR)
    _saved_fds.append(os.dup(0))
    _saved_fds.append(os.dup(1))
    _saved_fds.append(None if keep_stderr else os.dup(2))
    _saved_fds.append(null_fd)
    _saved_fds.append(0)
  else:
    null_fd = _saved_fds[3]

  if _saved_fds[4]:
    # Already Nulled
    _saved_fds[4] += 1
    return

  _saved_fds[4] += 1
  os.dup2(null_fd, 0)
  os.dup2(null_fd, 1)
  if not keep_stderr: os.dup2(null_fd, 2)

def denull_io():
  '''Restores `null_io` redirections.
  '''
  _saved_fds[4] -= 1
  if _saved_fds[4]: return

  os.dup2(_saved_fds[0], 0)
  os.dup2(_saved_fds[1], 1)
  if _saved_fds[2] is not None: os.dup2(_saved_fds[2], 2)

