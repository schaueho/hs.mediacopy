'''
    applogic.py -- main copy/scanning functionality.
    Basically, this is where we bring InfoStore objects,
    files and MetaInfo objects together.
    This file is part of mediacopy.

    Copyright (C) 2010 Holger Schauer <holger.schauer@gmx.de>

    mediacopy is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from hs.mediacopy.types import get_metainfo
from hs.mediacopy.utils import logger, unicodify
from hs.mediacopy.filelib import reduce_filename, \
    copy_file, walktree

def mediacopy_directory(sourcedir, destination, store, options, result):
    ''' Copy mediadata from sourcedir to destination, storing metainfos 
    Argument result is an accumulator storing counting information
    (tuple with three elements) about seen nrs. of seen files,
    copied files and duplicate files so far. Returns an updated 
    triple as result.'''

    (seen, copied, dupes) = result
    callback = lambda fname, counts: mediacopy_file(fname, destination, store, options, counts)
    (seen, copied, dupes) = walktree(sourcedir, callback, result)
    return (seen, copied, dupes)

def mediacopy_file(filename, destination, store, options, result):
    ''' Copy filename to destination, storing metainfo 
    Argument result is an accumulator storing counting information
    (tuple with three elements) about seen nrs. of seen files,
    copied files and duplicate files so far. Returns an updated 
    triple as result.'''

    (filecount, copycount, dupecount) = result
    filename = unicodify(filename, options.encoding or 'utf-8')
    duplicate = find_metainfo(store, filename)
    if duplicate:
        dupecount = dupecount + 1
        if options.force:
            logger.info("Force copy of duplicate %s" % filename)
            result = copy_and_store(filename, destination, store, options, True)
        else:
            logger.info("Ignoring duplicate %s" % filename)
    else:
        result = copy_and_store(filename, destination, store, options, False)
    filecount = filecount + 1
    if result is True:
        copycount = copycount + 1
    return (filecount, copycount, dupecount)

def copy_and_store(filename, destination, store, options, duplicate=False):
    ''' Copy file to destination and store metainfo
    If duplicate is True, copy only if options.force is also True.
    If options.noaction is True, do not really copy or store.'''

    result = True
    if options.noaction:
        logger.info("Would copy %s" % filename)
    else:
        if options.verbose:
            logger.info("Would copy %s" % filename)
        result = copy_file(filename, destination,
                           options.force, options.noaction, 
                           options.copyunknown)
        if not(duplicate):
            store.put_metainfo(get_metainfo(filename))
    return result

def store_metainfo_directory(store, sourcedir, options, result):
    ''' Store metainfo from directory in store 
    Argument result is an accumulator storing counting information
    (tuple with two elements) about seen nrs. of seen files,
    and duplicate files so far. Returns an updated tuple as result.'''

    (seen, dupes) = result
    callback  = lambda fname,counts : store_metainfo_file(store, fname, options, counts)
    (seen, dupes) = walktree(sourcedir, callback, (seen, dupes))
    logger.info("Saw %s files and %s duplicates" % (seen, dupes))
    return (seen, dupes)

def store_metainfo_file(store, filename, options, result):
    ''' Store metainfos and return the number of seen files
    Argument result is an accumulator storing counting information
    (tuple with two elements) about seen nrs. of seen files,
    and duplicate files so far. Returns an updated tuple as result.'''

    (seen, dupes) = result
    ufilename = unicodify(filename, options.encoding)
    basename = reduce_filename(ufilename)
    if options.verbose:
        logger.info("Scanning %s" % basename)
    if find_metainfo(store, ufilename):
        logger.info("Ignoring duplicate %s" % basename)
        dupes = dupes + 1
    else:
        store.put_metainfo(get_metainfo(ufilename))
    seen = seen + 1
    return (seen, dupes)

def find_metainfo(store, filename):
    ''' Check whether (metainfo for) filename is already contained in store 
    Returns metainfo if found, False otherwise.
    '''
    basename = reduce_filename(filename)
    if store.find_similar_by_name(basename):
        metainfo = get_metainfo(filename)
        if metainfo:
            result = store.find_similar(metainfo)
            return result
    return False

