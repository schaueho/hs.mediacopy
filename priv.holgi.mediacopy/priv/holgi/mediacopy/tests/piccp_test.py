from os import chmod, path, remove, rmdir, stat
from stat import S_IWUSR, S_IXUSR
from tempfile import mkstemp, mkdtemp, gettempdir
from unittest import TestCase
from nose.tools import raises
from priv.holgi.mediacopy.piccp import validate_destination

class ValidateDestination_Test(TestCase):
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

    def _setup_testdir(self):
        newdir=mkdtemp('','mct',gettempdir())
        self.destdir=newdir

    def _teardown_testdir(self):
        if self.destdir:
            rmdir(self.destdir)
            
