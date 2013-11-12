from distutils.core import setup
import sys

if sys.version_info[0] == 2 and sys.version_info[1] < 7:
    sys.exit(1)

setup(name='shapeways',
      version='0.1.3',
      description='Shapeways python bindings',
      author='Paul Walker',
      author_email='pwalker@fvml.ca',
      url='https://github.com/pauldw/shapeways-python',
      packages=['shapeways'],
      install_requires=['rauth >= 0.6.2'],
)