import codecs
from setuptools import setup, find_packages
from os import path

def read(*parts):
    return codecs.open(path.join(path.dirname(__file__), *parts),
                       encoding="utf-8").read()

setup(name='riemann_wrapper',
      version='0.6.0',
      description='send timing and exception stats to riemann',
      long_description=read('README.rst'),
      url='https://github.com/exoscale/python-riemann-wrapper',
      author='Pierre-Yves Ritschard',
      author_email='pierre-yves.ritschard@exoscale.ch',
      license='MIT, see LICENSE file',
      packages=find_packages(),
      include_package_data=True,
      install_requires=['bernhard'],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3'
      ],
      zip_safe=False)
