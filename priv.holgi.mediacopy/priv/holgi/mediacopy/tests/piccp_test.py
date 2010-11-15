from os import path, rmdir
from tempfile import mkdtemp, gettempdir
from unittest import TestCase
from nose.tools import raises
from priv.holgi.mediacopy.piccp import validate_destination

class ValidateDestination_Test(TestCase):
    destdir = None
    
    @raises(IOError)
    def invalid_destination_raises_ioerror_test(self):
        dest = path.join("tmp","doesnotexist")
        validate_destination(dest)

    def valid_destination_returns_true_test(self):
        self._setup_testdir()
        if validate_destination(self.destdir):
            self._teardown_testdir()
            pass
        else:
            self._teardown_testdir()
            assert False

    def _setup_testdir(self):
        newdir=mkdtemp('','mct',gettempdir())
        self.destdir=newdir

    def _teardown_testdir(self):
        if self.destdir:
            rmdir(self.destdir)
            
