#!/usr/bin/env python
''' Installation script for stats_lectures package '''

import os
import sys
from os.path import join as pjoin, dirname

# BEFORE importing distutils, remove MANIFEST. distutils doesn't properly
# update it when the contents of directories change.
if os.path.exists('MANIFEST'): os.remove('MANIFEST')

import numpy as np

# Get version and release info, which is all stored in regreg/info.py
ver_file = os.path.join('stats_lectures', 'info.py')
# Use exec for compabibility with Python 3
exec(open(ver_file).read())

# force_setuptools can be set from the setup_egg.py script
if not 'force_setuptools' in globals():
    # For some commands, use setuptools
    if len(set(('develop', 'bdist_egg', 'bdist_rpm', 'bdist', 'bdist_dumb',
                'bdist_mpkg', 'install_egg_info', 'egg_info',
                'easy_install')).intersection(sys.argv)) > 0:
        force_setuptools = True
    else:
        force_setuptools = False

if force_setuptools:
    # Try to preempt setuptools monkeypatching of Extension handling when Pyrex
    # is missing.  Otherwise the monkeypatched Extension will change .pyx
    # filenames to .c filenames, and we probably don't have the .c files.
    sys.path.insert(0, pjoin(dirname(__file__), 'fake_pyrex'))
    import setuptools

# We may just have imported setuptools, or we may have been exec'd from a
# setuptools environment like pip
if 'setuptools' in sys.modules:
    extra_setuptools_args = dict(
        tests_require=['nose'],
        test_suite='nose.collector',
        zip_safe=False,
        extras_require = dict(
            doc=['Sphinx>=1.0'],
            test=['nose>=0.10.1']),
        install_requires = [])
    # I removed numpy and scipy from install requires because easy_install seems
    # to want to fetch these if they are already installed, meaning of course
    # that there's a long fragile and unnecessary compile before the install
    # finishes.
    # We need setuptools install command because we're going to override it
    # further down.  Using distutils install command causes some confusion, due
    # to the Pyrex / setuptools hack above (force_setuptools)
    from setuptools.command import install
else:
    extra_setuptools_args = {}
    from distutils.command import install

# Import distutils _after_ potential setuptools import above, and after removing
# MANIFEST
from distutils.core import setup
from distutils.extension import Extension

from cythexts import cyproc_exts, get_pyx_sdist
from setup_helpers import package_check

# Define extensions
EXTS = []
for modulename, other_sources in ():
    pyx_src = pjoin(*modulename.split('.')) + '.pyx'
    EXTS.append(Extension(modulename,[pyx_src] + other_sources,
                          include_dirs = [np.get_include(),
                                         "src"]))
# Cython is a dependency for building extensions, iff we don't have stamped
# up pyx and c files.
extbuilder = cyproc_exts(EXTS, CYTHON_MIN_VERSION, 'pyx-stamps')


# Do our own build and install time dependency checking. setup.py gets called in
# many different ways, and may be called just to collect information (egg_info).
# We need to set up tripwires to raise errors when actually doing things, like
# building, rather than unconditionally in the setup.py import or exec

# Installer that checks for install-time dependencies
class installer(install.install):
    def run(self):
        package_check('numpy', NUMPY_MIN_VERSION)
        package_check('scipy', SCIPY_MIN_VERSION)
        install.install.run(self)


cmdclass = dict(
    build_ext=extbuilder,
    install=installer,
    sdist=get_pyx_sdist())


def main(**extra_args):
    setup(name=NAME,
          maintainer=MAINTAINER,
          maintainer_email=MAINTAINER_EMAIL,
          description=DESCRIPTION,
          long_description=LONG_DESCRIPTION,
          url=URL,
          download_url=DOWNLOAD_URL,
          license=LICENSE,
          classifiers=CLASSIFIERS,
          author=AUTHOR,
          author_email=AUTHOR_EMAIL,
          platforms=PLATFORMS,
          version=VERSION,
          requires=REQUIRES,
          provides=PROVIDES,
          packages     = ['stats_lectures',
                          'stats_lectures.stats60',
                          ],
          ext_modules = EXTS,
          package_data = {'stats_lectures':['data/*', 'cards/*']},
          data_files=[],
          scripts= [],
          cmdclass = cmdclass,
          **extra_args
         )

#simple way to test what setup will do
#python setup.py install --prefix=/tmp
if __name__ == "__main__":
    main(**extra_setuptools_args)
