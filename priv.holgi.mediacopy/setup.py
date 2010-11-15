from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='priv.holgi.mediacopy',
      version=version,
      description="copy media non-redundantly",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ("Topic :: Software Development ::"
         "Libraries :: Python Modules")
        ],
      keywords='pictures copy exif',
      author='Holger Schauer',
      author_email='holger.schauer@gmx.de',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['priv', 'priv.holgi'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      test_suite='nose.collector',
      test_requires=['Nose'],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
