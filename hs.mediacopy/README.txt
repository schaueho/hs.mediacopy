Introduction
============
mediacopy is a small python package intended to copy media files (i.e.
images, ...) from some source to some destination. It differs from a
simple copy operation in that it tries hard not to copy media a second
time.

Usage
=====
mediacopy consists of two simple shell utilities, mediacp.py and
mediascan.py. The first does the actual copying of media files while
the latter serves as a utility to (re-)scan a given directory of
already existing files at some destination.

mediacp.py has the following synopsis:

Usage: mediacp.py [options] sourcedir destinationdir

Options:
  -h, --help            show this help message and exit
  -D DATABASE, --database=DATABASE
                        location (path without filename) of database
  -f, --force           force overwrite
  -n, --noaction        don't perform the action
  -u, --unknown         copy unknown filetypes as well
  -v, --verbose         verbose logging

As you can see, mediacp.py expects a source directory which it will
recurse into and a destination directory to copy the media files to.

mediascan.py has the following synopsis:

Usage: mediascan.py [options] sourcedir

Options:
  -h, --help      show this help message and exit
  -D DATABASE, --database=DATABASE
                        location (path without filename) of database
  -n, --nowrite   don't write database
  -v, --verbose   verbose logging

mediascan will scan the mediafiles in sourcedir and record metadata
abouth them into a database with the name mediacp.db in sourcedir.

Installation
============
mediacopy comes as a python package ("egg"), which means that it is
intended to be installed via easy_install, cf. 
http://peak.telecommunity.com/DevCenter/EasyInstall

However, as of today, mediacopy is not distributed via
pypi.python.org. There is not even a so called 'source distribution'
package available -- besides the mercurial repository on
https://bitbucket.org/schaueho/mediacopy/. Hence, installation goes
currently works like this:

1. Install mercurial (hg)
2. Clone the bitbucket repository
   hg clone http://bitbucket.org/schaueho/mediacopy
3. Go to the directory priv.holgi.mediacopy
4. Issue a setup command:
   python setup.py install

This will /not/ download all required packages. In particular, it will
not download/install EXIF.py, which is available as a separate
download from http://sourceforge.net/projects/exif-py/ (it's neither
available as an egg nor as a source distribution of a python package
unfortunately). You must install EXIF.py into a place where your
python-installation can find it.

