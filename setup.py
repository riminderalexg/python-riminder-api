import sys
from setuptools import setup

py_require_string = '==2.7.*'
version_minor = 9
py_version = sys.version_info[0]
if py_version >= 3:
    version_minor += 1
    py_require_string = '>=3.4'

version_string = '1.3.{}'.format(str(version_minor))

setup(name='riminder',
      version=version_string,
      description='python riminder riminder api package',
      url='https://github.com/Riminder/python-riminder-api',
      author='mnouayti',
      author_email='contact@rimider.net',
      license='MIT',
      packages=['riminder'],
      install_requires=[
          'requests==2.18.4',
          'python-magic==0.4.15'
      ],
      python_requires=py_require_string,
      zip_safe=False)
