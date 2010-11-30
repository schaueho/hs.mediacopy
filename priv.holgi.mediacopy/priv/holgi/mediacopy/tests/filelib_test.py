from os import access, chmod, path, remove, rmdir, stat, R_OK
from stat import S_IWUSR, S_IXUSR
from tempfile import mkstemp
from nose.tools import raises, istest, eq_
from priv.holgi.mediacopy.filelib import validate_destination, \
    copy_file, similar_filenames, find_similar_filenames
from priv.holgi.mediacopy.tests.mediacp_base_test import MediacpTestBase

class ValidateDestination_Test(MediacpTestBase):
    ''' Tests ensuring that we're handling a valid destination '''
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
        try:
            retval = validate_destination(self.destdir)
        except:
            self._teardown_testdir()
            assert False
        else:
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
        eq_(copy_file(self.testfile, self.destdir, True), True)

class SimilarFile_Test(MediacpTestBase):

    def _setup_manually(self):
        self._setup_testdir()
        self._setup_testpic()

    def _teardown_manually(self):
        self._teardown_testpic()
        self._teardown_testdir()
    
    def case_doesnt_matter_test(self):
        eq_(similar_filenames('CIMG2448.JPG', 'cimg2448.jpg'), True)

    def similar_extensions_test(self):
        eq_(similar_filenames('CIMG2448.JPG', 'CIMG2448.JPEG'), True)

    def case_and_similar_extensions_test(self):
        eq_(similar_filenames('CIMG2448.JPG', 'cimg2448.jpeg'), True)

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
