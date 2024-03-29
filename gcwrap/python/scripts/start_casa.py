import os
import sys
import traceback
if os.environ.has_key('LD_PRELOAD'):
    del os.environ['LD_PRELOAD']

import argparse
from casa_system_defaults import casa

from IPython import start_ipython
from traitlets.config.loader import Config
__pylib = os.path.dirname(os.path.realpath(__file__))
__init_scripts = [
    "init_system.py",
    "init_logger.py",
    "init_user_pre.py",
    "init_dbus.py",
    "init_tools.py",
    "init_tasks.py",
    "init_funcs.py",
    "init_pipeline.py",
    "init_mpi.py",
    "init_docs.py",
    "init_user_post.py",
    "init_crashrpt.py",
    "init_welcome.py",
]

##
## this is filled via register_builtin (from casa_builtin.py)
##
casa_builtins = { }

##
## this is filled via add_shutdown_hook (from casa_shutdown.py)
##
casa_shutdown_handlers = [ ]

try:
    __startup_scripts = filter( os.path.isfile, map(lambda f: __pylib + '/' + f, __init_scripts ) )

    __parse = argparse.ArgumentParser(description='CASA bootstrap',add_help=False)
    __parse.add_argument( '--rcdir',dest='rcdir',default=casa['dirs']['rc'],
                          help='location for startup files' )
    __parse.add_argument( '--pipeline',dest='backend',default='tk',
                          const=None,action='store_const',
                          help='startup with pipeline context' )
    __parse.add_argument( '--agg',dest='backend',default='tk',
                          const=None,action='store_const',
                          help='startup without tkagg' )
    __parse.add_argument( '--iplog',dest='ipython_log',default=False,
                          const=True,action='store_const',
                          help='create ipython log' )
    __defaults,__trash = __parse.parse_known_args( )
    from IPython import __version__ as _ipython_version_

    __configs = Config( )
    __configs.TerminalInteractiveShell.ipython_dir = __defaults.rcdir.decode('unicode-escape') + "/ipython"
    __configs.TerminalInteractiveShell.banner1 = 'IPython %s -- An enhanced Interactive Python.\n\n' % _ipython_version_
    __configs.TerminalInteractiveShell.banner2 = ''
    __configs.HistoryManager.hist_file = __configs.TerminalInteractiveShell.ipython_dir + "/history.sqlite"
    __configs.TerminalIPythonApp.matplotlib = __defaults.backend

    start_ipython( config=__configs, argv= (['--logfile='+casa['files']['iplogfile']] if __defaults.ipython_log else []) + ['--ipython-dir='+__defaults.rcdir+"/ipython", '--autocall=2', "-c", "for i in " + str(__startup_scripts) + ": execfile( i )"+("\n%matplotlib" if __defaults.backend is not None else ""), "-i" ] )

except:
    print "Unexpected error:", sys.exc_info()[0]
    traceback.print_exc(file=sys.stdout)
    pass


### this should (perhaps) be placed in an 'atexit' hook...
for handler in casa_shutdown_handlers:
    handler( )
