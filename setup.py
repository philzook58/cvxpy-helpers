from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()
    
setup(name='cvxpy-mip-helpers',
      version='0.1',
      description='Helper functions for mip formulations in cvxpy',
      url='http://github.com/storborg/funniest',
      author='Philip Zucker',
      author_email='flyingcircus@example.com',
      license='MIT',
      packages=['cvxpy-mip-helpers'],
      install_requires=[
          'cvxpy',
          'numpy',
      ],
      zip_safe=False)
