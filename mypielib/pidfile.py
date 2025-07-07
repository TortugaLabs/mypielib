import os

#
def pidfile(filename:str):
  '''Save current PID to a file

  :param str filename: File to save the current PID to
  '''

  with open(filename,"w") as fh:
    fh.write("%d\n" % os.getpid())
