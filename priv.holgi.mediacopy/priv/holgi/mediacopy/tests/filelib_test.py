from os import access, chmod, path, remove, rmdir, stat, R_OK
from stat import S_IWUSR, S_IXUSR
from tempfile import mkstemp
from nose.tools import raises
from priv.holgi.mediacopy.filelib import validate_destination, copy_file
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
    def unwritable_destination_raises_ioerror_test(self):
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

    def valid_destination_returns_true_test(self):
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

    @property
    def _copiedfilepath(self):
        return path.join(self.destdir, self.testfilename)

    def testfile_accessible_test(self):
        assert (self.testfile and 
                path.exists(self.testfile) and 
                access(self.testfile, R_OK))

    def copyfile_generates_newfile_test(self):
        copy_file(self.testfile, self.destdir)
        assert (path.exists(self._copiedfilepath) and
                access(self._copiedfilepath, R_OK))
                  
