from __future__ import unicode_literals

from codecs import open as codecs_open
from setuptools import setup, find_packages


# Get the long description from the relevant file
with codecs_open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setup(name='osmgraph',
      version='0.0.1',
      description="Create networkx graphs from OpenStreetMap data",
      long_description=long_description,
      classifiers=[],
      keywords='',
      author="Jacob Wasserman",
      author_email='jwasserman@gmail.com',
      url='https://github.com/mapkin/osmgraph',
      license='MIT',
      packages=find_packages(exclude=['tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'geog',
          'imposm.parser',
          'networkx',
      ],
      extras_require={
          'test': ['pytest'],
      },
)
