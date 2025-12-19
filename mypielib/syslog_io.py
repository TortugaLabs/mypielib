#
# Makes the output of process to be logged on syslog
#
import os
import sys

def _io_syslog(fh,tag):
  """
  Redirects the output of a file handle to syslog with a specified tag.

  This function forks a child process to read from a pipe connected to the
  file handle provided. It reads lines from the file handle, removes trailing
  whitespace, and sends non-empty lines to syslog, prefixed with the given tag.

  :param file-hanlde fh: The file handle whose output will be redirected to syslog.
  :param str tag: The tag to prefix log messages with, identifying the source of the log.

  Note:
  - The function handles stdout and stderr redirection, closing these streams
    in the child process to prevent interference.
  - The child process terminates after processing the input.
  """
  r,w = os.pipe()
  cpid = os.fork()
  if cpid == 0:
    # Child...
    os.close(w)
    sys.stdin.close()
    sys.stdout.close()
    sys.stderr.close()
    fin = os.fdopen(r)

    # ~ x = open('log-%s.txt' % tag,'w')
    import syslog

    for line in fin:
      line = line.rstrip()
      if not line: continue
      syslog.syslog("%s: %s" % (tag,line))
      # ~ x.write("%s: %s\n" % (tag,line))
      # ~ x.flush()
    sys.exit(0)

  os.close(r)
  os.dup2(w, fh.fileno())
  os.close(w)

def syslog_io(tag:str):
  '''Re-directs stdio output to syslog with the given tag

  :param str tag: tag to show on syslog
  '''
  _io_syslog(sys.stdout,'%s(out)' % tag)
  _io_syslog(sys.stderr,'%s(err)' % tag)

