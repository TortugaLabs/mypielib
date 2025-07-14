'''
My private python library
'''

from .version import VERSION

from .cidr_to_netmask import cidr_to_netmask
from .daemonize import daemonize
from .file_args import file_args
from .gitver import gitver
from .myself import myself
from .null_io import null_io,denull_io
from .pidfile import pidfile
from .readfile import readfile
from .reaper import reap_child_proc
from .src import src
from .strtr import strtr
from .syslog_io import syslog_io
from .ts import timestamp,ts_print
from .unbuffered_io import unbuffered_io

