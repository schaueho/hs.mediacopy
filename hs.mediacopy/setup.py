from setuptools import setup, find_packages
import os

version = '0.2'

setup(name='hs.mediacopy',
      version=version,
      description="copy media files, avoiding duplicates",
      long_description=open("README.md").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ("Topic :: Software Development ::"
         "Topic :: Multimedia ::"
         "Libraries :: Python Modules")
        ],
      keywords='pictures copy exif',
      author='Holger Schauer',
      author_email='holger.schauer@gmx.de',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['hs'],
      include_package_data=True,
      zip_safe=True,
      setup_requires=['wheel'],
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'exifread',
          'python-magic',
          'sqlalchemy',
      ],
      dependency_links = [
      ],
      test_suite='nose.collector',
      tests_require=['Nose','fixture[decorators]'],
      entry_points={
        'console_scripts': [
            'mediacp=hs.mediacopy.mediacp:main',
            'mediascan=hs.mediacopy.mediascan:main'
            ],
        }
      )
