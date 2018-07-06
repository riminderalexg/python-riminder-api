from setuptools import setup

setup(name='riminder',
      version='1.1.2',
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
      python_requires='>=3.4',
      zip_safe=False)
