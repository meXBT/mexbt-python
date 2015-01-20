from setuptools import setup

setup(name='mexbt',
      version='0.1',
      description='A lightweight python client for the meXBT exchange API',
      url='http://github.com/meXBT/mexbt-python',
      author='meXBT',
      author_email='william@mexbt.com',
      license='MIT',
      packages=['mexbt'],
      install_requires=['requests'],
      zip_safe=False)