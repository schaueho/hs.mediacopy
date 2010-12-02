#!/usr/bin/python

import os
from optparse import OptionParser
from priv.holgi.mediacopy.filelib import validate_destination, \
    walktree
from priv.holgi.mediacopy.types import get_metainfo

def parse_options():
    usage = "usage: %prog [options] sourcedir"
    parser = OptionParser(usage=usage)
    parser.add_option('-v', '--verbose', dest="verbose", action="store_true",
                      help="verbose logging")
    options, args = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")
    return [parser, options, args]

class MetadataCollection(object):

    def __init__(self):
        self.metadata = {}

    def add_metainfo(self, metainfo):
        if metainfo:
            self.metadata[metainfo.name] = metainfo
        return self

    def printall(self):
        for (name, metadata) in self.metadata.items():
            print "%s:%s" % (name, metadata)

def main():
    callback = None
    parser, options, args = parse_options()
    try:
        validate_destination(args[0])
    except IOError, e:
        parser.print_help()
        raise e
    collection = MetadataCollection()
    callback = lambda f: collection.add_metainfo(get_metainfo(f))
    walktree(args[0], callback)
    collection.printall()

if __name__ == "__main__":
    main()
