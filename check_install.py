#!/usr/bin/env python
""" Script to check and install dependencies for stats 191 and 306b

Run with:

    python check_install.py
"""
from __future__ import print_function

import sys
from os.path import join as pjoin, isdir
from subprocess import Popen, PIPE
from distutils.version import LooseVersion
import shutil
# Requires Python 2.7
from argparse import ArgumentParser

MIN_IPYTHON='1.0.0'
PROFILE_NAME='stats'
R_LIBS=['knitr', 'stringr', 'alr3']


def back_tick(cmd, ret_err=False, as_str=True, raise_err=None):
    """ Run command `cmd`, return stdout, or stdout, stderr if `ret_err`

    Roughly equivalent to ``check_output`` in Python 2.7

    Parameters
    ----------
    cmd : sequence
        command to execute
    ret_err : bool, optional
        If True, return stderr in addition to stdout.  If False, just return
        stdout
    as_str : bool, optional
        Whether to decode outputs to unicode string on exit.
    raise_err : None or bool, optional
        If True, raise RuntimeError for non-zero return code. If None, set to
        True when `ret_err` is False, True if `ret_err` is True

    Returns
    -------
    out : str or tuple
        If `ret_err` is False, return stripped string containing stdout from
        `cmd`.  If `ret_err` is True, return tuple of (stdout, stderr) where
        ``stdout`` is the stripped stdout, and ``stderr`` is the stripped
        stderr.

    Raises
    ------
    Raises RuntimeError if command returns non-zero exit code
    """
    if raise_err is None:
        raise_err = False if ret_err else True
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    retcode = proc.returncode
    cmd_str = ' '.join(cmd) if isinstance(cmd, (list, tuple)) else cmd
    if retcode is None:
        proc.terminate()
        raise RuntimeError(cmd_str + ' process did not terminate')
    if raise_err and retcode != 0:
        raise RuntimeError(cmd_str + ' process returned code %d' % retcode)
    out = out.strip()
    if as_str:
        out = out.decode('latin-1')
    if not ret_err:
        return out
    err = err.strip()
    if as_str:
        err = err.decode('latin-1')
    return out, err


def check_R():
    try:
        back_tick(['R', '--version'])
    except RuntimeError:
        print("You may need to install R - see http://www.R-project.org")
        return False
    print('R: OK')
    return True


def check_rpy2():
    try:
        import rpy2
    except ImportError:
        print('Need rpy2 python package installed - see: '
              'http://rpy.sourceforge.net for instructions')
        return False
    print('rpy2: OK')
    return True


def check_rlib(name):
    out, err = back_tick(
        ['R', '--slave', '-e', 'library({0})'.format(name)],
        ret_err=True)
    if 'Error in library' in err:
        print("Missing R library '{0}'; "
              "try `install.packages('{0}')` in R".format(name))
        return False
    print("R library '{0}': OK".format(name))
    return True


def check_ipython():
    try:
        import IPython
    except ImportError:
        print('Need ipython installed - see '
              'http://ipython.org for instructions')
        return False
    if LooseVersion(IPython.__version__) < LooseVersion(MIN_IPYTHON):
        print('Version of IPython is too old; please upgrade - see '
              'http://ipython.org for instructions')
        return False
    print('IPython: OK')
    return True


def install_profile(name, clobber, progname):
    profile_sdir = 'profile_' + name
    from IPython.utils.path import get_ipython_dir
    ip_dir = get_ipython_dir()
    out_path = pjoin(ip_dir, profile_sdir)
    if isdir(out_path):
        if not clobber:
            print('ipython profile "{0}" exists; not overwriting. '
                  'Use {1} --clobber option to overwrite'.format(
                      name, progname))
            return False
        shutil.rmtree(out_path)
    shutil.copytree(profile_sdir, out_path)
    print('Installed profile {0} - use with `ipython notebook '
          '--profile={0}`'.format(name))
    return True


def main():
    parser = ArgumentParser(
        description='Check / install script for stats notebooks')
    parser.add_argument('--clobber', action='store_true',
                        help='if set, overwrite existing profile directory')
    args = parser.parse_args()
    if check_R():
        for name in R_LIBS:
            check_rlib(name)
    check_rpy2()
    if check_ipython():
        install_profile(PROFILE_NAME, args.clobber, sys.argv[0])


if __name__ == '__main__':
    main()
