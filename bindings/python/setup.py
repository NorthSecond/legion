import argparse
from distutils.core import setup
from distutils.command.build_py import build_py
import os, sys, platform

import legion_cffi_build

import legion_info_build

cmake_source_dir = os.environ.get('CMAKE_SOURCE_DIR')
cmake_build_dir = os.environ.get('CMAKE_BUILD_DIR')
cmake_install_prefix = os.environ.get('CMAKE_INSTALL_PREFIX')

canonical_python_lib = None
system = platform.system()
if system == 'Linux' or system == 'FreeBSD':
    canonical_python_lib = 'liblegion_canonical_python.so'
elif system == 'Darwin':
    canonical_python_lib = 'liblegion_canonical_python.dylib'
else:
    assert 0, 'Unsupported platform'

class my_build_py(build_py):
    def run(self):
        if not self.dry_run:
            self.mkpath(self.build_lib)
            legion_cffi_build.build_cffi(None, cmake_source_dir, cmake_build_dir, self.build_lib, ['legion.h'], ['runtime'], 'legion_builtin_cffi.py')
            legion_cffi_build.build_cffi(cmake_install_prefix + '/lib/' + canonical_python_lib, cmake_source_dir, cmake_build_dir, self.build_lib, ['canonical_python.h', 'legion.h'], [os.path.join('bindings', 'python'), 'runtime'], 'legion_canonical_cffi.py')
            legion_info_build.build_legion_info()
        build_py.run(self)

setup(name='legion',
      version='0.1',
      py_modules=[
          'legion_top',
          'legion_cffi',
          'legion_info',
          'pygion',
      ],
      cmdclass={'build_py': my_build_py})
