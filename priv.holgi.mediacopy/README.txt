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

Usage: mediacp.py [options] sourcedir

Options:
  -h, --help            show this help message and exit
  -d DESTINATION, --destination=DESTINATION
                        set destination (default: /home/schauer/Bilder/Fotos)
  -e, --encoding        file name encoding
  -f, --force           force overwrite
  -n, --noaction        don't perform the action
  -u, --unknown         copy unknown filetypes as well
  -v, --verbose         verbose logging

As you can see, mediacp.py expects a source directory which it will
recurse into and, optionally, a destination directory where to copy
the media files to.

mediascan.py has the following synopsis:

Usage: mediascan.py [options] sourcedir

Options:
  -h, --help      show this help message and exit
  -e, --encoding  file name encoding
  -n, --nowrite   don't write database
  -v, --verbose   verbose logging

mediascan will scan the mediafiles in sourcedir and record metadata
abouth them into a database with the name mediacp.db in sourcedir.
