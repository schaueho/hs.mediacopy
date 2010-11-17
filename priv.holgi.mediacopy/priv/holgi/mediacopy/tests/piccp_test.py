from os import access, chmod, path, remove, rmdir, stat, R_OK
from stat import S_IWUSR, S_IXUSR
from tempfile import mkstemp, mkdtemp, gettempdir
from unittest import TestCase
from nose.tools import raises
from priv.holgi.mediacopy.filelib import validate_destination, copy_file

class MediacpTestBase(TestCase):
    ''' class for providing base functionality required by Test classes 
    Serves basically as some kind of a zope.testing layer, w/o the benefits
    of a real layer.
    '''
    def _setup_testdir(self):
        newdir=mkdtemp('','mct',gettempdir())
        self.destdir=newdir

    def _teardown_testdir(self):
        if self.destdir:
            rmdir(self.destdir)
    

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
        package_dir = path.dirname(__file__)
        self.testfilename = 'CIMG2448.JPG'
        self.testfile = path.join(package_dir, self.testfilename)
        self._setup_testdir()

    def tearDown(self):
        if path.exists(self._copiedfilepath):
            remove(self._copiedfilepath)
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
                  
