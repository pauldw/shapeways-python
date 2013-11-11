from distutils.core import setup

setup(name='shapeways',
      version='2',
      description='Shapeways python bindings',
      author='Paul Walker',
      author_email='pwalker@fvml.ca',
      url='https://fvml.ca',
      packages=['shapeways'],
      install_requires=['rauth'],
)

# TODO: install_requires and test_suite