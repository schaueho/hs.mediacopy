'''
    filelib_test.py -- tests related to file handling functions.
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

from os import access, chmod, path, remove, rmdir, stat, R_OK
from stat import S_IWUSR, S_IXUSR
from tempfile import mkstemp
from nose.tools import raises, istest, eq_
from hs.mediacopy.filelib import validate_destination, \
    copy_file, copy_newfile, is_knownfiletype, \
    similar_filenames, find_similar_filenames
from hs.mediacopy.tests.mediacp_base_test import MediacpTestBase

class ValidateDestination_Test(MediacpTestBase):
    ''' Tests ensuring that we are handling a valid destination '''
    destdir = None

    @raises(IOError)
    def inexistant_destination_raises_ioerror_test(self):
        dest = path.join("tmp","doesnotexist")
        validate_destination(dest)

    @raises(IOError)
    def file_destination_raises_ioerror_test(self):
        self._setup_testdir()
        (handler, tempfile) = mkstemp("", "mct", self.destdir)
        try:
            validate_destination(tempfile)
        except IOError, e:
            remove(tempfile)
            self._teardown_testdir()
            raise e
        else:
            remove(tempfile)
            self._teardown_testdir()
            assert False

    @raises(IOError)
    @istest
    def unwritable_destination_raises_ioerror(self):
        self._setup_testdir()
        chmod(self.destdir, stat(self.destdir).st_mode ^ S_IWUSR ^ S_IXUSR)
        try:
            validate_destination(self.destdir)
        except IOError, e:
            chmod(self.destdir, S_IWUSR & S_IXUSR)
            self._teardown_testdir()
            raise e
        else:
            chmod(self.destdir, S_IWUSR & S_IXUSR)
            self._teardown_testdir()
            assert False

    @istest
    def valid_destination_returns_true(self):
        self._setup_testdir()
        retval = None
        try:
            retval = validate_destination(self.destdir)
        finally:
            self._teardown_testdir()
        return retval

            
class CopyFile_Test(MediacpTestBase):
    ''' Tests related to copying a file '''

    def setUp(self):
        self._setup_testpic()
        self._setup_testdir()

    def tearDown(self):
        self._teardown_testpic()
        self._teardown_testdir()

    @istest
    def testfile_is_accessible(self):
        assert (self.testfile and 
                path.exists(self.testfile) and 
                access(self.testfile, R_OK))

    @istest
    def copyfile_generates_newfile(self):
        retval = copy_file(self.testfile, self.destdir)
        assert (path.exists(self._copiedfilepath) and
                access(self._copiedfilepath, R_OK))
        eq_(retval, True)

    @istest
    def copyfile_doesnt_overwrite(self):
        # we use an initial copy as test setup condition
        copy_file(self.testfile, self.destdir)
        eq_(copy_file(self.testfile, self.destdir), False)

    @istest
    def copyfile_overwrites_when_forced(self):
        # we use an initial copy as test setup condition
        copy_file(self.testfile, self.destdir)
        eq_(copy_file(self.testfile, self.destdir, overwrite=True), True)

    @istest
    def copy_newfile_doesnt_overwrite_similarfiles(self):
        # we use an initial copy as test setup condition
        copy_file(self.testfile, self.destdir)
        eq_(copy_newfile(self.testfile, self.destdir), False)

    @istest
    def copy_newfile_overwrites_similarfiles_when_forced(self):
        # we use an initial copy as test setup condition
        copy_file(self.testfile, self.destdir)
        eq_(copy_newfile(self.testfile, self.destdir, overwrite=True), True)

    @istest
    def copy_newfile_doesntcopy_unknownfiles(self):
        # we try to copy ourself!
        assert not(is_knownfiletype(__file__))
        eq_(copy_newfile(__file__, self.destdir), False)

    @istest
    def copy_newfile_copies_unknownfiles_if_forced(self):
        # we try to copy ourself!
        result = False
        assert not(is_knownfiletype(__file__))
        try:
            eq_(copy_newfile(__file__, self.destdir, copyunknown=True), True)
            result = True
        finally:
            remove(path.join(self.destdir, path.basename(__file__)))
        return result
        

class SimilarFile_Test(MediacpTestBase):

    def _setup_manually(self):
        self._setup_testdir()
        self._setup_testpic()

    def _teardown_manually(self):
        self._teardown_testpic()
        self._teardown_testdir()
    
    def case_doesnt_matter_test(self):
        eq_(similar_filenames(u'CIMG2448.JPG', u'cimg2448.jpg'), True)

    def similar_extensions_test(self):
        eq_(similar_filenames(u'CIMG2448.JPG', u'CIMG2448.JPEG'), True)

    def case_and_similar_extensions_test(self):
        eq_(similar_filenames(u'CIMG2448.JPG', u'cimg2448.jpeg'), True)

    @istest
    def find_similar_filenames_finds_matches_in_directories(self):
        self._setup_manually()
        copy_file(self.testfile, self.destdir)
        try:
            eq_(find_similar_filenames(self.destdir, self.testfilename), 
                [path.join(self.destdir, self.testfilename)])
        except AssertionError, e:
            self._teardown_manually()
            raise e
        else:
            self._teardown_manually()
            return True
