from setuptools import setup

setup(name='riminder',
      version='0.1',
      description='riminder api package wrapper',
      url='https://github.com/mnouayti/python-riminder-api',
      author='mnouayti',
      author_email='med.nouayti@gmail.com',
      license='MIT',
      packages=['requests==2.18.4', 'python-magic==0.4.15'],
      zip_safe=False)